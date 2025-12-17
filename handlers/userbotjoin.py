# ZauteMusic - Userbot join/leave komutları
# Telif Hakkı (C) 2021 ZauteKm
# GNU Affero Genel Kamu Lisansı v3

from callsmusic.callsmusic import client as USER
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from helpers.decorators import hata_yakala, sadece_yetkili_kullanıcılar
from config import BOT_OWNER

@Client.on_message(filters.group & filters.command(["userbotjoin"]))
@sadece_yetkili_kullanıcılar
@hata_yakala
async def userbot_katil(client: Client, message: Message):
    """
    /userbotjoin - Userbot'u gruba çağırır (sadece adminler)
    """
    chat_id = message.chat.id
    
    # Davet linki oluştur
    try:
        davet_linki = await client.export_chat_invite_link(chat_id)
    except:
        await message.reply_text(
            "❌ <b>Önce beni grubun <u>yöneticisi</u> yapın!</b>"
        )
        return

    # Userbot bilgilerini al
    try:
        userbot_bilgi = await USER.get_me()
    except:
        userbot_bilgi = type('obj', (object,), {'first_name': '@Spotifymuzikk_bot'})()

    # Userbot'u gruba davet et
    try:
        await USER.join_chat(davet_linki)
        await USER.send_message(
            message.chat.id, 
            f"🎵 <b>Merhaba! @Spotifymuzikk_bot olarak katıldım!</b>

"
            f"👑 <b>Sahip:</b> {BOT_OWNER}
"
            f"🎶 <code>/play şarkı adı</code> ile müzik çalabiliriz!"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            "✅ <b>@Spotifymuzikk_bot zaten grupta!</b>"
        )
        return
    except Exception as e:
        print(f"Userbot join hatası: {e}")
        await message.reply_text(
            f"❌ <b>@Spotifymuzikk_bot gruba katılamadı!</b>

"
            f"🔍 <b>Olası sebepler:</b>
"
            f"• @Spotifymuzikk_bot grupta yasaklanmış
"
            f"• FloodWait (bekleme) hatası

"
            f"👉 <b>Çözüm:</b> Userbot'u manuel ekleyin!"
        )
        return
    
    await message.reply_text(
        f"✅ <b>@Spotifymuzikk_bot başarıyla katıldı!</b>
"
        f"🎵 Artık <code>/play</code> komutu çalışır!"
    )

@USER.on_message(filters.group & filters.command(["userbotleave"]))
async def userbot_ayril(USER, message: Message):
    """
    /userbotleave - Userbot'u gruptan çıkarır
    """
    try:
        await USER.leave_chat(message.chat.id)
        await message.reply_text(
            "✅ <b>@Spotifymuzikk_bot gruptan ayrıldı!</b>"
        )
    except Exception as e:
        await message.reply_text(
            f"❌ <b>@Spotifymuzikk_bot gruptan ayrılamadı!</b>

"
            f"🔧 <b>Çözüm:</b>
"
            f"• Manuel olarak gruptan atın
"
            f"• FloodWait olabilir, bekleyin"
        )
        print(f"Userbot leave hatası: {e}")
