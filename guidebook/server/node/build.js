
const fs = require('fs');
const path = require('path');

// Create default data if it doesn't exist
const dataPath = path.join(__dirname, 'data.json');
if (!fs.existsSync(dataPath)) {
    const defaultData = {
        title: "Guidebook",
        categories: [],
        points: []
    };
    fs.writeFileSync(dataPath, JSON.stringify(defaultData, null, 2));
    console.log('Created default data.json');
}