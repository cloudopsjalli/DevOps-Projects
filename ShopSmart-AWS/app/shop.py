from flask import Flask
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="shopsmart-db.xxxxxxxxxxxxxxxxxxxxx.amazonaws.com",
        user="admin",
        password="admin123",
        database="shopsmart"
    )

@app.route("/")
def home():
    return "<h1>Welcome to ShopSmart</h1><a href='/products'>View Products</a>"

@app.route("/products")
def products():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    output = "<h2>Product List</h2>"
    for row in rows:
        output += f"<p>{row[1]} - ${row[2]}</p>"

    cursor.close()
    db.close()
    return output

@app.route("/add")
def add():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES ('Tablet', 300)")
    db.commit()
    cursor.close()
    db.close()
    return "Product Added"

app.run(host="0.0.0.0", port= 5050)