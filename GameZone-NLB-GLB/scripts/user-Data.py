#!/bin/bash

# Update system
apt update -y

# Install Python + venv
apt install -y python3 python3-venv

cd /home/ubuntu

# Create virtual environment
python3 -m venv venv

# Activate venv and install Flask
source venv/bin/activate
pip install flask

# Create Flask app
cat <<EOF > /home/ubuntu/app.py
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Simulated player pool
players = ["player1", "player2", "player3"]

# Root endpoint
@app.route("/")
def home():
    return "GameZone Backend Running (Ubuntu + venv)"

# Casual match (direct path)
@app.route("/casual-match")
def casual():
    player = random.choice(players)
    return jsonify({
        "mode": "casual",
        "player": player,
        "latency": random.randint(20, 40),
        "note": "No inspection path"
    })

# Ranked match (GWLB path)
@app.route("/ranked-match")
def ranked():
    player = random.choice(players)
    return jsonify({
        "mode": "ranked",
        "player": player,
        "latency": random.randint(60, 120),
        "client_ip": request.remote_addr,
        "note": "This will go via GWLB"
    })

# Health check (for NLB)
@app.route("/health")
def health():
    return {"status": "ok"}, 200

# Start app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
EOF

# Run app using venv Python
nohup /home/ubuntu/venv/bin/python /home/ubuntu/app.py > /home/ubuntu/app.log 2>&1 &