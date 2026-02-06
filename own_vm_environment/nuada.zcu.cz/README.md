
# Jak rozchodit VM s SSH připojením na nuada.zcu.cz


- Řešení problémů:
  - Připojení přes SSH musí být z univerzitní sítě !!!

  - Linux NANO editor [vloži pravým tl.myši, CTRL+X, potvrdit Y, a uložit Enter].

  - Část návodu je zde: https://helpdesk.zcu.cz/wiki/Virtu%C3%A1ln%C3%AD_stroje

  - Někdy se při špatném přihlášení ve Windows automaticky uloží nefunkční klíč k SSH do uživatelského prostředí a pak se automaticky (chybně) používá, viz poslední řádky souboru (případně je smazat):
    ```c:/Users/nyklm/.ssh/known_hosts```

---------

- Klíč vygenerovat v PuTTygen jako **RSA (2048)** - po vygenerování lze z okna zkopírovat Public Key a nutně si uložit oba soubory s Public i Private klíči.

- V nuada.zcu.cz Sunstone jít do **User -> Settings -> Security** a zkopírovat Public Key, ale bez dalšího balastu kolem, např. jen:
<br>
```ssh-rsa AAAAB3NzaC1y...jELF8FZHKOxmqYO3 rsa-key-20260202```
  - Lze vložit i Private Key.

- VM vytvořit s **Ubuntu 22** (z nabýzených je nejmenší).

- Každá Virtual Machine (VM) si vezme uživatelovy klíče (nastavé v security) pouze při svém prvním startu!!
  - Lze ověřit ve webové konzoli - přihlásit jako "root" bez hesla.
  - Nechat si vypsat obsah souboru, který sice není vyhledatelný přes "ls", ale měl by existovat:
    ```
    cat /root/.ssh/authorized_keys\
    ```
  - Pokud neexistuje, tak lze vytvořit a vložit tam čistý Public Key. Nastavení práv nevím, jestli je nutné.
    ```
    mkdir -p /root/.ssh
    nano /root/.ssh/authorized_keys
    chmod 700 /root/.ssh
    chmod 600 /root/.ssh/authorized_keys
    ```
  - Přidání dalších Public Key lze doplněním souboru "authorized_keys", každý klíč na jedné řádce.
    ```
    nano /root/.ssh/authorized_keys
    ```

-------------

- Přihlášení pres PuTTy:
  - Zadat server jako IP (např. 147.228.173.27) nebo **sulis27.zcu.cz**, viz webová konzole.
  - Načíst soubor s primárním klíčem v **Category -> Connection -> SSH -> Auth -> Credentials**.
  - Takto nastavené prostředí lze v PuTTy uložit přes Save.
  - Otevřít spojení a přihlásit se jako "root". Namísto hesla se automaticky použije klíč.

- Přihlášení přes WinSCP:
  - **SFTP, sulis27.zcu.cz, port 22**.
  - Uživatel **"root" bez hesla**.
  - Načíst soubor s primárním klíčem v **Pokročilé -> SSH -> Autentizace -> Parametry autentizace**.
  - Lze uložit.

-----------

- Instalace VM pro nasazení Python Flask serveru:
  - Instalace knihoven:
    ```
    apt update
    apt install python3-pip
    - Potvrdit restartované služby přes OK.
    pip3 --version
    pip3 install flask
    ```

  - Spuštění aplikace **server_test.py**:
    ```
    python3 server_test.py
    ```
    - Ukáže, na jaké URL běží, a tu stačí zadat do prohlížeče, např. http://147.228.173.27:5000/
  
- Nastavení automatické služby spouštěné po startu systému:
  - Soubor s nastavením služby:
```
    sudo nano /etc/systemd/system/flask-app.service
```
- Zadat následující (vloži pravým tl.myši, CTRL+X, potvrdit Y, a uložit Enter):
```
[Unit]
Description=Flask test application
Wants=network-online.target
After=network-online.target

[Service]
User=root
WorkingDirectory=/home
ExecStart=/usr/bin/python3 /home/server_test.py
Restart=always
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
```

  - Spuštění služby:
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app
```

  - Kontrola stavu služby:
```
systemctl status flask-app
```

  - Ukončení aktuálního běhu a celková deaktivace služby:
```
sudo systemctl stop flask-app
sudo systemctl disable flask-app
```


