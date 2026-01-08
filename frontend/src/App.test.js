import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import App from './App';

jest.mock('axios');

describe('App Component Tests', () => {
  
  beforeEach(() => {
    jest.clearAllMocks();
    
    axios.get.mockImplementation((url) => {
      if (url.endsWith('/')) {
        return Promise.resolve({ data: { environment: 'testing' } });
      }
      if (url.endsWith('/api/items')) {
        return Promise.resolve({ data: [
          { name: 'Existing Item', description: 'A description' }
        ]});
      }
      return Promise.reject(new Error('not found'));
    });

    axios.post.mockResolvedValue({ 
      data: { name: 'New Item', description: 'New Description' } 
    });
  });


  test('Unit 1: Renders the main application title', async () => {
    await act(async () => { render(<App />); });
    const linkElement = screen.getByText(/My Fullstack App/i);
    expect(linkElement).toBeInTheDocument();
  });

  test('Unit 2: Renders the form input fields correctly', async () => {
    await act(async () => { render(<App />); });
    const nameInput = screen.getByTestId('item-name-input');
    const descInput = screen.getByTestId('item-description-input');
    
    expect(nameInput).toBeInTheDocument();
    expect(descInput).toBeInTheDocument();
    expect(nameInput).toHaveAttribute('placeholder', 'Item Name');
  });

  test('Unit 3: Renders the submit button', async () => {
    await act(async () => { render(<App />); });
    const button = screen.getByTestId('submit-button');
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent('Add Item');
  });


  test('Integration 1: Fetches and displays data on load', async () => {
    await act(async () => { render(<App />); });

    await waitFor(() => {
      expect(screen.getByText('TESTING')).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByText('Existing Item')).toBeInTheDocument();
    });

    expect(axios.get).toHaveBeenCalledTimes(2);
  });

  test('Integration 2: Allows user to add an item and refreshes list', async () => {
    await act(async () => { render(<App />); });

    const nameInput = screen.getByTestId('item-name-input');
    const descInput = screen.getByTestId('item-description-input');
    const submitBtn = screen.getByTestId('submit-button');

    fireEvent.change(nameInput, { target: { value: 'New Item' } });
    fireEvent.change(descInput, { target: { value: 'New Description' } });

    axios.get.mockImplementation((url) => {
      if (url.endsWith('/api/items')) {
        return Promise.resolve({ data: [
          { name: 'Existing Item', description: 'A description' },
          { name: 'New Item', description: 'New Description' } 
        ]});
      }
      return Promise.resolve({ data: { environment: 'testing' } });
    });

    fireEvent.click(submitBtn);

   await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/items'), 
        { name: 'New Item', description: 'New Description' }
      );
    });

    // FIX: Wrap this assertion in waitFor so it waits for the state update
    await waitFor(() => {
      expect(nameInput.value).toBe('');
    });

    await waitFor(() => {
      expect(screen.getByText('New Item')).toBeInTheDocument();
    });
  });

});