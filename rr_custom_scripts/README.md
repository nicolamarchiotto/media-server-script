# For Sonarr and Radarr Connector

Custom script which send message to Telegram bot. Telegram bot can be created with Telegram BotFather.

Script requires bot token (prompter when creating the bot) and your chat id, which can be obtained using Telegram @RawDataBot 

# Test

From inside sonar container launch

sonarr_eventtype=Download sonarr_series_title="Demo Series" sonarr_episodefile_seasonnumber=1 sonarr_episodefile_episodenumbers=1 sonarr_episodefile_episodetitles="Pilot" sonarr_episodefile_relativepath="Season 01/Demo - S01E01.mkv" sonarr_episodefile_size=3449483648 sonarr_series_imdbid="tt0944947" ./rr_telegram_notifier.sh

