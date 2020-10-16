# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Robot.Edevat.zenginLog import log_yolla, hata_log
from Robot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"     : "eczaneler.gen.tr'den nöbetçi eczane bilgilerini verir..",
        "parametreler" : [
            "il ilçe"
            ],
        "ornekler"     : [
            ".nobetci çanakkale merkez"
            ]
    }
})

from pyrogram import Client, filters
from Robot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from Robot.Edevat.Spatula.nobetci_spatula import nobetci_eczane

@Client.on_message(filters.command(['nobetci'],['!','.','/']))
async def nobetci(client, message):
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
    elif len(girilen_yazi) == 2:
        await ilk_mesaj.edit("__Arama yapabilmek için `ilçe` **de** girmelisiniz..__")
        return

    il   = girilen_yazi[1].lower()  # komut hariç birinci kelime
    ilce = girilen_yazi[2].lower()  # komut hariç ikinci kelime

    tr2eng  = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
    il      = il.translate(tr2eng)
    ilce    = ilce.translate(tr2eng)

    mesaj = f"**Aranan Nöbetçi Eczane :** `{ilce}` / `{il}`\n"

    try:
        for eczane in nobetci_eczane(il, ilce, "json_veri"):
            mesaj += f"**\n\t⚕ {eczane['eczane_adi']}**\n📍 __{eczane['eczane_adresi']}__\n\t☎️ `{eczane['eczane_telefonu']}`\n\n"

        await ilk_mesaj.edit(mesaj)
    except IndexError:
        await ilk_mesaj.edit(f'__`{ilce}` / `{il}` diye bir yer bulamadım..__')
    except Exception as hata:
        hata_log(client, hata)
        await ilk_mesaj.edit(f'**Hata Var !**\n\n`{type(hata).__name__}`\n\n__{hata}__')