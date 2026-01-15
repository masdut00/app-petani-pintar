import streamlit as st
from google import genai
import requests

st.set_page_config(page_title="Konsultan Cuaca Akurat", page_icon="☁️")

st.title("☁️ Konsultan Cuaca Presisi")
st.caption("Pilih lokasi spesifik agar strategi bertani akurat")

# --- FUNGSI 1: MENCARI KANDIDAT KOTA ---
def cari_kota(keyword):
    """Mencari daftar kota dengan detail Kota/Kabupaten"""
    try:
        # 1. NAIKKAN LIMIT KE 20 (Supaya Ciledug Tangerang kebagian tempat)
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={keyword}&count=20&language=id&format=json"
        response = requests.get(url).json()
        
        if not response.get('results'):
            return []
            
        opsi_kota = []
        for item in response['results']:
            nama = item.get('name')
            
            # 2. AMBIL DATA ADMIN LEBIH LENGKAP
            # admin1 = Provinsi, admin2 = Kota/Kabupaten
            provinsi = item.get('admin1', '') 
            kota_kab = item.get('admin2', '') 
            negara = item.get('country', '')
            
            # 3. LABEL LEBIH JELAS
            # Format: "Ciledug, Kota Tangerang, Banten"
            lokasi_detail = []
            if kota_kab: lokasi_detail.append(kota_kab)
            if provinsi: lokasi_detail.append(provinsi)
            
            detail_str = ", ".join(lokasi_detail)
            label_lengkap = f"{nama} ({detail_str})"
            
            opsi_kota.append({
                "label": label_lengkap,
                "lat": item['latitude'],
                "lon": item['longitude']
            })
            
        return opsi_kota
    except Exception as e:
        st.error(f"Error pencarian: {e}")
        return []

# --- FUNGSI 2: AMBIL CUACA BERDASARKAN KOORDINAT ---
def ambil_cuaca(lat, lon):
    """Mengambil data cuaca jika koordinat sudah pasti"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,wind_speed_10m&timezone=auto"
        data = requests.get(url).json()
        current = data['current']
        
        # Terjemahkan kode cuaca
        code = current['weather_code']
        kondisi = "Cerah/Berawan"
        if code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: kondisi = "Hujan"
        elif code in [95, 96, 99]: kondisi = "Badai Petir"
        
        return {
            "suhu": f"{current['temperature_2m']} °C",
            "kondisi": kondisi,
            "angin": f"{current['wind_speed_10m']} km/h"
        }
    except Exception as e:
        return None

# --- UI UTAMA ---

# Cek API Key
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.warning("⚠️ API Key belum di-setup.")
    st.stop()

# Input Pencarian
kota_input = st.text_input("📍 Ketik Nama Kecamatan/Desa", placeholder="Contoh: Ciledug")

# Menggunakan Session State untuk menyimpan hasil pencarian sementara
if "hasil_pencarian" not in st.session_state:
    st.session_state.hasil_pencarian = []

# Tombol Cari (Hanya untuk mencari nama tempat)
if st.button("🔍 Cari Lokasi"):
    if kota_input:
        with st.spinner("Mencari di peta..."):
            hasil = cari_kota(kota_input)
            if hasil:
                st.session_state.hasil_pencarian = hasil
                st.success(f"Ditemukan {len(hasil)} lokasi bernama '{kota_input}'")
            else:
                st.error("Lokasi tidak ditemukan. Coba nama kota yang lebih besar.")

# --- BAGIAN PEMILIHAN LOKASI ---
# Jika ada hasil pencarian, tampilkan Dropdown (Selectbox)
if st.session_state.hasil_pencarian:
    
    # Buat list label untuk dropdown
    pilihan_label = [item['label'] for item in st.session_state.hasil_pencarian]
    
    # User memilih salah satu
    pilihan_user = st.selectbox("Pilih lokasi yang benar:", pilihan_label)
    
    # Cari data koordinat asli berdasarkan pilihan user
    # (Teknik filter list di Python)
    lokasi_terpilih = next(item for item in st.session_state.hasil_pencarian if item['label'] == pilihan_user)
    
    st.info(f"Anda memilih: **{lokasi_terpilih['label']}**")
    
    # --- INPUT TANAMAN & ANALISIS ---
    st.markdown("---")
    st.subheader("🌱 Analisis Pertanian")
    
    c1, c2 = st.columns(2)
    with c1:
        tanaman = st.text_input("Tanaman Anda", placeholder="Contoh: Bawang Merah")
    with c2:
        fase = st.selectbox("Fase", ["Semai", "Pertumbuhan", "Berbuah", "Panen"])
        
    if st.button("🚀 Analisis Strategi Cuaca"):
        if not tanaman:
            st.warning("Isi jenis tanaman dulu.")
        else:
            # 1. Ambil Cuaca Real-time dari Koordinat Terpilih
            cuaca_now = ambil_cuaca(lokasi_terpilih['lat'], lokasi_terpilih['lon'])
            
            if cuaca_now:
                # Tampilkan Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Suhu", cuaca_now['suhu'])
                m2.metric("Kondisi", cuaca_now['kondisi'])
                m3.metric("Angin", cuaca_now['angin'])
                
                # 2. Kirim ke Gemini
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    Lokasi: {lokasi_terpilih['label']}
                    Cuaca Real-time: {cuaca_now['suhu']}, {cuaca_now['kondisi']}, Angin {cuaca_now['angin']}.
                    Tanaman: {tanaman} (Fase: {fase}).
                    
                    Berikan strategi bertani singkat dan taktis untuk kondisi ini.
                    """
                    
                    with st.spinner('Gemini sedang berpikir...'):
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error AI: {e}")