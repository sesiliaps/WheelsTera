import streamlit as st
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("file:wheelstera.db?mode=rwc")
cursor = conn.cursor()

#Fungsi untuk membuat tabel data user
def create_users_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, username TEXT UNIQUE, password TEXT, nama TEXT, no_hp TEXT, nik TEXT, nim TEXT, prodi TEXT)")

#Fungsi untuk membuat tabel data admin
def create_admins_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,username TEXT UNIQUE,password TEXT,nama TEXT)")

    cursor.execute("SELECT id FROM admin LIMIT 1")
    result = cursor.fetchone()
    if result:
        admin_id = result[0]

#Fungsi untuk membuat tabel data pesanan
def create_pesanan_table():
  cursor.execute("CREATE TABLE IF NOT EXISTS pesanan (id INTEGER PRIMARY KEY AUTOINCREMENT,kode_pemesanan TEXT UNIQUE,durasi TEXT,jaminan TEXT,total_biaya INTEGER,status TEXT,user_id INTEGER,FOREIGN KEY (user_id) REFERENCES users (id))")

#Fungsi untuk input data register user
def add_userdata(email, username, password, nama, no_hp, nik, nim, prodi):
    cursor.execute('INSERT INTO users (email, username, password, nama, no_hp, nik, nim, prodi) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (email, username, password, nama, no_hp, nik, nim, prodi))
    conn.commit()
    st.success("Registrasi pengguna berhasil. Silakan Login.")

#Fungsi untuk input data register admin
def add_admindata(email, username, password, nama):
    cursor.execute('INSERT INTO admin (email, username, password, nama) VALUES (?, ?, ?, ?)', (email, username, password, nama))
    conn.commit()
    st.success("Registrasi admin berhasil. Silakan Login.")

#Fungsi Login user
def login_users(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user_data = cursor.fetchone()
    return user_data

#Fungsi Login admin
def login_admin(username, password):
    cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
    admin_data = cursor.fetchone()
    return admin_data

#Fungsi logout
def logout():
    st.success("Berhasil logout.")
    st.stop

#Fungsi untuk mendapatkan data pengguna berdasarkan ID
def get_user_by_id(user_id):
    conn = sqlite3.connect("file:wheelstera.db?mode=rwc")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

#Fungsi untuk mendapatkan data pesanan berdasarkan user ID
def get_orders_by_user_id(user_id):
    conn = sqlite3.connect("file:wheelstera.db?mode=rwc")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pesanan WHERE user_id=?", (user_id,))
    pesanan_data = cursor.fetchone()
    conn.close()
    return pesanan_data

#Fungsi untuk mendapatkan data admin berdasarkan ID
def get_admin_by_id(admin_id):
    conn = sqlite3.connect("file:wheelstera.db?mode=rwc")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE id=?", (admin_id,))
    admin_data = cursor.fetchone()
    conn.close()
    return admin_data

#Fungsi untuk konfirmasi pemesanan
def konfirmasi_pemesanan(admin_id, kode_pemesanan):
    if st.button("Konfirmasi Pemesanan"):
        cursor.execute("UPDATE pesanan SET status='Sedang Berjalan' WHERE kode_pemesanan=?", (kode_pemesanan,))
        conn.commit()
        st.success(f"Pemesanan dengan kode {kode_pemesanan} telah dikonfirmasi.")

#Fungsi untuk menyelesaikan pemesanan
def selesaikan_pemesanan(admin_id, user_id, kode_pemesanan):
    if st.button("Konfirmasi Pemesanan"):
        cursor.execute("UPDATE pesanan SET status='Selesai' WHERE kode_pemesanan=?", (kode_pemesanan,))
        conn.commit()
        st.info(f"Pemesanan dengan kode {kode_pemesanan} telah diselesaikan.")

#Fungsi untuk membuat lama profile user
def profile_user(user_id):
    st.title("Profile User")
    st.button("Back", on_click=dashboard_user, args=(user_id,))

    user_data = get_user_by_id(user_id)
    st.subheader("Data Diri")
    st.write(f"Email:{user_data[1]}")
    st.write(f"Username: {user_data[2]}")
    st.write(f"Nama: {user_data[4]}")
    st.write(f"No HP: {user_data[5]}")
    st.write(f"NIK: {user_data[6]}")
    st.write(f"NIM: {user_data[7]}")
    st.write(f"Prodi: {user_data[8]}")

#Fungsi untuk melakukan pemesanan
def pemesanan():
    st.title("Pemesanan Sepeda")
    st.info("Silakan beralih ke halaman pemesanan.")

#Fungsi untuk membuat page home admin
def home_admin(admin_id):
    st.title("Halaman Home Admin")
    st.button("Back", on_click=dashboard_admin, args=(admin_id,))

    st.subheader("Stok Sepeda")
    st.info("Silakan beralih ke laman stok sepeda.")

    st.subheader("Konfirmasi Pemesanan")
    st.info("Silakan beralih ke laman konfirmasi pemesanan")

#Fungsi untuk membuat page profile admin
def profile_admin(admin_id):
    st.title("Halaman Profile Admin")
    st.button("Back", on_click=dashboard_admin, args=(admin_id,))

    #Menampilkan data diri admin
    admin_data = get_admin_by_id(admin_id)
    st.subheader("Data Diri")
    st.write(f"Email:{admin_data[1]}")
    st.write(f"Username: {admin_data[2]}")
    st.write(f"Nama: {admin_data[4]}")

    #Menampilkan pendapatan hari ini
    pendapatan = 0
    pendapatan = pendapatan + st.session_state.total_biaya 
    st.subheader("Pendapatan")
    st.info(f"Total pendapatan hari ini: {pendapatan}")

#Fungsi Dashboard User
def dashboard_user(user_id):
    st.title("Dashboard User")

    st.button("Profile", on_click = profile_user, args=(user_id,))
    st.button("Pemesanan", on_click = pemesanan)
    st.button("Logout", on_click = logout)

#Fungsi Dashboard Admin
def dashboard_admin(admin_id):
    st.title("Dashboard Admin")

    st.button("Home", on_click=home_admin, args=(admin_id,))
    st.button("Profile", on_click=profile_admin, args=(admin_id,))
    st.button("Logout", on_click = logout)

#Fungsi utama
def main():

    st.set_page_config(
        page_title="WheeslTera App")
 
    create_users_table()
    create_admins_table()
    create_pesanan_table()

    role = st.sidebar.selectbox("Role", ["User", "Admin"])

    if role == "User":
        menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

        if menu == "Login":
            st.sidebar.subheader("Login")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type='password')

            if st.sidebar.button("Login"):
                create_users_table()
                result = login_users(username, password)

                if result:
                    st.success("Berhasil login. Selamat datang, {}".format(username))
                    st.button("Halaman User", on_click = dashboard_user, args=(result[0],))
                else:
                    st.error("Login gagal. Silakan masukkan kembali username dan password yang sesuai.")

        elif menu == "Register":
            st.sidebar.subheader("Register")
            email = st.sidebar.text_input("Email")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type='password')
            nama = st.sidebar.text_input("Nama")
            no_hp = st.sidebar.text_input("Nomor HP")
            nik = st.sidebar.text_input("Nomor Induk Kependudukan")
            nim = st.sidebar.text_input("Nomor Induk Mahasiswa")
            prodi = st.sidebar.text_input("Program Studi")

            if st.sidebar.button("Daftar"):
                create_users_table()
                add_userdata(email, username, password, nama, no_hp, nik, nim, prodi)

    elif role == "Admin":
        menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

        if menu == "Login":
            st.sidebar.subheader("Login")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type='password')

            if st.sidebar.button("Login"):
                create_admins_table()
                result = login_admin(username, password)

                if result:
                    st.success("Berhasil login. Selamat datang, {}".format(username))
                    st.button("Halaman Admin", on_click=dashboard_admin, args=(result[0],))
                else:
                    st.error("Login gagal. Silakan masukkan kembali username dan password yang sesuai.")

        elif menu == "Register":
            st.sidebar.subheader("Register")
            email = st.sidebar.text_input("Email")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            nama = st.sidebar.text_input("Nama")

            if st.sidebar.button("Daftar"):
                create_admins_table()
                add_admindata(email, username, password, nama)

if __name__ == "__main__":
    main()