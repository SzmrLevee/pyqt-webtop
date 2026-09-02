# PyQt5 Webtop + MySQL

Böngészőből futó fejlesztői környezet PyQt5 alkalmazásokhoz. A felületet a LinuxServer Webtop szolgáltatja, az adatokat MySQL tárolja, az adatbázist pedig phpMyAdminból is tudod kezelni.

Ez a projekt arra készült, hogy iPaden, NAS-on vagy távoli Linux szerveren is kényelmesen fejlessz PyQt5-öt, miközben a háttérben egy valódi SQL adatbázist használsz.

## Technológiák

- PyQt5
- MySQL 8.4
- phpMyAdmin
- LinuxServer Webtop
- KasmVNC
- Docker Compose

## Mit tud

- böngészőből elérhető asztali Linux környezet
- PyQt5 app futtatása a Webtop konténerben
- MySQL-alapú jegyzetkezelés
- automatikus tábla-létrehozás első induláskor
- egyszerű indítás egyetlen scriptből

## Indítás

1. Másold a mintakörnyezetet:

```bash
cp .env.example .env
```

2. Állítsd be az adatbázis jelszavakat az `.env` fájlban.

Minimum ezek legyenek benne:

```bash
MYSQL_ROOT_PASSWORD=change_this_root_password
MYSQL_DATABASE=pyqt_app
MYSQL_USER=pyqt_user
MYSQL_PASSWORD=change_this_application_password
```

3. Indítsd el a teljes stack-et:

```bash
chmod +x start.sh
./start.sh
```

Az első indulás lassabb lehet, mert a Docker letölti és felépíti a képeket.

A `start.sh` végigviszi a teljes indítást: felhozza a Dockert, megvárja a MySQL-t, majd elindítja a PyQt appot a Webtop konténerben.

Ha csak a Docker stack-et akarod felhozni külön a script nélkül:

```bash
docker compose up -d --build
```

## Tiszta újraindítás

Ha csak újra akarod építeni és indítani a teljes stack-et, ezt használd:

```bash
docker compose up -d --force-recreate
```

Ha a MySQL jelszavakat is átírtad, és a régi adatbázis-állapot gondot okoz, akkor teljes reset kell:

```bash
docker compose down -v --remove-orphans
docker compose up -d --build --force-recreate
```

## Ha nem jelenik meg a PyQt

Ha a Webtop elindul, de a PyQt alkalmazás nem jön fel automatikusan, így indíthatod kézzel a konténerben:

```bash
docker exec -it \
	-u abc \
	-e DISPLAY=:1 \
	-e XDG_RUNTIME_DIR=/tmp/runtime-abc \
	pyqt-webtop bash -lc '
		mkdir -p /tmp/runtime-abc &&
		chmod 700 /tmp/runtime-abc &&
		cd /workspace &&
		if [ ! -x .venv-webtop/bin/python ]; then
			python3 -m venv .venv-webtop
		fi &&
		source .venv-webtop/bin/activate &&
		python -m pip install -r requirements.txt &&
		python main.py'
```

Ha ez még mindig nem indítja el, először nézd meg, hogy a konténerek futnak-e:

```bash
docker compose ps
```

## Elérés

- Webtop: `http://127.0.0.1:3000`
- Webtop HTTPS: `https://127.0.0.1:3001`
- phpMyAdmin: `http://127.0.0.1:8081`
- MySQL: `127.0.0.1:3306`

## phpMyAdmin belépés

- Szerver: `mysql`
- A phpMyAdmin alapból az `MYSQL_USER` / `MYSQL_PASSWORD` párral nyílik meg
- Ha manuálisan kell belépni, ugyanazokat az értékeket használd

Ha korábban változott az `.env`, de a belépés mégis hibát dob, valószínűleg a régi MySQL volume maradt meg. Ilyenkor futtasd a teljes újrainicializálást a fenti "Tiszta újraindítás" rész szerint.

Root admin belépéshez:

- Felhasználónév: `root`
- Jelszó: az `MYSQL_ROOT_PASSWORD` értéke

## Fő fájlok

- [main.py](main.py) - PyQt5 felület és jegyzetkezelés
- [database.py](database.py) - MySQL kapcsolat és SQL műveletek
- [docker-compose.yml](docker-compose.yml) - szolgáltatások és portok
- [start.sh](start.sh) - teljes indító script

## Megjegyzés

A projekt helyi fejlesztésre készült. Az `.env` fájlt ne töltsd fel GitHubra.
