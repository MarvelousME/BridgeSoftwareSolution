const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors()); // Allows cross-origin requests
app.use(bodyParser.json()); // Parses JSON bodies
app.use(bodyParser.urlencoded({ extended: true })); // Parses URL-encoded bodies

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// API endpoints
app.get('/api/data', (req, res) => {
    // Replace with your actual data-fetching logic
    const sampleData = {
        message: 'This is sample data from the API.'
    };
    res.json(sampleData);
});

app.post('/api/contact', (req, res) => {
    const { name, email, message } = req.body;
    // Replace with your actual logic for handling contact form submissions
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

