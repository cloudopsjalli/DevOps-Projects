from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Product Service is running!"

@app.route('/products')
def get_products():
    return jsonify([
        {"id": 101, "name": "Laptop"},
        {"id": 102, "name": "Phone"}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)