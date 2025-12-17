# ZauteMusic - Telegram müzik indirme botu
# Telif Hakkı (C) 2021 ZauteKm
# GNU Affero Genel Kamu Lisansı v3

from __future__ import unicode_literals
import os
import requests
import aiohttp
import youtube_dl
import wget
import math
from pyrogram import filters, Client
from youtube_search import YoutubeSearch
from Python_ARQ import ARQ
from urllib.parse import urlparse
import aiofiles
import random
from youtubesearchpython import SearchVideos
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Chat, Message, User
import asyncio
from typing import Callable, Coroutine, Dict, List, Tuple, Union
import sys
import time
from helpers.errors import DurationLimitError
from config import BOT_OWNER, DURATION_LIMIT

@Client.on_message(filters.command('song') & ~filters.channel)
async def sarkı_indir(client: Client, message: Message):
    """
    /song komutu - YouTube'dan şarkı indirir
    """
    kullanıcı_id = message.from_user.id 
    kullanıcı_adı = message.from_user.first_name 
    rpk = f"[{kullanıcı_adı}](tg://user?id={kullanıcı_id})"

    sorgu = ' '.join(message.command[1:])
    print(f"🔎 Şarkı aranıyor: {sorgu}")
    
    m = await message.reply('🔎 Şarkı bulunuyor...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    
    try:
        sonuçlar = YoutubeSearch(sorgu, max_results=1).to_dict()
        link = f"https://youtube.com{sonuçlar[0]['url_suffix']}"
        başlık = sonuçlar[0]["title"][:40]       
        kapak = sonuçlar[0]["thumbnails"][0]
        kapak_adı = f'kapak{başlık}.jpg'
        kapak_resim = requests.get(kapak, allow_redirects=True)
        with open(kapak_adı, 'wb') as f:
            f.write(kapak_resim.content)

        süre = sonuçlar[0]["duration"]
        izlenme = sonuçlar[0]["views"]

    except Exception as e:
        await m.edit("❌ Hiçbir şey bulunamadı.
Başka bir anahtar kelime deneyin!")
        print(f"Hata: {e}")
        return
    
    await m.edit("📥 Şarkı indiriliyor...")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            ses_dosyası = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        
        rep = f'**🎵 İndiren: {BOT_OWNER}**'
        await message.reply_audio(
            ses_dosyası, 
            caption=rep, 
            thumb=kapak_adı, 
            parse_mode='md', 
            title=başlık, 
            duration=time_to_seconds(süre)
        )
        await m.delete()
        
    except Exception as e:
        await m.edit('❌ İndirme hatası!')
        print(e)

    # Dosyaları temizle
    try:
        os.remove(ses_dosyası)
        os.remove(kapak_adı)
    except:
        pass

# ARQ API (Müzik servisleri için)
ARQ_API = "http://35.240.133.234:8000"
arq = ARQ(ARQ_API)

def metin_al(mesaj: Message) -> str:
    """Mesajdan sorgu metni alır"""
    if not mesaj.text:
        return None
    if " " in mesaj.text:
        try:
            return mesaj.text.split(None, 1)[1]
        except IndexError:
            return None
    return None

def boyut_insan_okur(boyut):
    """Baytları KB/MB/GB yapar"""
    if not boyut: return ""
    güç = 2 ** 10
    kat = 0
    birimler = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while boyut > güç:
        boyut /= güç
        kat += 1
    return f"{round(boyut, 2)} {birimler[kat]}B"

async def ilerleme(current, total, mesaj, baslangic, tur, dosya_adi=None):
    """İndirme ilerlemesini gösterir"""
    şimdi = time.time()
    fark = şimdi - baslangic
    if round(fark % 10.00) == 0 or current == total:
        yüzde = current * 100 / total
        hız = current / fark
        gecen_zaman = round(fark) * 1000
        if gecen_zaman == 0: return
        
        bitis_zamani = round((total - current) / hız) * 1000
        tahmini_toplam = gecen_zaman + bitis_zamani
        
        ilerleme_cizgisi = "{0}{1} {2}%".format(
            "🔴" * math.floor(yüzde / 10),
            "🔘" * (10 - math.floor(yüzde / 10)),
            round(yüzde, 2)
        )
        tmp = f"{ilerleme_cizgisi}
{boyut_insan_okur(current)} / {boyut_insan_okur(total)}
Kalan: {zaman_formatla(tahmini_toplam)}"
        
        if dosya_adi:
            try:
                await mesaj.edit(f"{tur}
**Dosya:** `{dosya_adi}`
{tmp}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
        else:
            try:
                await mesaj.edit(f"{tur}
{tmp}")
            except FloodWait as e:
                await asyncio.sleep(e.x)

def zaman_formatla(milisaniye: int) -> str:
    """Milisaniyeyi okunur zamana çevirir"""
    saniye, milisaniye = divmod(int(milisaniye), 1000)
    dakika, saniye = divmod(saniye, 60)
    saat, dakika = divmod(dakika, 60)
    gün, saat = divmod(saat, 24)
    tmp = (
        (f"{gün} gün, " if gün else "") +
        (f"{saat} saat, " if saat else "") +
        (f"{dakika} dakika, " if dakika else "") +
        (f"{saniye} saniye" if saniye else "")
    )
    return tmp[:-2]

def saniyeye_cevir(zaman):
    """HH:MM:SS'yi saniyeye çevirir"""
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(zaman).split(':'))))

# YouTube indirme ayarları
ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}

