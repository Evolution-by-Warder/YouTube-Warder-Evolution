# YouTube Warder Evolution 1.0.2

**Stabilné vydanie – 17. novembra 2026**

## Novinky
- Obrazovka **Nastavenia** používa prehľadný natívny zoznam. Položky Účet YouTube, Prehrávač, Maximálna kvalita videa a Hlavné menu Enigma2 sa ovládajú šípkami, OK alebo ZELENÝM tlačidlom; ŽLTÉ a MODRÉ tlačidlo naďalej menia prehrávač a kvalitu.
- Nová voľba **Zobraziť v hlavnom menu Enigma2: Nie/Áno**. Predvolené nastavenie je **Nie**. Výber sa uloží natrvalo; po zmene treba reštartovať GUI Enigma2. V bežnom zozname pluginov YouTube zostáva dostupný bez ohľadu na túto voľbu.
- Preklady nového menu sú dostupné v SK, CS, DE a EN.
- Inštalácia, aktualizácia, preinštalovanie aj odinštalovanie cez Telnet vypisujú zjednotené bloky hviezdičiek a správne hlásenia, rovnako ako Warder Radio. Pri upgrade sa nevypisuje „Removal finished“.
- Zachovaná automatická kontrola ServiceApp, ExtePlayer3, Python modulov a yt-dlp po ukončení opkg a diagnostický súbor `/tmp/warder-youtube-deps.log`.

## Zachované funkcie a dáta
Prehrávanie, Domov, Odbery, účet YouTube, obnovenie tokenov, Obľúbené, História a existujúce používateľské údaje sa nemenia. Oprava Google TV OAuth z verzie 1.0.1 zostáva súčasťou balíka. Staré ostré vydania 1.0.0 a 1.0.1 sa neprepisujú.

## Inštalácia
Použi vstavanú položku **Aktualizácie** v stabilnej 1.0.1 alebo IPK v adresári `/tmp`:

```sh
opkg install /tmp/enigma2-plugin-extensions-youtube-warder-evolution_1.0.2_all.ipk
```

Po inštalácii reštartuj GUI Enigma2. Ak máš nainštalovanú verziu `1.0.2~test1`, použi IPK ručne, pretože testovací aktualizačný kanál nemusí ponúknuť stabilné vydanie.

## Overenie a kompatibilita
Automatické testy, platnosť archívu, zhoda verzií a kontrola inštalátora. Pôvodná kompatibilita OpenATV a OpenPLi je zachovaná, ale vzhľad a nové menu vo verzii 1.0.2 ešte potrebujú kontrolu na skutočnom prijímači.
