#!/bin/sh
# Background helper: postinst must not recursively invoke opkg while its lock is held.
# Logs: /tmp/warder-youtube-deps.log
PATH=/usr/sbin:/usr/bin:/sbin:/bin
LOG=/tmp/warder-youtube-deps.log
LOCK=/tmp/warder-youtube-deps.lock
INSTALLER_PID="${1:-}"
log() { echo "[Warder YouTube] $*" >> "$LOG"; }
: > "$LOG"
log 'Waiting for package manager to finish...'
# Wait for parent opkg to exit. Never run nested opkg inside postinst.
case "$INSTALLER_PID" in
    ''|*[!0-9]*) INSTALLER_PID=0 ;;
esac
count=0
if [ "$INSTALLER_PID" -gt 1 ]; then
    while kill -0 "$INSTALLER_PID" 2>/dev/null; do
        count=$((count + 1))
        if [ "$count" -ge 180 ]; then log 'ERROR: installer still running; no changes made'; exit 1; fi
        sleep 1
    done
fi
# Avoid racing another opkg process (including updates from GUI).
count=0
while pidof opkg >/dev/null 2>&1; do
    count=$((count + 1))
    if [ "$count" -ge 180 ]; then log 'ERROR: opkg still busy; no changes made'; exit 1; fi
    sleep 1
done
if ! mkdir "$LOCK" 2>/dev/null; then log 'Dependency check already running'; exit 0; fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT HUP INT TERM
haspkg() { opkg list-installed 2>/dev/null | grep -Fq "$1 - "; }
installpkg() {
    if haspkg "$1"; then log "$1: OK"; return 0; fi
    log "$1: installing..."
    if opkg install "$1" >> "$LOG" 2>&1; then log "$1: installed"; return 0; fi
    log "ERROR: cannot install $1 from the receiver feed"
    return 1
}
log 'Checking required components...'
# ServiceApp and ExtePlayer3 also appear in package Depends. Validate again.
installpkg enigma2-plugin-systemplugins-serviceapp || exit 1
installpkg exteplayer3 || exit 1
if ! command -v python3 >/dev/null 2>&1; then
    log 'ERROR: Python 3 is missing'; exit 1
fi
# OpenPLi Python 3.9 ships dataclasses as part of python3-profile.
if python3 -c 'import dataclasses' >/dev/null 2>&1; then
    log 'Python dataclasses: OK'
else
    log 'Python dataclasses: missing; checking python3-profile'
    installpkg python3-profile || exit 1
    if ! python3 -c 'import dataclasses' >/dev/null 2>&1; then
        log 'ERROR: Python dataclasses still missing'; exit 1
    fi
fi
# Check import and CLI execution, rather than just command presence.
if command -v yt-dlp >/dev/null 2>&1 && python3 -m yt_dlp --version >/dev/null 2>&1 && yt-dlp --version >/dev/null 2>&1; then
    log "yt-dlp: OK ($(yt-dlp --version 2>/dev/null))"
else
    log 'yt-dlp unavailable or broken; installing compatible runtime...'
    installpkg python3-pip || exit 1
    installpkg python3-certifi || exit 1
    if ! python3 -m pip --version >/dev/null 2>&1; then
        log 'ERROR: Python pip unavailable'; exit 1
    fi
    # Known working for Python 3.9.9 on OpenPLi 9.2; no unbounded -U.
    if ! python3 -m pip install --disable-pip-version-check --no-deps 'yt-dlp==2025.10.14' >> "$LOG" 2>&1; then
        log 'ERROR: yt-dlp pip installation failed'; exit 1
    fi
    if ! python3 -m yt_dlp --version >/dev/null 2>&1 || ! yt-dlp --version >/dev/null 2>&1; then
        log 'ERROR: yt-dlp did not pass validation'; exit 1
    fi
    log "yt-dlp: installed and working ($(yt-dlp --version 2>/dev/null))"
fi
log 'Dependency check COMPLETE'
exit 0
