# Calls Music 1 - Telegram grup sesli sohbet müzik botu
# Telif Hakkı (C) 2021 Roj Serbest
# GNU Affero Genel Kamu Lisansı v3

from typing import Callable, List
from pyrogram import Client
from pyrogram.types import Message, Chat, User

from config import SUDO_USERS
import cache.admins  # Önbellek sistemi (aşağıda tanımlı)


async def yönetici_listesi_al(chat: Chat) -> List[User]:
    """
    Grup yöneticilerini alır ve önbelleğe kaydeder.
    """
    mevcut = cache.admins.get(chat.id)

    if mevcut:
        return mevcut
    else:
        yöneticiler = await chat.get_members(filter="administrators")
        kaydedilecekler = []

        for yönetici in yöneticiler:
            kaydedilecekler.append(yönetici.user.id)

        cache.admins.set(chat.id, kaydedilecekler)
        return await yönetici_listesi_al(chat)


def hata_yakala(func: Callable) -> Callable:
    """
    Hata yakalama - Komutlar hata verirse kullanıcıya bildirir
    """
    async def dekorator(client: Client, mesaj: Message):
        try:
            return await func(client, mesaj)
        except Exception as e:
            await mesaj.reply(f"❌ Hata: {type(e).__name__}: {e}")

    return dekorator


def sadece_yetkili_kullanıcılar(func: Callable) -> Callable:
    """
    Yetki kontrolü - Sadece adminler ve sudo kullanıcılar kullanabilir
    """
    async def dekorator(client: Client, mesaj: Message):
        # Sen (SUDO_USERS) her zaman kullanabilirsin
        if mesaj.from_user.id in SUDO_USERS:
            return await func(client, mesaj)

        # Grup yöneticilerini kontrol et
        yöneticiler = await yönetici_listesi_al(mesaj.chat)

        for yönetici in yöneticiler:
            if yönetici == mesaj.from_user.id:
                return await func(client, mesaj)

    return dekoratordef authorized_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

        administrators = await get_administrators(message.chat)

        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator
