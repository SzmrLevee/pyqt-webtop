#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$PROJECT_DIR"

echo "Docker-szolgáltatások indítása..."
docker compose up -d --build

echo "Várakozás a MySQL-re..."

until [ "$(docker inspect \
    --format='{{.State.Health.Status}}' \
    pyqt-mysql 2>/dev/null || true)" = "healthy" ]; do
    sleep 2
done

echo "A MySQL elérhető."

echo "Python-környezet ellenőrzése..."

docker exec \
    -u abc \
    pyqt-webtop \
    bash -lc '
        cd /workspace

        if [ ! -x .venv-webtop/bin/python ]; then
            rm -rf .venv-webtop
            python3 -m venv .venv-webtop
        fi

        source .venv-webtop/bin/activate
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
    '

echo "PyQt5 alkalmazás indítása..."

docker exec -it \
    -u abc \
    -e DISPLAY=:1 \
    -e XDG_RUNTIME_DIR=/tmp/runtime-abc \
    pyqt-webtop \
    bash -lc '
        mkdir -p /tmp/runtime-abc
        chmod 700 /tmp/runtime-abc

        cd /workspace
        source .venv-webtop/bin/activate

        python main.py
    '