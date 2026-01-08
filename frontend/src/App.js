import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [items, setItems] = useState([]);
  const [itemName, setItemName] = useState('');
  const [itemDescription, setItemDescription] = useState('');

  useEffect(() => {
    fetchItems();
  }, []);

 

  const fetchItems = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/items`);
      // Change this line:
      setItems(response.data); 
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE_URL}/api/items`, {
        name: itemName,
        description: itemDescription
      });
      setItemName('');
      setItemDescription('');
      fetchItems();
    } catch (error) {
      console.error('Error creating item:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>My Fullstack App</h1>
      
        
        <div className="form-container">
          <h2>Add New Item</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Item Name"
              value={itemName}
              onChange={(e) => setItemName(e.target.value)}
              data-testid="item-name-input"
              required
            />
            <input
              type="text"
              placeholder="Description"
              value={itemDescription}
              onChange={(e) => setItemDescription(e.target.value)}
              data-testid="item-description-input"
            />
            <button type="submit" data-testid="submit-button">Add Item</button>
          </form>
        </div>

        <div className="items-container">
          <h2>Items List</h2>
          <ul data-testid="items-list">
            {items.map((item, index) => (
              <li key={index}>
                <strong>{item.name}</strong>: {item.description}
              </li>
            ))}
          </ul>
        </div>
      </header>
    </div>
  );
}
export default App;