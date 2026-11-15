# YouTube Warder Evolution – Odbery: overená referencia Taapat git1296
14. november 2026 | Výskum k test33 | Iba vývojová vetva, **bez vydania IPK**

## Referenčný balík

Používateľ dodal `enigma2-plugin-extensions-youtube_git1296(1).ipk`.
Jeho Debian/opkg control obsahuje:
- `Package: enigma2-plugin-extensions-youtube`;
- `Version: git1296+15a7fba0+15a7fba89b-r0`;
- `Maintainer: Taapat`, `License: GPL-2.0-or-later`;
- `Architecture: cortexa15hf-neon-vfpv4`.

Archív používa `data.tar.zst`. Funkčný Python kód je distribuovaný prevažne ako `.pyc`, **nie** ako čitateľné zdrojové `.py`. Nasledujúce pozorovania sú **statická analýza názvov funkcií a reťazcov**, nie potvrdenie funkčnosti na aktuálnom Enigma2 či účte.

Pozorované komponenty:
- `OAuth.pyc`: `get_user_code`, `get_new_token`, `get_access_token`, `device_code`, `refresh_token`;
- `YouTubeApi.pyc`: `subscriptions_list` s `mine=true`, `subscriptions_insert`, `subscriptions_delete`, `channels_list`, `playlist_items_list`;
- `YouTubeUi.pyc`: `mySubscriptions`, `getAllSubscriptions`, `recent_subscr`, `subscribeChannel`, `unsubscribeChannel`, `myPlaylists`;
- ikony `my_subscriptions`, `recent_subscr`, `my_playlists` a ďalšie lokalizácie vrátane SK/CZ/DE.

V balíku je aj konfiguračný súbor `/etc/enigma2/YouTube.key`. **Jeho hodnoty ani pôvodný OAuth client ID/secret nesmú byť vložené do Warder pluginu, repozitára, logov ani preberať ako verejné prihlasovacie údaje.**

## Starý OAuth nie je vhodné skopírovať

Súbor `OAuth.pyc` obsahuje staré endpointy:
- `https://accounts.google.com/o/oauth2/device/code`
- `https://accounts.google.com/o/oauth2/token`

Oficiálna dokumentácia Google pre **TV and Limited-Input Device Applications** dnes uvádza:
- `https://oauth2.googleapis.com/device/code` – vydanie overovacieho kódu;
- `https://oauth2.googleapis.com/token` – získanie/obnovenie tokenov;
- rozsah `https://www.googleapis.com/auth/youtube.readonly` pre čítanie odberov.

Dokumentácia: https://developers.google.com/identity/protocols/oauth2/limited-input-device .
Prihlásenie sa vykoná **na inom zariadení** cez zobrazenú URL a kód, nie písaním Google hesla do boxu. Potrebný je vlastný OAuth klient typu **TVs and Limited Input devices** a povolená YouTube Data API. Bez skutočného overenia nemožno tvrdiť, že osobné Odbery už fungujú.

## Naša implementácia Odberov (prednosť pred Playlistmi)

Používateľ ukázal youtube.com/feed/subscriptions s prehľadom **Najnovšie** a voľbou **Všetky odbery**. Cieľová natívna Warder obrazovka:

1. Ak nie je účet pripojený: zrozumiteľné `Pripojiť YouTube účet`; nepredstierať odbery ani nepoužiť lokálne Obľúbené ako náhradu.
2. OAuth TV flow: tlačidlo `Pripojiť účet` explicitne vyžiada device code; zobrazí URL, krátky kód, čas platnosti; prerušenie a vypršanie bez zaseknutia GUI; rešpektovať `interval` a `slow_down`. Žiadne heslo sa na TV nevyžaduje.
3. Len po úspešnom súhlase `subscriptions.list(part=snippet,contentDetails,mine=true,maxResults=50,pageToken=...)` načíta **Všetky odbery** s stránkovaním.
4. Pre **Najnovšie** je samotný `subscriptions.list` zoznam kanálov, nie feed videí. Identifikovať `contentDetails.relatedPlaylists.uploads` odoberaných kanálov cez `channels.list(part=contentDetails,id=...)`; potom získavať najnovšie položky cez `playlistItems.list(part=snippet,contentDetails,playlistId=...)`. V UI zobraziť skutočné videá s dátumom publikovania, limitovaným cache a jasnými chybami. Tento prístup podporuje oficiálna YouTube Data API dokumentácia.
5. Pre prehrávanie použiť **existujúci** Warder resolver a prehrávač; pre 3×2 náhľady existujúci `HomeThumbs`, limity max 2 download workers a 1 ePicLoad dekóder.
6. Všetka sieť, token refresh a diskové I/O iba cez worker, nikdy na GUI vlákne. Tokens lokálne so súkromnými právami, bez vypisovania, bezpečné odhlásenie a možnosť odvolať prístup. Chybové stavy nezamieňať s prázdnym zoznamom.
7. Pre prvé overenie iba **read-only Odbery**. Pridávanie a rušenie odberov na samotnom YouTube si vyžaduje osobitný write scope a potvrdenie používateľom; nepridávať ho implicitne.

Oficiálne zdroje:
- https://developers.google.com/youtube/data/reference/rest/v3/subscriptions/list
- https://developers.google.com/youtube/data/reference/rest/v3/channels
- https://developers.google.com/youtube/data/reference/rest/v3/playlistItems/list
- https://developers.google.com/youtube/data/guides/implementation/videos

## Regresné hranice

**Nedotýkať sa** používateľom schváleného test33 vzhľadu hlavičky a INFO okna (náhľad, posúvanie textu a posuvník), prehrávača, vyhľadávania, Histórie ani Obľúbených. Všetky nové texty pre SK/CZ/DE/EN. Nevydať stabilnú verziu bez schválenia používateľom. Nepublikovať ani nezabaliť cudzie credentials. Kód z referenčnej binárky nereprodukovať ako domnelý nový zdroj.

Stav: **analýza referenčného IPK a implementačný plán dokončené; OAuth/odbery zatiaľ neimplementované**.
