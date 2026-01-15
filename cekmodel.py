from google import genai

# JANGAN LUPA ISI API KEY
client = genai.Client(api_key="AIzaSyBRz6-kdlwN1ufitLtFqDSz8u_PiQNwPdM")

print("🔍 Mengambil semua daftar model tanpa filter...")

try:
    # Ambil list model
    pager = client.models.list()
    
    for model in pager:
        # Kita print nama modelnya saja
        # Biasanya formatnya: "models/nama-model"
        print(f"NAMA: {model.name}")

except Exception as e:
    print(f"\n❌ Error: {e}")