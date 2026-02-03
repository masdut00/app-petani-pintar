import requests
import datetime
import uuid

# GANTI DENGAN URL APPS SCRIPT KAMU SENDIRI
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyMQzRrTlR0QPe9k61RtrwVwtQQrfoe3nRVFIZhf0MkiiTitpNaEDBLnBw0eBXRzklw/exec"

def login_user(no_hp, password):
    payload = {
        "nama_sheet": "users",
        "aksi": "login",
        "cari_hp": no_hp,
        "cari_pass": password
    }
    try:
        response = requests.post(APPS_SCRIPT_URL, json=payload)
        hasil = response.text
        if "LOGIN_SUKSES" in hasil:
            return {"nama": hasil.split("|")[1], "no_hp": no_hp}
        return None
    except:
        return None

def register_user(nama, no_hp, password, alamat):
    user_id = str(uuid.uuid4())[:8]
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "nama_sheet": "users",
        "aksi": "tambah",
        "isi_baris": [ts, user_id, no_hp, password, nama, alamat]
    }
    try:
        requests.post(APPS_SCRIPT_URL, json=payload)
        return True
    except:
        return False