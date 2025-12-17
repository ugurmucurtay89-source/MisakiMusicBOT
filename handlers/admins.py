# Calls Music 1 - Müzik kontrol komutları
# Telif Hakkı (C) 2021 Roj Serbest
# GNU Affero Genel Kamu Lisansı v3

from asyncio.queues import QueueEmpty
from cache.admins import set
from pyrogram import Client, filters
from pyrogram.types import Message
from callsmusic import callsmusic
import traceback
import os
import sys
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.errors.exceptions.flood_420 import FloodWait
from config import BOT_NAME as BN, BOT_OWNER, SUDO_USERS
from helpers.filters import komut, diğer_filtreler
from helpers.decorators import hata_yakala, sadece_yetkili_kullanıcılar
from config import que, admins as a

@Client.on_message(filters.command('adminreset'))
@sadece_yetkili_kullanıcılar
async def yönetici_güncelle(client: Client, message: Message):
    """
    /adminreset - Yönetici listesini yeniler
    """
    global a
    try:
        yöneticiler = await client.get_chat_members(message.chat.id, filter="administrators")
        yeni_yöneticiler = [kullanıcı.user.id for kullanıcı in yöneticiler]
        a[message.chat.id] = yeni_yöneticiler
        await message.reply_text(
            f"✅ <b>Yönetici listesi güncellendi!</b>
"
            f"📊 <b>Grup:</b> {message.chat.title}
"
            f"👥 <b>Yönetici Sayısı:</b> {len(yeni_yöneticiler)}"
        )
    except Exception as e:
        await message.reply_text(f"❌ Hata: {str(e)}")

@Client.on_message(komut("pause") & diğer_filtreler)
@hata_yakala
@sadece_yetkili_kullanıcılar
async def duraklat(_, message: Message):
    """
    /pause - Müziği duraklatır
    """
    if (message.chat.id not in callsmusic.pytgcalls.active_calls or 
        callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'):
        await message.reply_text("❗ Hiçbir şey çalmıyor!")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("⏸️ <b>Müzik duraklatıldı!</b>")

@Client.on_message(komut("resume") & diğer_filtreler)
@hata_yakala
@sadece_yetkili_kullanıcılar
async def devam_et(_, message: Message):
    """
    /resume - Müziği devam ettirir
    """
    if (message.chat.id not in callsmusic.pytgcalls.active_calls or 
        callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'):
        await message.reply_text("❗ Hiçbir şey duraklatılmadı!")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("▶️ <b>Müzik devam ediyor!</b>")

@Client.on_message(komut("end") & diğer_filtreler)
@hata_yakala
@sadece_yetkili_kullanıcılar
async def durdur(_, message: Message):
    """
    /end - Müziği tamamen durdurur
    """
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ Hiçbir şey çalmıyor!")
    else:
        try:
            callsmusic.queues.clear(message.chat.id)
        except QueueEmpty:
            pass
        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text("❌ <b>Müzik durduruldu ve userbot ayrıldı!</b>")

@Client.on_message(komut("skip") & diğer_filtreler)
@hata_yakala
@sadece_yetkili_kullanıcılar
async def atla(_, message: Message):
    """
    /skip - Şarkıyı atlar
    """
    global que
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ Atlamak için bir şey çalmıyor!")
    else:
        callsmusic.queues.task_done(message.chat.id)
        
        if callsmusic.queues.is_empty(message.chat.id):
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                message.chat.id,
                callsmusic.queues.get(message.chat.id)["file"]
            )
    
    sıra = que.get(message.chat.id)
    if sıra:
        atlanan = sıra.pop(0)
        if sıra:
            şimdi_çalan = sıra[0][0]
            await message.reply_text(
                f"⏭️ <b>Atlandı:</b> {atlanan[0]}
"
                f"▶️ <b>Şimdi:</b> {şimdi_çalan}"
            )
        else:
            await message.reply_text(f"⏭️ <b>Atlandı:</b> {atlanan[0]}")

@Client.on_message(filters.command("admincache"))
@hata_yakala
async def yönetici_önbellek(client: Client, message: Message):
    """
    /admincache - Yönetici önbelleğini yeniler
    """
    try:
        yöneticiler = [üyelik.user for üyelik in await message.chat.get_members(filter="administrators")]
        set(message.chat.id, yöneticiler)
        await message.reply_text(
            f"✅ <b>Yönetici önbelleği yenilendi!</b>
"
            f"👑 <b>Sahip:</b> {BOT_OWNER}
"
            f"📢 <b>Grup:</b> {message.chat.title}"
        )
    except Exception as e:
        await message.reply_text(f"❌ Hata: {str(e)}")    admins = await client.get_chat_members(message.chat.id, filter="Yöneticiler")
    new_ads = []
    for u in admins:
        new_ads.append(u.user.id)
    a[message.chat.id] = new_ads
    await message.reply_text('Yönetici listesi **{}** biçiminde başarıyla güncellendi'.format(message.chat.title))




@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'
    ):
        await message.reply_text("❗ Hiçbir şey oynatılmıyor!")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("▶️ Duraklatıldı!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'
    ):
        await message.reply_text("❗ Hiçbir şey duraklatılmadı!")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("⏸ Devam Edildi!")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ streaming Hiçbir şey yayın yapmıyor!")
    else:
        try:
            callsmusic.queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text("❌ Akış durduruldu!")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ Atlamak için hiçbir şey oynatılmıyor!")
    else:
        callsmusic.queues.task_done(message.chat.id)

        if callsmusic.queues.is_empty(message.chat.id):
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                message.chat.id,
                callsmusic.queues.get(message.chat.id)["file"]
            )
                

    qeue = que.get(message.chat.id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f'- Atlandı **{skip[0]}**\n- Şimdi Oynatılıyor **{qeue[0][0]}**')


@Client.on_message(
    filters.command("admincache")
)
@errors
async def admincache(client, message: Message):
    set(message.chat.id, [member.user for member in await message.chat.get_members(filter="Yöneticiler")])
    #await message.reply_text("♪ VCPlayBot ♪=❇️ Admin cache refreshed!")
