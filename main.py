from flask import Flask, render_template, jsonify, request
import random
from datetime import datetime, timedelta

app = Flask(__name__)

class BitcoinSimulator:
    def __init__(self):
        self.price = 45000.0
        self.balance = 10000.0  # Starting with $10,000
        self.btc = 0.0
        self.history = []
        
    def update_price(self):
        change_percent = random.uniform(-2, 2)
        change = self.price * (change_percent / 100)
        self.price = max(1000, self.price + change)
        self.history.append({
            "time": datetime.now().strftime("%H:%M"),
            "price": round(self.price, 2),
            "change_24h": round(change_percent, 2)
        })
        if len(self.history) > 60:  # Keep last hour of data
            self.history.pop(0)
        return round(self.price, 2)

simulator = BitcoinSimulator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update')
def update():
    price = simulator.update_price()
    return jsonify({
        'price': price,
        'balance': round(simulator.balance, 2),
        'btc': round(simulator.btc, 6),
        'history': simulator.history
    })

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json()
    action = data.get('action')
    amount = float(data.get('amount', 0))
    
    if action == 'buy':
        if amount * simulator.price <= simulator.balance:
            simulator.balance -= amount * simulator.price
            simulator.btc += amount
    elif action == 'sell':
        if amount <= simulator.btc:
            simulator.balance += amount * simulator.price
            simulator.btc -= amount
            
    return jsonify({
        'balance': round(simulator.balance, 2),
        'btc': round(simulator.btc, 6)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
