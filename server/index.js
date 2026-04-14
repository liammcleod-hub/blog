const express = require('express');
const cors = require('cors');
const path = require('path');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Basic API routes
app.get('/api/stats', async (req, res) => {
  try {
    // In a real app, these would be SQL queries. 
    // For now, we'll serve the mock data we generated.
    const fs = require('fs');
    const data = JSON.parse(fs.readFileSync(path.join(__dirname, '../mock_data.json'), 'utf8'));
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