async def sarkı_indir_url(url):
    """URL'den şarkı indirir"""
    dosya_adi = f"{random.randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as oturum:
        async with oturum.get(url) as yanıt:
            if yanıt.status == 200:
                async with aiofiles.open(dosya_adi, mode='wb') as f:
                    await f.write(await yanıt.read())
    return dosya_adi

indirme_durumu = False

@Client.on_message(filters.command("saavn") & ~filters.edited)
async def saavn_sarkı(_, message):
    """JioSaavn'dan şarkı indirir"""
    global indirme_durumu
    if len(message.command) < 2:
        await message.reply_text("/saavn <şarkı adı> yazın!")
        return
    if indirme_durumu:
        await message.reply_text("Başka indirme devam ediyor!")
        return
    
    indirme_durumu = True
    sorgu = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("🔎 Aranıyor...")
    
    try:
        şarkılar = await arq.saavn(sorgu)
        şarkı_adi = şarkılar[0].song
        link = şarkılar[0].media_url
        sanatçı = şarkılar[0].singers
        
        await m.edit("📥 İndiriliyor...")
        dosya = await sarkı_indir_url(link)
        await m.edit("⬆️ Yükleniyor...")
        
        await message.reply_audio(
            audio=dosya, 
            title=şarkı_adi,
            performer=sanatçı
        )
        os.remove(dosya)
        await m.delete()
        
    except Exception as e:
        await m.edit(f"❌ Hata: {str(e)}")
    finally:
        indirme_durumu = False

@Client.on_message(filters.command("deezer") & ~filters.edited)
async def deezer_sarkı(_, message):
    """Deezer'dan şarkı indirir"""
    global indirme_durumu
    if len(message.command) < 2:
        await message.reply_text("/deezer <şarkı adı> yazın!")
        return
    if indirme_durumu:
        await message.reply_text("Başka indirme devam ediyor!")
        return
    
    indirme_durumu = True
    sorgu = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("🔎 Aranıyor...")
    
    try:
        şarkılar = await arq.deezer(sorgu, 1)
        başlık = şarkılar[0].title
        link = şarkılar[0].url
        sanatçı = şarkılar[0].artist
        
        await m.edit("📥 İndiriliyor...")
        dosya = await sarkı_indir_url(link)
        await m.edit("⬆️ Yükleniyor...")
        
        await message.reply_audio(
            audio=dosya, 
            title=başlık,
            performer=sanatçı
        )
        os.remove(dosya)
        await m.delete()
        
    except Exception as e:
        await m.edit(f"❌ Hata: {str(e)}")
    finally:
        indirme_durumu = False

