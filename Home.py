import streamlit as st
import db  # Import file db.py yang baru dibuat

st.set_page_config(page_title="Si Tani", page_icon="🌱")

# Cek status login di session state
if 'user_session' not in st.session_state:
    st.session_state['user_session'] = None

# --- BAGIAN 1: BELUM LOGIN ---
if st.session_state['user_session'] is None:
    st.title("🌱 Selamat Datang di Si Tani")
    
    tab1, tab2 = st.tabs(["Login", "Daftar Akun"])
    
    with tab1:
        hp = st.text_input("Nomor HP")
        pw = st.text_input("Password", type="password")
        if st.button("Masuk"):
            user = db.login_user(hp, pw)
            if user:
                st.session_state['user_session'] = user
                st.rerun() # Refresh agar langsung masuk dashboard
            else:
                st.error("Gagal Login. Cek Nomor HP atau Password.")
                
    with tab2:
        st.write("Buat akun baru")
        reg_nama = st.text_input("Nama Lengkap")
        reg_hp = st.text_input("Nomor HP (untuk login)")
        reg_pw = st.text_input("Buat Password", type="password")
        reg_alamat = st.text_area("Alamat")
        if st.button("Daftar Sekarang"):
            sukses = db.register_user(reg_nama, reg_hp, reg_pw, reg_alamat)
            if sukses:
                st.success("Berhasil daftar! Silakan Login.")
            else:
                st.error("Gagal daftar.")

# --- BAGIAN 2: SUDAH LOGIN (DASHBOARD) ---
else:
    nama_user = st.session_state['user_session']['nama']
    st.sidebar.success(f"Login sebagai: {nama_user}")
    
    if st.sidebar.button("Logout"):
        st.session_state['user_session'] = None
        st.rerun()
        
    st.title(f"Halo, Pak/Bu {nama_user}! 👋")
    st.write("Silakan pilih menu di sebelah kiri untuk mulai:")
    
    # Menu Cards sederhana
    col1, col2 = st.columns(2)
    with col1:
        st.info("🏥 **Diagnosis Penyakit**\n\nCek kesehatan tanaman Anda.")
    with col2:
        st.success("☁️ **Konsultan Cuaca**\n\nCek ramalan cuaca hari ini.")