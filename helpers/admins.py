# Calls Music 1 - Telegram grup sesli sohbetlerde müzik akışı botu
# Telif Hakkı (C) 2021 Roj Serbest
# GNU Affero Genel Kamu Lisansı v3 altında özgür yazılımdır

from typing import List
from pyrogram.types import Chat, User

import cache.admins  # Yönetici önbelleği modülü


async def yönetici_listesi_al(chat: Chat) -> List[User]:
    """
    Grup yöneticilerini alır ve önbelleğe kaydeder.
    
    Args:
        chat (Chat): Grup sohbeti
        
    Returns:
        List[User]: Yönetici kullanıcı listesi
    """
    # Önbellekten kontrol et
    mevcut = cache.admins.get(chat.id)

    if mevcut:
        return mevcut
    else:
        # Grubun tüm yöneticilerini al
        yöneticiler = await chat.get_members(filter="administrators")
        kaydedilecekler = []

        # Sesli sohbet yönetme yetkisi olanları ekle
        for yönetici in yöneticiler:
            #if yönetici.can_manage_voice_chats:  # Bu satır yorumda kalmış
            kaydedilecekler.append(yönetici.user.id)

        # Önbelleğe kaydet
        cache.admins.set(chat.id, kaydedilecekler)
        return await yönetici_listesi_al(chat)
        cache.admins.set(chat.id, to_set)
        return await get_administrators(chat)
