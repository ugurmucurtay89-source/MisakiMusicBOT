import asyncio
from pyrogram import Client

print("🎵 Calls Music Bot - SESSION STRING OLUŞTURUCU")
print("👑 Bot Sahibi: @Cumhurbbaskani")
print("=" * 50)

async def main():
    # Senin verdiğin bilgiler otomatik yüklendi!
    async with Client(
        "@Cumhurbbaskani", 
        api_id=33818253, 
        api_hash="22a4a51c2bd3799fdde7226fc112e6d6"
    ) as app:
        print("📱 Telefon numaranı gir (userbot için):")
        print("✅ Session STRING OLUŞTURULUYOR...")
        
        session_string = await app.export_session_string()
        print("
🎉 SESSION STRING HAZIR!")
        print("=" * 50)
        print(f"SESSION_NAME={session_string}")
        print("=" * 50)
        print("📝 Bu string'i config.py'ye kopyala!")

if __name__ == "__main__":
    asyncio.run(main())
