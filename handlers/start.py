# ZauteMusic - Telegram grup sesli sohbet müzik botu
# Telif Hakkı (C) 2021 ZauteKm
# GNU Affero Genel Kamu Lisansı v3

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn, BOT_OWNER


@Client.on_message(
    filters.command("start")
    & filters.private
    & ~filters.edited
)
async def baslat_ozel(client: Client, message: Message):
    """
    Özel mesajda /start komutu - Bot tanıtımı ve butonlar
    """
    await message.reply_text(
        f"""👋 <b>Hoş geldiniz {message.from_user.first_name}!</b>

🎵 <b>{BOT_NAME}</b> grup sesli sohbetlerinizde müzik çalmak için tasarlanmış basit bir bot!

❓ <b>Nasıl kullanılır?</b>
Komut listesi için <b>/help</b> yazın veya butonlara basın!""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton("➕ Beni Grubunuza Ekleyin ➕", url=f"t.me/{bn}?startgroup=true")
                ],
                [
                    InlineKeyboardButton("📋 Komutlar", callback_data="help"),
                    InlineKeyboardButton("👑 Sahip", url="https://t.me/Cumhurbbaskani")
                ],
                [
                    InlineKeyboardButton("📢 Müzik Destek", url="https://t.me/muzikkdestekk"),
                    InlineKeyboardButton("🌐 Netinternet", url="https://t.me/Netinternet20")
                ],
                [
                    InlineKeyboardButton("📶 Sınırsız İnternet", url="https://t.me/sinirsizinternet63"),
                    InlineKeyboardButton("⭐ BlackSky Sohbet", url="https://t.me/BlackSkySohbett")
                ],
                [ 
                    InlineKeyboardButton("👑 @Cumhurbbaskani 👑", url="https://t.me/Cumhurbbaskani")
                ]
            ]
        ),
        disable_web_page_preview=True
    )


@Client.on_message(
    filters.command("start")
    & filters.group
    & ~filters.edited
)
async def baslat_grup(client: Client, message: Message):
    """
    Grup mesajında /start - Hızlı müzik arama önerisi
    """
    await message.reply_text(
        "🎵 <b>YouTube'dan şarkı mı aramak istiyorsunuz?</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👑 @Cumhurbbaskani", url="https://t.me/Cumhurbbaskani")
                ],    
                [    
                    InlineKeyboardButton("✅ Evet", switch_inline_query_current_chat=""),
                    InlineKeyboardButton("❌ Hayır", callback_data="close")
                ],
                [
                    InlineKeyboardButton("📢 Müzik Destek", url="https://t.me/muzikkdestekk")
                ]
            ]
        )
    )


@Client.on_message(
    filters.command("help")
    & filters.private
    & ~filters.edited
)
async def yardim(client: Client, message: Message):
    """
    /help komutu - Tüm komut listesi
    """
    await message.reply_text(
        f"""📋 <b>TÜM KOMUTLAR</b>

🎶 <b>Müzik Komutları:</b>
• <code>/play şarkı adı</code> - Şarkı çal
• <code>/playlist</code> - Çalma listesi göster
• <code>/current</code> - Şu an çalan şarkı

⏯️ <b>Yönetici Komutları:</b>
• <code>/player</code> - Müzik paneli
• <code>/pause</code> - Duraklat
• <code>/resume</code> - Devam et
• <code>/skip</code> - İleri al
• <code>/end</code> - Müziği durdur

💾 <b>İndirme Komutları:</b>
• <code>/song şarkı</code> - Şarkı indir
• <code>/video şarkı</code> - Video indir

👑 <b>Bot Sahibi:</b> {BOT_OWNER}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👑 @Cumhurbbaskani", url="https://t.me/Cumhurbbaskani")
                ],
                [
                    InlineKeyboardButton("📢 Müzik Destek", url="https://t.me/muzikkdestekk"),
                    InlineKeyboardButton("🌐 Netinternet", url="https://t.me/Netinternet20")
                ]
            ]
        )
    )
<b>❓ Nasıl kullanılır?</b>
botun komutlarının tam listesini görmek için! » 🎛 <b>Komutlar</b> düğmesine ve Hits /help düğmesine basın <b>GoodVibesMusic!</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Beni Grubunuza Ekleyin ➕", url="t.me/MisakiMusicbot?startgroup=true")
                  ],[
                    InlineKeyboardButton(
                        "🎛️ Komutlar", url="/play (ŞARKI İSMİ)"
                    ),
                    InlineKeyboardButton(
                        "👑Sahibim👑", url="https://t.me/ByMisakiMey")
                    ],[
                    InlineKeyboardButton(
                        "Ana kanalımız", url="https://t.me/MisakiDev"
                    ),
                    InlineKeyboardButton(
                        "Assistanım🎼", url="https://t.me/GoodVibeesMusic"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "👑Bodrumlu👑", url="https://t.me/kucukadmin"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(
    filters.command("start")
    & filters.group
    & ~ filters.edited
)
async def start(client: Client, message: Message):
    await message.reply_text(
        "💁🏻‍♂️ <b>Bir YouTube videosu mu aramak istiyorsunuz?</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Ana Kanalım🎵", url="https://t.me/MisakiDev"
                    )
                ],    
                [    
                    InlineKeyboardButton(
                        "✅ Evet", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "❌ Hayır", callback_data="close"
                    )
                ]
            ]
        )
    )

@Client.on_message(
    filters.command("help")
    & filters.private
    & ~ filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b><u>Yararlı Komutlar!</u>
\n/play <song name> - istediğiniz şarkıyı çalın
/dplay <song name> - deezer aracılığıyla istediğiniz şarkıyı çalın
/splay <song name> - jio saavn aracılığıyla istediğiniz şarkıyı çalın
/playlist - Şimdi çalma listesini göster
/current - Şimdi çalan göster
/song <song name> - istediğiniz şarkıları hızlı bir şekilde indirin
/search <query> - youtube'daki videoları ayrıntılarla arayın
/deezer <song name> - istediğiniz şarkıları deezer ile hızlıca indirin
/saavn <song name> - istediğiniz şarkıları saavn aracılığıyla hızlıca indirin
/video <song name> - istediğiniz videoları hızlı bir şekilde indirin
\n<u>Yalnızca yöneticiler</u>
/player - müzik çalar ayarları panelini aç
/pause - şarkı çalmayı duraklatır
/resume - şarkıyı çalmaya devam et
/skip - sonraki şarkıyı çal
/end - müzik çalmayı durdur
/userbotjoin - asistanı sohbetinize davet edin
/admincache - Yönetici listesini yeniler
 </b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Ana Kanalım🎵", url="https://t.me/MisakiDev"
                    )
                ]
            ]
        )
    )    
