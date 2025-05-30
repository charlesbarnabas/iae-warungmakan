import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from models import db, Menu, Order, OrderItem, Customer

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
            'category': menu.category,
            'foto': foto_url
        })
    return jsonify(result)

@app.route('/menus/<int:id>', methods=['GET'])
def get_menu(id):
    menu = db.session.get(Menu, id)
    if not menu:
        return jsonify({'message': 'Menu tidak ditemukan'}), 404

    foto_url = url_for('static', filename=menu.foto) if menu.foto else url_for('static', filename='default.png')
    return jsonify({
        'id': menu.id,
        'nama': menu.nama,
        'harga': menu.harga,
        'category': menu.category,
        'foto': foto_url
    })

@app.route('/menus', methods=['POST'])
def create_menu():
    nama = request.form.get('nama')
    harga = request.form.get('harga')
    category = request.form.get('category')
    foto = request.files.get('foto')

    if not nama or not harga or not category:
        return jsonify({'message': 'Nama, harga, dan kategori wajib diisi'}), 400

    filename = 'default.png'
    if foto:
        try:
            img = Image.open(foto)
            filename = secure_filename(f"{nama}.png")
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'PNG')
        except Exception as e:
            print(f"Error converting image to PNG: {e}")
            filename = 'default.png'

    new_menu = Menu(nama=nama, harga=int(harga), category=category, foto=filename)
    db.session.add(new_menu)
    db.session.commit()

    return jsonify({'message': 'Menu berhasil ditambahkan'}), 201

@app.route('/menus/<int:id>', methods=['PUT'])
def update_menu(id):
    menu = db.session.get(Menu, id)
    if not menu:
        return jsonify({'message': 'Menu tidak ditemukan'}), 404

    nama = request.form.get('nama')
    harga = request.form.get('harga')
    category = request.form.get('category')
    foto = request.files.get('foto')

    if not nama or not harga or not category:
        return jsonify({'message': 'Nama, harga, dan kategori wajib diisi'}), 400

    menu.nama = nama
    menu.harga = int(harga)
    menu.category = category

    if foto:
        # Hapus foto lama
        if menu.foto:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], menu.foto)
            if os.path.exists(old_path):
                os.remove(old_path)

        # Buat nama file baru dari nama menu
        ext = os.path.splitext(foto.filename)[1]  # ambil ekstensi .jpg / .png
        new_filename = secure_filename(nama.replace(" ", "_") + ext)

        # Simpan file baru
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        menu.foto = new_filename

    db.session.commit()
    return jsonify({'message': 'Menu berhasil diperbarui'})

@app.route('/menus/<int:id>', methods=['DELETE'])
def delete_menu(id):
    menu = db.session.get(Menu, id)
    if not menu:
        return jsonify({'message': 'Menu tidak ditemukan'}), 404

    if menu.foto and menu.foto != 'default.png':
        try:
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], menu.foto)
            if os.path.exists(foto_path):
                os.remove(foto_path)
        except Exception as e:
            print(f"Error menghapus foto: {e}")

    db.session.delete(menu)
    db.session.commit()

    return jsonify({'message': 'Menu berhasil dihapus dan foto terkait telah dihapus'}), 200

# ================================
#        ORDER DETAILS VIEW
# ================================

@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders = db.session.query(Order).all()
    result = []
    for order in orders:
        items = []
        for item in order.order_items:
            items.append({
                'nama_menu': item.menu.nama,
                'quantity': item.quantity,
                'harga_satuan': item.menu.harga
            })
        result.append({
            'id': order.id,
            'nama_customer': order.customer.nama,
            'total_harga': order.total_harga,
            'metode_pembayaran': order.metode_pembayaran,
            'tanggal_pembelian': order.tanggal_pembelian.strftime('%Y-%m-%d'),
            'items': items
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
