import streamlit as st
from datetime import datetime, timedelta

def pemesanan():
    st.title("Pemesanan Sepeda")

    stok_sepeda = st.session_state.stok_sepeda

    if stok_sepeda > 0:
        st.write(f"Stok Sepeda Listrik yang Tersedia: {stok_sepeda}")
        
        jumlah_unit = st.number_input("Masukkan jumlah unit", 0, stok_sepeda)
        durasi = st.slider("Pilih Durasi (dalam menit):", 30, 300, 30, 30)
        jaminan = st.radio("Pilih Jaminan:", ["KTP", "KTM", "SIM"])

        total_biaya = jumlah_unit * durasi // 30 * 10000
        st.write(f"Total Biaya: Rp {total_biaya}")
        st.session_state.total_biaya = total_biaya

        metode_pembayaran = st.selectbox("Pilih metode pembayaran:", ["Cash", "Cashless"])
        if metode_pembayaran == "Cash":
            st.write("Silakan bayar kepada admin yang bertugas.")
        elif metode_pembayaran == "Cashless":
            st.write("Silakan scan QR code yang tersedia.")

        if st.button("Selesaikan Pemesanan"):
            kode_pemesanan = f"WT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            st.success(f"Pemesanan berhasil! Kode Pemesanan Anda: {kode_pemesanan}")
            st.session_state.kode_pemesanan = kode_pemesanan

def main():
    st.set_page_config(page_title="Pemesanan Sepeda Listrik")
 
    if "total_biaya" not in st.session_state:
        st.session_state.total_biaya = 0
    if "kode_pemesanan" not in st.session_state:
        st.session_state.kode_pemesanan = ""
    pemesanan()

if __name__ == "__main__":
    main()