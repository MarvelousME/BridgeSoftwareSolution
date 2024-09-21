const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const cors = require('cors');

// Create an instance of the express app
const app = express();
const port = process.env.PORT || 3000;

// Middleware setup
app.use(cors()); // Allow cross-origin requests
app.use(bodyParser.json()); // Parse JSON bodies
app.use(bodyParser.urlencoded({ extended: true })); // Parse URL-encoded bodies

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// API routes
app.get('/api/data', (req, res) => {
    // Sample data endpoint - replace with actual data fetching logic
    const sampleData = {
        message: 'This is sample data from the API.'
    };
    res.json(sampleData);
});

app.post('/api/contact', (req, res) => {
    const { name, email, message } = req.body;
    // Handle contact form submission - replace with actual logic
    console.log('Contact form submitted:', { name, email, message });
    res.status(200).send('Contact form submitted successfully!');
});

// Serve the index.html file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

