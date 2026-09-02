FROM lscr.io/linuxserver/webtop:ubuntu-openbox

USER root

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        libxcb-cursor0 \
        libxcb-xinerama0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-render-util0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0 \
        libgl1 \
        libegl1 \
        libdbus-1-3 \
        libfontconfig1 \
        libfreetype6 \
    && rm -rf /var/lib/apt/lists/*