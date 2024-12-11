const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const app = express();

// Enhanced CORS configuration
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type']
}));

app.use(express.json());

// Add security headers middleware
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

const dataPath = path.join(__dirname, 'data.json');

// Status endpoint
app.get('/api/status', (req, res) => {
    res.status(200).json({ status: 'online' });
});

// Enhanced error handling
app.get('/api/data', (req, res) => {
    try {
        if (!fs.existsSync(dataPath)) {
            // Create default data if file doesn't exist
            const defaultData = {
                title: "Guidebook",
                categories: [],
                points: []
            };
            fs.writeFileSync(dataPath, JSON.stringify(defaultData, null, 2));
        }
        
        const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
        console.log('Data sent successfully');
        res.json(data);
    } catch (error) {
        console.error('Error reading data:', error);
        res.status(500).json({ error: 'Failed to read data', details: error.message });
    }
});

app.post('/api/data', (req, res) => {
    try {
        fs.writeFileSync(dataPath, JSON.stringify(req.body, null, 2));
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ error: 'Failed to write data' });
    }
});

const port = 3000;
app.listen(port, () => {
    console.log(`Guidebook server running on port ${port}`);
});