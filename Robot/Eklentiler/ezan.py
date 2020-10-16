# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Robot.Edevat.zenginLog import log_yolla, hata_log
from Robot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama" : "sabah.com.tr'den ezan vakti bilgilerini verir..",
        "kullanim" : [
            "il"
            ],
        "ornekler" : [
            ".ezan çanakkale"
            ]
    }
})

from pyrogram import Client, filters
from Robot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from Robot.Edevat.Spatula.ezan_spatula import ezan_vakti

@Client.on_message(filters.command(['ezan'],['!','.','/']))
async def ezan(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    yanitlanacak_mesaj = yanitlanan_mesaj(message)
    ilk_mesaj = await message.reply("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown",
        reply_to_message_id         = yanitlanacak_mesaj
    )
    girilen_yazi = message.command
    #------------------------------------------------------------- Başlangıç >

    if len(girilen_yazi) == 1:
        await ilk_mesaj.edit("__Arama yapabilmek için `il` ve `ilçe` girmelisiniz..__")
        return

    il   = girilen_yazi[1].lower()  # komut hariç birinci kelime

    tr2eng  = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
    il      = il.translate(tr2eng)

    try:
        await ilk_mesaj.edit(ezan_vakti(il))
    except IndexError:
        await ilk_mesaj.edit(f'`{il}` __diye bir yer bulamadım..__')
    except Exception as hata:
        hata_log(client, hata)
        await ilk_mesaj.edit(f'**Hata Var !**\n\n`{type(hata).__name__}`\n\n__{hata}__')