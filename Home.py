# File: Home.py
import streamlit as st

st.set_page_config(
    page_title="Tani-Selamat Home",
    page_icon="🌱",
)

st.title("🌱 Tani-Selamat")
st.subheader("Super App untuk Petani Cerdas")

st.markdown("""
Selamat datang di pusat komando pertanian Anda.
Silakan pilih menu di sebelah kiri:

* **🏥 Diagnosis Penyakit:** Foto tanaman sakit, AI akan mendiagnosis.
* **☁️ Konsultan Cuaca:** Dapatkan strategi bertani berdasarkan kondisi cuaca.

---
*Dibuat dengan ❤️ untuk Petani Indonesia*
""")

# Cek API Key (Global Check)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Peringatan: File .gitignore/.streamlit/secrets.toml belum ditemukan.")