
# Experimentální nasazení AI pro opravu studentských prací

- V tuto chvíli HTTP server neběží a musí se spustit přes SSH.
  - URL webu: http://147.228.173.27:5000
  - Python aplikace: python3 /home/server_test.py

## VM na nuada.zcu.cz

- Přihlášení přes SSH lze pouze z univerzitní sítě !!
  - Např. Cisco VPN AnyConnect (instalace viz web support CIV)

- Popis vytvoření VM je v adresáři **nuada.zcu.cz**.
  - Obsahuje i popis připojení přes PuTTY a WinSCP.
  - Obsahuje i sdílený SSH klíč pro přihlášení k VM (v rámci vývoje).
  - Dále obsahuje popis nasazení Python aplikace s Flask HTTP serverem 
  - a vytvoření příslušné služby spouštěné při startu systému (přesněji po navázání internetového připojení; plus případný restart aplikace).

- Základní Python aplikace s HTTP serverem je v **python_flask_test_app**.