@Client.on_message(filters.command(["vsong", "video"]))
async def video_indir(client: Client, message: Message):
    """Video indirir (/vsong veya /video)"""
    global indirme_durumu
    if indirme_durumu:
        await message.reply_text("Başka indirme devam ediyor!")
        return

    sorgu = metin_al(message)
    pablo = await client.send_message(
        message.chat.id,
        f"`YouTube'dan '{sorgu}' alınıyor...`"
    )
    
    if not sorgu:
        await pablo.edit("❌ Geçersiz komut!")
        return
    
    arama = SearchVideos(sorgu, offset=1, mode="dict", max_results=1)
    sonuç = arama.result()["search_result"][0]
    video_link = sonuç["link"]
    başlık = sonuç["title"]
    kanal = sonuç["channel"]
    video_id = sonuç["id"]
    kapak_link = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    await asyncio.sleep(0.6)
    kapak = wget.download(kapak_link)
    
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "quiet": True,
    }
    
    try:
        indirme_durumu = True
        with youtube_dl.YoutubeDL(opts) as ytdl:
            info = ytdl.extract_info(video_link, False)
            süre = round(info["duration"] / 60)

            if süre > DURATION_LIMIT:
                await pablo.edit(f"❌ {DURATION_LIMIT} dakikadan uzun videolara izin yok!")
                indirme_durumu = False
                return
                
            ytdl_data = ytdl.extract_info(video_link, download=True)
    
    except Exception as e:
        indirme_durumu = False
        return
    
    dosya_adi = f"{ytdl_data['id']}.mp4"
    açıklama = f"**Video:** `{başlık}`
**Sorgu:** `{sorgu}`
**Kanal:** `{kanal}`
**Link:** `{video_link}`"
    
    baslangic = time.time()
    await client.send_video(
        message.chat.id, 
        video=open(dosya_adi, "rb"), 
        duration=int(ytdl_data["duration"]), 
        file_name=ytdl_data["title"], 
        thumb=kapak, 
        caption=açıklama, 
        supports_streaming=True,
        progress=ilerleme,
        progress_args=(pablo, baslangic, f'`{sorgu} yükleniyor!`', dosya_adi)
    )
    
    await pablo.delete()
    indirme_durumu = False
    
    # Temizlik
    for dosya in (kapak, dosya_adi):
        if os.path.exists(dosya):
            os.remove(dosya)al:** `{kanal}`
**Link:** `{video_link}`"
    
    baslangic = time.time()
    await client.send_video(
        message.chat.id, 
        video=open(dosya_adi, "rb"), 
        duration=int(ytdl_data["duration"]), 
        file_name=ytdl_data["title"], 
        thumb=kapak, 
        caption=açıklama, 
        supports_streaming=True,
        progress=ilerleme,
        progress_args=(pablo, baslangic, f'`{sorgu} yükleniyor!`', dosya_adi)
    )
    
    await pablo.delete()
    indirme_durumu = False
    
    # Temizlik
    for dosya in (kapak, dosya_adi):
        if os.path.exists(dosya):
            os.remove(dosya)import sys
import time
from helpers.errors import DurationLimitError

@Client.on_message(filters.command('song') & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 Şarkı Bulunuyor...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "❌ Hiçbir Şey Bulunamadı.\n\nBaşka bir anahtar işini deneyin veya belki doğru şekilde heceleyin."
        )
        print(str(e))
        return
    m.edit("Şarkıyı indirme ")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = '**🎵 Yükleyen @MisakimusicBot**'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('❌ Hata')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

ARQ_API = "http://35.240.133.234:8000"
arq = ARQ(ARQ_API)


def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None
    
    

