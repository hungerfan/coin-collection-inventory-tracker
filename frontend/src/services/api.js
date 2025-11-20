import axios from 'axios'

// Base URL for Django API
const API_BASE_URL = 'http://localhost:8000/api'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API functions will go here
async function getAllCoins() {
    let url = '/coins/';
    const items = [];
    while (url) {
      const { data } = await api.get(url);
      const pageItems = data.results || data;
      items.push(...pageItems);
      url = data.next ? data.next.replace(API_BASE_URL, '') : null; // keep it relative
    }
    return items;
  }

async function getStats() {
    const { data } = await api.get('/stats/');
    return data;
}


export { getAllCoins, getStats };