from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DB_PATH = '/mnt/data/products.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        image TEXT,
                        price REAL,
                        description TEXT,
                        category TEXT
                    )''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT name, image, price, description, category FROM products")
        products = c.fetchall()
    return render_template('index.html', products=products)

@app.route('/admin')
def admin():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
    return render_template('admin.html', products=products)

@app.route('/admin/add', methods=['POST'])
def add_product():
    name = request.form['name']
    image = request.form['image']
    price = float(request.form['price'])
    description = request.form['description']
    category = request.form['category']
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO products (name, image, price, description, category) VALUES (?, ?, ?, ?, ?)",
                  (name, image, price, description, category))
        conn.commit()
    return redirect(url_for('admin'))

@app.route('/admin/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    name = request.form['name']
    image = request.form['image']
    price = float(request.form['price'])
    description = request.form['description']
    category = request.form['category']
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("UPDATE products SET name=?, image=?, price=?, description=?, category=? WHERE id=?",
                  (name, image, price, description, category, product_id))
        conn.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
