from google import genai

# --- PENTING: GANTI INI DENGAN KODE API KEY KAMU ---
MY_API_KEY = "AIzaSyBRz6-kdlwN1ufitLtFqDSz8u_PiQNwPdM" 

try:
    # 1. Konfigurasi Client
    client = genai.Client(api_key=MY_API_KEY)
    
    print("⏳ Sedang menghubungi Dokter Tanaman...")

    # 2. Mengirim Pesan (Request)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Halo, saya petani pemula. Berikan 1 tips singkat (maksimal 20 kata) merawat cabai."
    )

    # 3. Menampilkan Jawaban
    print("\n✅ SUKSES! JAWABAN DARI AI:")
    print(response.text)

except Exception as e:
    print(f"\n❌ Masih ada error: {e}")