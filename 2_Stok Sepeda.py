import streamlit as st 

def update_stok():
    stok_sepeda = 0
    tambahan = st.number_input("Masukkan jumlah sepeda yang akan ditambahkan", 0)
    stok_sepeda += tambahan
    st.session_state.stok_sepeda = stok_sepeda
    if st.button("Perbarui stok sepeda"):
        st.success(f"Stok sepeda berhasil ditambahkan. Stok sepeda saat ini: {st.session_state.stok_sepeda}")
    return stok_sepeda

def main():
    st.set_page_config(page_title="Stok Sepeda")
 
    if "stok_sepeda" not in st.session_state:
        st.session_state.stok_sepeda = 0
    update_stok()

if __name__ == "__main__":
	main()