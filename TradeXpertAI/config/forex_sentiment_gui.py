import tkinter as tk
from tkinter import ttk
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define function to load data from JSON file
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Define function to update the tree view with forex data
def update_treeview(data):
    for forex in data['forex_data']:
        pair = forex['pair']
        sentiment_score = forex['sentiment']['overall_sentiment_score']
        price = forex['market_data']['price']
        volatility = forex['market_data']['volatility']
        
        tree.insert('', 'end', values=(pair, price, sentiment_score, volatility))

# Define function to plot data
def plot_data(data):
    pairs = [forex['pair'] for forex in data['forex_data']]
    sentiment_scores = [forex['sentiment']['overall_sentiment_score'] for forex in data['forex_data']]
    prices = [forex['market_data']['price'] for forex in data['forex_data']]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    color = 'tab:blue'
    ax1.set_xlabel('Forex Pair')
    ax1.set_ylabel('Sentiment Score', color=color)
    ax1.bar(pairs, sentiment_scores, color=color, alpha=0.6, label='Sentiment Score')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Price', color=color)
    ax2.plot(pairs, prices, color=color, marker='o', label='Price')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Forex Sentiment and Price Visualization')

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# Create the main application window
root = tk.Tk()
root.title("Forex Sentiment Analysis")

# Set up the frame for the tree view and plot
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

# Create a tree view to display forex sentiment data
tree = ttk.Treeview(frame, columns=("Pair", "Price", "Sentiment Score", "Volatility"), show='headings')
tree.heading('Pair', text='Forex Pair')
tree.heading('Price', text='Price')
tree.heading('Sentiment Score', text='Sentiment Score')
tree.heading('Volatility', text='Volatility')
tree.pack(side='left', fill='both', expand=True)

# Load the forex sentiment data
FOREX_SENTIMENT_FILE = 'forex_sentiment.json'
data = load_data(FOREX_SENTIMENT_FILE)

# Update the tree view with the loaded data
update_treeview(data)

# Plot the data
plot_data(data)

# Run the application
root.mainloop()

