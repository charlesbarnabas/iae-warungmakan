from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setup Flask
app = Flask(__name__)
CORS(app)

# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi database
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the app
app.app_context().push() #push app context

# ================================
#            MODEL
# ================================
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(180), nullable=False)
    no_telp = db.Column(db.String(20), nullable=False)

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.String(255), nullable=True)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    total_harga = db.Column(db.Integer, nullable=False)
    metode_pembayaran = db.Column(db.String(20), nullable=False)
    tanggal_pembelian = db.Column(db.Date, nullable=False)

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    menu = db.relationship('Menu', backref=db.backref('order_items', lazy=True))