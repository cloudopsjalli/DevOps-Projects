from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users')
def get_users():
    return jsonify([
        {"id": 1, "name": "Kalyan"},
        {"id": 2, "name": "Azure Deploy"}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)