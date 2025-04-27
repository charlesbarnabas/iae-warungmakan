from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Customer, Menu, Order, OrderItem

# Setup Flask
app = Flask(__name__)
CORS(app)

# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi database
db.init_app(app)
with app.app_context():
    db.create_all()

# ================================
#     CUSTOMER & ORDERS SERVICE
# ================================

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    new_customer = Customer(
        nama=data['nama'],
        no_telp=data['no_telp']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'id': new_customer.id}), 201

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.json
        # Use the database column names explicitly
        customer_id = data['customer_id']
        order_items = data['order_items']
        metode_pembayaran = data['metode_pembayaran']
        tanggal_pembelian = datetime.strptime(data['tanggal_pembelian'], '%Y-%m-%d').date()

        total_harga = 0
        for item in order_items:
            menu = db.session.get(Menu, item['menu_id'])
            if not menu:
                return jsonify({'message': f"Menu dengan id {item['menu_id']} tidak ditemukan"}), 400
            total_harga += menu.harga * item['quantity']

        new_order = Order(
            customer_id=customer_id,
            total_harga=total_harga,
            metode_pembayaran=metode_pembayaran,
            tanggal_pembelian=tanggal_pembelian
        )
        db.session.add(new_order)
        db.session.commit()

        for item in order_items:
            order_item = OrderItem(
                order_id=new_order.id,
                menu_id=item['menu_id'],
                quantity=item['quantity']
            )
            db.session.add(order_item)
        db.session.commit()

        return jsonify({'message': 'Order berhasil dibuat', 'order_id': new_order.id}), 201
    except Exception as e:
        return jsonify({'message': 'Error saat membuat order', 'error': str(e)}), 500

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = db.session.get(Order, id)
    if not order:
        return jsonify({'message': 'Order tidak ditemukan'}), 404

    items = []
    for item in order.order_items:
        items.append({
            'nama_menu': item.menu.nama,
            'quantity': item.quantity,
            'harga_satuan': item.menu.harga
        })

    return jsonify({
        'nama_customer': order.customer.nama,
        'no_telp': order.customer.no_telp,
        'total_harga': order.total_harga,
        'metode_pembayaran': order.metode_pembayaran,
        'tanggal_pembelian': order.tanggal_pembelian.strftime('%Y-%m-%d'),
        'items': items
    })

@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders = db.session.query(Order).all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'nama_customer': order.customer.nama,
            'total_harga': order.total_harga,
            'metode_pembayaran': order.metode_pembayaran,
            'tanggal_pembelian': order.tanggal_pembelian.strftime('%Y-%m-%d')
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001, debug=True)