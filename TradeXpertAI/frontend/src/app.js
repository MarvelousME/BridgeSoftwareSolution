

// Vanilla JavaScript Code
document.addEventListener('DOMContentLoaded', () => {
    const fetchDataBtn = document.getElementById('fetchDataBtn');
    const dataDisplay = document.getElementById('dataDisplay');
    
    fetchDataBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/data'); // Adjust endpoint as needed
            const data = await response.json();
            dataDisplay.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    const contactForm = document.getElementById('contactForm');
    
    contactForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(contactForm);
        const data = {};
        
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        try {
            await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            alert('Message sent successfully!');
        } catch (error) {
            console.error('Error sending message:', error);
        }
    });
});

// React Code
import React from 'react';
import ReactDOM from 'react-dom';
import Header from './header';
import Footer from './footer';
import Sidebar from './sidebar';

const App = () => {
    return (
        <div className="app-container">
            <Header />
            <div className="main-content">
                <Sidebar />
                <div className="content">
                    {/* Your main content goes here */}
                    <button id="fetchDataBtn">Fetch Data</button>
                    <pre id="dataDisplay"></pre>
                    <form id="contactForm">
                        <input type="text" name="name" placeholder="Your Name" required />
                        <input type="email" name="email" placeholder="Your Email" required />
                        <textarea name="message" placeholder="Your Message" required></textarea>
                        <button type="submit">Send Message</button>
                    </form>
                </div>
            </div>
            <Footer />
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));

