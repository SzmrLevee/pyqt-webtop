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

3. Indítsd el a teljes stack-et:

```bash
chmod +x start.sh
./start.sh
```

Az első indulás lassabb lehet, mert a Docker letölti és felépíti a képeket.

## Elérés

- Webtop: `http://127.0.0.1:3000`
- Webtop HTTPS: `https://127.0.0.1:3001`
- phpMyAdmin: `http://127.0.0.1:8081`
- MySQL: `127.0.0.1:3306`

## phpMyAdmin belépés

- Szerver: `mysql`
- A phpMyAdmin alapból az `MYSQL_USER` / `MYSQL_PASSWORD` párral nyílik meg
- Ha manuálisan kell belépni, ugyanazokat az értékeket használd

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
