
const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('ui'));

// API endpoint to get data
app.get('/api/data', async (req, res) => {
    try {
        const data = await fs.readFile('./ui/mockdata.json', 'utf8');
        res.json(JSON.parse(data));
    } catch (error) {
        res.status(500).send('Error reading data');
    }
});

// API endpoint to save data
app.post('/api/data', async (req, res) => {
    try {
        await fs.writeFile('./ui/mockdata.json', JSON.stringify(req.body, null, 4));
        res.send('Data saved successfully');
    } catch (error) {
        res.status(500).send('Error saving data');
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});