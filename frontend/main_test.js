import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import axios from 'axios';

jest.mock('axios');

test('renders environment badge', async () => {
  axios.get.mockResolvedValue({ data: { environment: 'local', items: [] } });
  
  render(<App />);
  
  await waitFor(() => {
    const badge = screen.getByTestId('environment-badge');
    expect(badge).toBeInTheDocument();
  });
});