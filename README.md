# Makan.in

[![Lisensi](https://img.shields.io/badge/Lisensi-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Deskripsi Proyek
![Uploading image.png…]()

**Makan.in** adalah aplikasi web sederhana yang dirancang untuk memfasilitasi transaksi kasir dan pengelolaan menu. Aplikasi ini memungkinkan pengguna untuk melakukan pemesanan, mencatat pembayaran, dan menghasilkan laporan transaksi. Di sisi administrasi, aplikasi ini menyediakan fitur untuk mengelola daftar menu, termasuk menambah, mengedit, dan menghapus item menu beserta detail harganya.

## Prasyarat

Sebelum menjalankan proyek ini, pastikan Anda telah menginstal perangkat lunak berikut di sistem Anda:

* **Python 3.x:** Untuk menjalankan backend dan server frontend sederhana. Anda dapat mengunduhnya dari [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **pip:** Package installer untuk Python (biasanya sudah terinstal dengan Python).
* **Git:** Untuk melakukan clone repository. Anda dapat mengunduhnya dari [https://git-scm.com/downloads](https://git-scm.com/downloads)
* **Dependensi Backend:** Proyek backend ini kemungkinan memiliki dependensi spesifik. Pastikan Anda telah menginstal semua dependensi yang diperlukan menggunakan file `requirements.txt` (jika ada).

## Instalasi dan Menjalankan Proyek

Berikut adalah langkah-langkah untuk menginstal dan menjalankan proyek **Makan.in** di lingkungan lokal Anda:

1.  **Clone Repository**

    Buka terminal atau command prompt Anda dan jalankan perintah berikut untuk meng-clone repository proyek ke komputer Anda:

    
    git clone https://github.com/charlesbarnabas/iae-warungmakan.git
    

2.  **Menjalankan Backend**

    a.  Masuk ke direktori backend proyek:

        
        cd backend
        

    b.  Jika terdapat file `requirements.txt`, instal dependensi backend terlebih dahulu:

        
        pip install -r requirements.txt
        

    c.  Jalankan service backend:

        
        python customer_order_services.py
        python menu_service.py
        

        Pastikan kedua service backend berjalan tanpa error. Anda mungkin akan melihat pesan log atau indikasi bahwa server sedang berjalan pada port tertentu.

3.  **Menjalankan Frontend**

    a.  Buka terminal atau command prompt **baru** (jangan menutup terminal yang menjalankan backend).

    b.  Masuk ke direktori frontend proyek:

        
        cd frontend
        

    c.  Jalankan server HTTP sederhana dari Python untuk melayani file frontend:

        
        python -m http.server 8000
        

        Perintah ini akan memulai server HTTP lokal pada port 8000.

    d.  Buka browser web Anda dan kunjungi alamat berikut untuk mengakses frontend **Makan.in**:

        
        http://localhost:8000
        

        Anda akan melihat antarmuka pengguna untuk transaksi kasir dan mungkin juga tautan atau area untuk akses pengelolaan menu oleh admin (tergantung implementasi frontend).

## Konfigurasi (Opsional)

Jika proyek **Makan.in** memerlukan konfigurasi tambahan (misalnya, pengaturan database, otentikasi admin, dll.), jelaskan langkah-langkah konfigurasinya di bagian ini. Sebutkan file konfigurasi yang perlu diubah dan parameter-parameter penting yang perlu diatur.

## Penggunaan

Jelaskan cara menggunakan aplikasi **Makan.in**, termasuk:

* **Transaksi Kasir:** Bagaimana pengguna melakukan pemesanan, menambahkan item ke keranjang, menghitung total, dan mencatat pembayaran.
* **Pengelolaan Menu (Admin):** Bagaimana admin dapat mengakses halaman pengelolaan menu, menambah item baru, mengedit detail item (nama, harga, deskripsi), dan menghapus item dari menu.

Berikan langkah-langkah yang jelas untuk setiap fungsi.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek **Makan.in**, silakan ikuti langkah-langkah berikut:

1.  Fork repository ini.
2.  Buat branch baru untuk fitur atau perbaikan Anda (`git checkout -b fitur-baru` atau `git checkout -b perbaikan-bug`).
3.  Lakukan perubahan dan commit perubahan Anda (`git commit -am 'Tambahkan fitur baru'`).
4.  Push ke branch Anda di fork Anda (`git push origin fitur-baru`).
5.  Buat Pull Request ke branch `main` (atau `master`) dari repository ini.

Harap ikuti pedoman kontribusi jika ada.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detailnya.

## Kontak

Jika Anda memiliki pertanyaan atau umpan balik tentang **Makan.in**, jangan ragu untuk menghubungi kami melalui [alamat email Anda] atau [link ke profil media sosial Anda].

---

**Catatan:**

* Pastikan untuk mengganti `<link-repo-anda>`, detail konfigurasi, informasi kontak, dan detail lisensi dengan informasi yang sesuai untuk proyek **Makan.in** Anda.
* Jika ada dependensi backend yang spesifik, pastikan untuk mencantumkannya atau menjelaskan penggunaan file `requirements.txt`.
* Anda dapat menambahkan bagian lain seperti "Dokumentasi API", "Pengujian", atau "Deployment" jika relevan dengan proyek Anda.
* Penggunaan `python -m http.server` cocok untuk pengembangan dan pengujian lokal. Untuk deployment produksi, Anda mungkin memerlukan server web yang lebih robust seperti Nginx atau Apache.
