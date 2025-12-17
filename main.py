from pyrogram import Client as Bot, Client as Userbot
from callsmusic import run
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME

BOT_OWNER = "@Cumhurbbaskani"  # Bot Sahibi

# Bot hesabı (mesajlar ve komutlar için)
bot = Bot(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)

# Userbot hesabı (sesli sohbet için - ZORUNLU)
userbot = Userbot(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True
)

print("🎵 Calls Music Bot BAŞLIYOR...")
print(f"👑 Bot Sahibi: {BOT_OWNER}")
print("📱 Bot token yüklendi")
print("👤 Userbot session yüklendi")

# İkisini de başlat
bot.start()
userbot.start()

print("✅ BOT VE USERBOT AKTİF!")
print(f"👑 Sahip: {BOT_OWNER}")
print("🎶 Grup sesli sohbete katıl: /play şarkı adı")
print("🔄 Bot sonsuza kadar çalışacak...")

# CallsMusic motorunu başlat
run()
