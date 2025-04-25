import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from PIL import Image
from models import db, Customer, Menu, Order, OrderItem

# Setup Flask
app = Flask(__name__, static_folder='public')
CORS(app)

# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Konfigurasi folder upload
UPLOAD_FOLDER = 'public'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inisialisasi database
db.init_app(app)
with app.app_context():
    db.create_all()

# ================================
#            MENU SERVICE
# ================================

@app.route('/menus', methods=['GET'])
def get_menus():
    menus = Menu.query.all()
    result = []
    for menu in menus:
        foto_url = url_for('static', filename=menu.foto) if menu.foto else url_for('static', filename='default.png')
        result.append({
            'id': menu.id,
            'nama': menu.nama,
            'harga': menu.harga,
            'foto': foto_url
        })
    return jsonify(result)

@app.route('/menus/<int:id>', methods=['GET'])
def get_menu(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({'message': 'Menu tidak ditemukan'}), 404

    return jsonify({
        'id': menu.id,
        'nama': menu.nama,
        'harga': menu.harga,
        'foto': menu.foto
    })

@app.route('/menus', methods=['POST'])
def create_menu():
    nama = request.form.get('nama')
    harga = request.form.get('harga')
    foto = request.files.get('foto')

    if not nama or not harga:
        return jsonify({'message': 'Nama dan harga wajib diisi'}), 400

    filename = 'default.png'
    if foto:
        try:
            img = Image.open(foto)
            filename = secure_filename(f"{nama}.png")
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'PNG')
        except Exception as e:
            print(f"Error converting image to PNG: {e}")
            filename = 'default.png'

    new_menu = Menu(nama=nama, harga=int(harga), foto=filename)
    db.session.add(new_menu)
    db.session.commit()

    return jsonify({'message': 'Menu berhasil ditambahkan'}), 201

@app.route('/menus/<int:id>', methods=['PUT'])
def update_menu(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({'message': 'Menu tidak ditemukan'}), 404

    # Mengambil data dari form (FormData)
    nama = request.form.get('nama')
    harga = request.form.get('harga')
    foto = request.files.get('foto')  # Foto baru jika ada

    menu.nama = nama
    menu.harga = int(harga)

    # Jika ada foto baru yang di-upload
    if foto:
        filename = secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        menu.foto = filename

    db.session.commit()
    return jsonify({'message': 'Menu berhasil diperbarui'})

@app.route('/menus/<int:id>', methods=['DELETE'])
def delete_menu(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({'message': 'Menu tidak ditemukan'}), 404

    db.session.delete(menu)
    db.session.commit()
    return jsonify({'message': 'Menu berhasil dihapus'})

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
    data = request.json
    customer_id = data['customer_id']
    order_items = data['order_items']
    metode_pembayaran = data['metode_pembayaran']
    tanggal_pembelian = datetime.strptime(data['tanggal_pembelian'], '%Y-%m-%d').date()

    total_harga = 0
    for item in order_items:
        menu = Menu.query.get(item['menu_id'])
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

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
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
    orders = Order.query.all()
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
    app.run(port=5000, debug=True)