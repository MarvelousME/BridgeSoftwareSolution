import tkinter as tk
from tkinter import ttk
import json
import os

# Define function to load data from JSON file
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        return json.load(file)

# Define function to update the tree view with forex data
def update_treeview(data):
    if 'forex_data' not in data:
        raise KeyError("The 'forex_data' key is missing from the JSON data.")
    
    for forex in data['forex_data']:
        pair = forex.get('pair', 'N/A')
        sentiment_score = forex.get('sentiment', {}).get('overall_sentiment_score', 'N/A')
        price = forex.get('market_data', {}).get('price', 'N/A')
        volatility = forex.get('market_data', {}).get('volatility', 'N/A')
        
        tree.insert('', 'end', values=(pair, price, sentiment_score, volatility))

# Create the main application window
root = tk.Tk()
root.title("Forex Sentiment Analysis")

# Set up the frame for the tree view
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

# Create a tree view to display forex sentiment data
tree = ttk.Treeview(frame, columns=("Pair", "Price", "Sentiment Score", "Volatility"), show='headings')
tree.heading('Pair', text='Forex Pair')
tree.heading('Price', text='Price')
tree.heading('Sentiment Score', text='Sentiment Score')
tree.heading('Volatility', text='Volatility')
tree.pack(fill='both', expand=True)

# Load the forex sentiment data
FOREX_SENTIMENT_FILE = 'forex_sentiment.json'

try:
    data = load_data(FOREX_SENTIMENT_FILE)
    # Update the tree view with the loaded data
    update_treeview(data)
except Exception as e:
    error_label = tk.Label(root, text=f"Error: {e}", fg='red')
    error_label.pack(pady=10)

# Run the application
root.mainloop()

