#!/bin/sh
#
# Unified Telegram notifier for Sonarr & Radarr
#

BOT_TOKEN="${RR_NOTIFICATOR_TELEGRAM_BOT_TOKEN}"
CHAT_ID="${RR_NOTIFICATOR_TELEGRAM_CHAT_ID}"

if [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
    echo "❌ ERROR: BOT_TOKEN or CHAT_ID not set!"
    exit 1
fi

# === Helpers ===

send_message() {
    local TEXT="$1"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
         -d chat_id="$CHAT_ID" \
         -d text="$TEXT" >/dev/null
}

# Convert bytes → GB with 1 decimal (used only for Grab events)
to_gb() {
    local BYTES="$1"
    if [ -z "$BYTES" ] || [ "$BYTES" -le 0 ] 2>/dev/null; then
        echo "0.0"
    else
        awk -v size="$BYTES" 'BEGIN { printf "%.1f", size/1024/1024/1024 }'
    fi
}

# === Detect Caller ===
if [ -n "$sonarr_eventtype" ]; then
    APP="Sonarr"
    EVENT="$sonarr_eventtype"
elif [ -n "$radarr_eventtype" ]; then
    APP="Radarr"
    EVENT="$radarr_eventtype"
else
    send_message "⚠️ Unknown caller for Telegram notifier script."
    exit 1
fi

# === SONARR HANDLER ===
if [ "$APP" = "Sonarr" ]; then
    case "$EVENT" in
      Test)
        send_message "✅ Sonarr Telegram script test successful!"
        ;;

      Grab)
        SIZE_GB=$(to_gb "$sonarr_release_size")
        MESSAGE="📥 [Sonarr] New release grabbed

📺 Series: $sonarr_series_title
💾 Release: $sonarr_release_title
🌐 Indexer: $sonarr_release_indexer
📦 Size: ${SIZE_GB} GB"
        if [ -n "$sonarr_series_imdbid" ]; then
            MESSAGE="$MESSAGE
🔗 IMDb: https://www.imdb.com/title/${sonarr_series_imdbid}"
        fi
        send_message "$MESSAGE"
        ;;

      Download)
        SEASON="S$(printf "%02d" "$sonarr_episodefile_seasonnumber")"
        EPS="E$(printf "%02d" "$sonarr_episodefile_episodenumber")"

        MESSAGE="✅ [Sonarr] Episode imported

📺 Series: $sonarr_series_title
🎬 Episode: ${SEASON}${EPS} - $sonarr_episodefile_episodetitles
💾 File: $sonarr_episodefile_relativepath"
        if [ -n "$sonarr_series_imdbid" ]; then
            MESSAGE="$MESSAGE
🔗 IMDb: https://www.imdb.com/title/${sonarr_series_imdbid}"
        fi
        send_message "$MESSAGE"
        ;;
    esac
fi

# === RADARR HANDLER ===
if [ "$APP" = "Radarr" ]; then
    case "$EVENT" in
      Test)
        send_message "✅ Radarr Telegram script test successful!"
        ;;

      Grab)
        SIZE_GB=$(to_gb "$radarr_release_size")
        MESSAGE="📥 [Radarr] New movie grabbed

🎬 Title: $radarr_movie_title ($radarr_movie_year)
💾 Release: $radarr_release_title
🌐 Indexer: $radarr_release_indexer
📦 Size: ${SIZE_GB} GB"
        if [ -n "$radarr_movie_imdbid" ]; then
            MESSAGE="$MESSAGE
🔗 IMDb: https://www.imdb.com/title/${radarr_movie_imdbid}"
        fi
        send_message "$MESSAGE"
        ;;

      Download)
        MESSAGE="✅ [Radarr] Movie imported

🎬 Title: $radarr_movie_title ($radarr_movie_year)
💾 File: $radarr_moviefile_relativepath"
        if [ -n "$radarr_movie_imdbid" ]; then
            MESSAGE="$MESSAGE
🔗 IMDb: https://www.imdb.com/title/${radarr_movie_imdbid}"
        fi
        send_message "$MESSAGE"
        ;;
    esac
fi

exit 0