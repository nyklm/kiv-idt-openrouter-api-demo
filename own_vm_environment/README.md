
# Experimentální nasazení AI pro opravu studentských prací

- V tuto chvíli HTTP server neběží a musí se spustit přes SSH.
  - URL webu: http://147.228.173.27:5000
  - Python aplikace:
    ```
    python3 /home/server_test.py
    ```

## VM na nuada.zcu.cz

- Přihlášení přes SSH lze pouze z univerzitní sítě !!
  - Např. Cisco VPN AnyConnect (instalace viz web support CIV)

- Popis vytvoření VM je v adresáři **nuada.zcu.cz**.
  - Obsahuje i popis připojení přes PuTTY a WinSCP.
  - Obsahuje i sdílený SSH klíč pro přihlášení k VM (v rámci vývoje).
  - Dále obsahuje popis nasazení Python aplikace s Flask HTTP serverem 
  - a vytvoření příslušné služby spouštěné při startu systému (přesněji po navázání internetového připojení; plus případný restart aplikace).

- Základní Python aplikace s HTTP serverem je v **app_python_flask_test**.

---------

---------

# Poznámky pro implementaci
- CW umí udělat export prací, ale neumí import. Místo importu ruční kopírování.

## Současný stav

**!!! Popis programu app_main je v app_main/README.md !!!**.

* Na CW exportuji práce do ZIPu s volbou "Rozbalit ZIPy uvnitř".
* Dám tento ZIP do input_dir.
* Spustím *main.py* skript, který:
  * rozbalí tento ZIP.
  * projde adresáře jednotlivých studentů a extrahje obsahy všech .cs souborů do jednoho souboru pro každého studenta,
  * pro každého studenta zavolá OpenRouter API s tímto souborem a uloží odpověď do souboru s analýzou pro každého studenta,
  * zkomprimuje výstupní adresář do ZIPu.

--------------

* v OpenRouterAPITool je ukázka jak jednu práci studenta vyhodnotit přes OpenRouter API,
    * poskládá zprávu pro OpenRouter API a odešle jí tam,
    * odpověď uloží do souboru.


--------------

# Experimety

- Zkoušel jsem kód slečny Romové (od nás 5 bodů):
  - google/gemini-2.5-flash-lite
    - 4 pokusy se stejným nastavením
    - identifikovány hlavní problémy (byť jsou triviální)
    - výstupy se celkem liší po jazykové stránce a detailu nalezených chyb
    - někdy mírně zavádějící
    - nejvíce zavádějící bodové hodnocení "správnost řešení" - různé hodnoty.
      - možná je to špantá otázka, špatně rozhodnutelná.
    - možná vadí ono "lite"
  - google/gemini-2.0-flash-001
    - 4 pokusy se stejným nastavením
    - stručnější výstup než u 2.5, ale možná to je lepší.
    - stabilnější bodové hodnocení
    - přijde mi lepší, než 2.5 lite.
  - 
