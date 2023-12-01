import streamlit as st
from datetime import datetime, timedelta

def konfirmasi_pemesanan():
	st.title("Konfirmasi Pemesanan")
	kode_pemesanan = st.text_input("Masukkan kode pemesanan")
	if st.button("Konfirmasi"):
		if kode_pemesanan == st.session_state.kode_pemesanan:
			st.success("Pemesanan berhasil dikonfirmasi.")
		else:
			st.warning("Kode Pemesanan tidak sesuai.")

def main():
    st.set_page_config(page_title="Konfirmasi Pemesanan")
    konfirmasi_pemesanan()

if __name__ == "__main__":
	main()