# Calls Music 1 - Telegram Grup Sesli Sohbet Müzik Botu
# Telif Hakkı (C) 2025 Cumhurbaşkanı uraz
# Inukaasith tarafından düzenlendi

from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Global değişkenler (sıra bekleyen şarkılar)
que = {}

# Oturum adı (kullanıcı hesabı için) - VERDİĞİN DEĞER
SESSION_NAME = "@Cumhurbbaskani"

# Bot bilgileri (zorunlu) - VERDİĞİN TOKEN
BOT_TOKEN = "8567616568:AAEaJh29GcTwv_Gq4U6AAAiUcp7VdnXdx-I"
BOT_NAME = "Uraz Müzik Botu"

# Yönetici listesi
admins = {}

# Telegram API bilgileri (zorunlu) - VERDİĞİN DEĞERLER
API_ID = 33818253
API_HASH = "22a4a51c2bd3799fdde7226fc112e6d6"

# Maksimum şarkı süresi (dakika) - 10 DAKİKA YAPILDI
DURATION_LIMIT = 10

# Komut ön ekleri
COMMAND_PREFIXES = ["/", "!"]

# Süper kullanıcılar (bot adminleri) - SENİN TELEGRAM ID'N
SUDO_USERS = [916150666]

print("🎵 Calls Music Bot yapılandırması yüklendi!")
print(f"📱 Bot: {BOT_NAME}")
print(f"👤 Session: {SESSION_NAME}")
print(f"⏱️ Maksimum süre: {DURATION_LIMIT} dakika")
print(f"👑 Admin: {SUDO_USERS}")
print("✅ HAZIR - Ana bot dosyasını çalıştırın!")