def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["🔴" for i in range(math.floor(percentage / 10))]),
            "".join(["🔘" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**Dosya Adı:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


def get_user(message: Message, text: str) -> [int, str, None]:
    if text is None:
        asplit = None
    else:
        asplit = text.split(" ", 1)
    user_s = None
    reason_ = None
    if message.reply_to_message:
        user_s = message.reply_to_message.from_user.id
        reason_ = text if text else None
    elif asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_


def get_readable_time(seconds: int) -> int:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]



ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


# Funtion To Download Song
async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return song_name

is_downloading = False


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))







@Client.on_message(filters.command("saavn") & ~filters.edited)
async def jssong(_, message):
    global is_downloading
    if len(message.command) < 2:
        await message.reply_text("/saavn bir bağımsız değişken gerektirir.")
        return
    if is_downloading:
        await message.reply_text("Başka bir indirme işlemi devam ediyor, bir süre sonra tekrar deneyin.")
        return
    is_downloading = True
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("Aranıyor...")
    try:
        songs = await arq.saavn(query)
        sname = songs[0].song
        slink = songs[0].media_url
        ssingers = songs[0].singers
        await m.edit("İndiriliyor")
        song = await download_song(slink)
        await m.edit("Yükleniyor")
        await message.reply_audio(audio=song, title=sname,
                                  performer=ssingers)
        os.remove(song)
        await m.delete()
    except Exception as e:
        is_downloading = False
        await m.edit(str(e))
        return
    is_downloading = False



# Deezer Music


@Client.on_message(filters.command("deezer") & ~filters.edited)
async def deezsong(_, message):
    global is_downloading
    if len(message.command) < 2:
        await message.reply_text("/deezer bir bağımsız değişken gerektirir.")
        return
    if is_downloading:
        await message.reply_text("Başka bir indirme işlemi devam ediyor, bir süre sonra tekrar deneyin.")
        return
    is_downloading = True
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("Aranıyor...")
    try:
        songs = await arq.deezer(query, 1)
        title = songs[0].title
        url = songs[0].url
        artist = songs[0].artist
        await m.edit("İndiriliyor")
        song = await download_song(url)
        await m.edit("Yükleniyor")
        await message.reply_audio(audio=song, title=title,
                                  performer=artist)
        os.remove(song)
        await m.delete()
    except Exception as e:
        is_downloading = False
        await m.edit(str(e))
        return
    is_downloading = False


@Client.on_message(filters.command(["vsong", "video"]))
async def ytmusic(client,message: Message):
    global is_downloading
    if is_downloading:
        await message.reply_text("Başka bir indirme işlemi devam ediyor, bir süre sonra tekrar deneyin.")
        return

    urlissed = get_text(message)

    pablo =  await client.send_message(
            message.chat.id,
            f"`Youtube Sunucularından {urlissed} Alınıyor . Lütfen Bekleyin.`")
    if not urlissed:
        await pablo.edit("Geçersiz Komut Sözdizimi, Daha Fazla Bilgi Almak İçin Lütfen Yardım Menüsüne Bakın!")
        return
    
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
    try:
        is_downloading = True
        with youtube_dl.YoutubeDL(opts) as ytdl:
            infoo = ytdl.extract_info(url, False)
            duration = round(infoo["duration"] / 60)

            if duration > 8:
                await pablo.edit(
                    f"❌ 8 dakikadan uzun videolara izin verilmez, sağlanan video {duration} dakikadır"
                )
                is_downloading = False
                return
            ytdl_data = ytdl.extract_info(url, download=True)
            
    
    except Exception as e:
        #await pablo.edit(event, f"**Failed To Download** \n**Error :** `{str(e)}`")
        is_downloading = False
        return
    
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**Video Adı ➠** `{thum}` \n**İstenen :** `{urlissed}` \n**Kanal :** `{thums}` \n**Bağlantı :** `{mo}`"
    await client.send_video(message.chat.id, video = open(file_stark, "rb"), duration = int(ytdl_data["duration"]), file_name = str(ytdl_data["title"]), thumb = sedlyf, caption = capy, supports_streaming = True , progress=progress, progress_args=(pablo, c_time, f'`Uploading {urlissed} Song From YouTube Music!`', file_stark))
    await pablo.delete()
    is_downloading = False
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
