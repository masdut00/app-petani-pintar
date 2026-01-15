import streamlit as st
from google import genai
from PIL import Image

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Tani-Selamat 2.5", page_icon="🌱", layout="wide")

# --- CSS SAYA HAPUS AGAR AMAN DI DARK MODE ---

st.title("🌱 Tani-Selamat (v2.5)")
st.caption("Didukung oleh Gemini 2.5 Flash")

# 2. OTOMATIS AMBIL API KEY
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.warning("⚠️ File .streamlit/secrets.toml belum dibuat.")
    api_key = st.text_input("Google API Key:", type="password")

# 3. INISIALISASI SESSION STATE
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "diagnosis_done" not in st.session_state:
    st.session_state.diagnosis_done = False
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# Sidebar
with st.sidebar:
    if st.button("🗑️ Reset Konsultasi"):
        st.session_state.chat_history = []
        st.session_state.diagnosis_done = False
        st.session_state.current_image = None
        st.rerun()

# 4. AREA UPLOAD
uploaded_file = st.file_uploader("📸 Upload Foto Tanaman Sakit", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.session_state.current_image = image
    st.image(image, caption="Pasien Tanaman", width=350)

    # TOMBOL DIAGNOSIS
    if not st.session_state.diagnosis_done:
        if st.button("🚀 Diagnosis dengan Gemini 2.5"):
            if not api_key:
                st.error("API Key error!")
            else:
                try:
                    client = genai.Client(api_key=api_key)
                    
                    with st.spinner('Sedang menganalisis struktur daun...'):
                        prompt_awal = """
                        Kamu adalah Dokter Tanaman Profesional.
                        Analisis gambar ini dengan teliti. Berikan output:
                        1. **Penjelasan Tanaman**: (Nama Tanaman)
                        2. **Diagnosis Utama**: (Nama Penyakit)
                        3. **Penyebab**: (Kenapa bisa begini?)
                        4. **Solusi Organik**: (Bahan alami)
                        5. **Solusi Kimia**: (Opsi terakhir)
                        6. **Kesimpulan Dari Tanaman**
                        
                        Gunakan bahasa Indonesia yang mudah dimengerti petani desa.
                        """
                        
                        response = client.models.generate_content(
                            model="gemini-2.5-flash", 
                            contents=[prompt_awal, image]
                        )
                        
                        st.session_state.chat_history.append({"role": "assistant", "text": response.text})
                        st.session_state.diagnosis_done = True
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error Koneksi: {e}")

# 5. FITUR CHAT
if st.session_state.diagnosis_done:
    st.divider()
    st.subheader("💬 Konsultasi Lanjutan")

    for chat in st.session_state.chat_history:
        role_icon = "👨‍🌾" if chat["role"] == "user" else "🤖"
        
        with st.chat_message(chat["role"], avatar=role_icon):
            st.markdown(chat["text"])

    # Input User
    user_input = st.chat_input("Tanya lagi... (Contoh: Obatnya beli dimana?)")
    
    if user_input:
        if not api_key:
            st.error("API Key error.")
        else:
            with st.chat_message("user", avatar="👨‍🌾"):
                st.markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "text": user_input})

            try:
                client = genai.Client(api_key=api_key)
                
                chat_context = f"User bertanya tentang diagnosis sebelumnya: '{user_input}'. Jawab to the point."
                
                with st.spinner('Mengetik...'):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[chat_context, st.session_state.current_image]
                    )
                
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(response.text)
                
                st.session_state.chat_history.append({"role": "assistant", "text": response.text})

            except Exception as e:
                st.error(f"Gagal membalas: {e}")