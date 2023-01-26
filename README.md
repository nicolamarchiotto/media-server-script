# media-server-script

The install.sh script create a media server, list of services offered by dockers

qbittorrent web interface   http://localhost:8080
default user:admin, default password:adminadmin

filebrowser web interface   http://localhost:8081
default user:admin, default password:admin

jellyfin web interface      http://localhost:8096

sonarr web interface        http://localhost:8989

radarr web interface        http://localhost:7878

jackett web interface       http://localhost:9117

The scipts creates a media folder, with a shows and a movies subdirectoris, in the user home
If the folders already exist they will not be overwritten

Jellyfin will visualize media from these folders

# Radarr and Sonarr

To be set on web interface:
- Set client torrent as qbittorrent, address is localhost:8080, credentials admin-adminadmin
- Set client (qbittorrent) download folder:
- For radarr /downloads/movies, for sonarr /downloads/shows
- Set indexers using jackett, settings -> indexers -> add -> torznab
  url as torznab feed in jackett
  api key is the jackett api key
  set categories accordingly to the indexer
- For sonarr use tags to automatically retrieve episode with subtitles
  - create a profile named "subs" with must contained field the word "sub"
  - for the category tags, write "subs" -> IMPORTANT!
  - set the following preferred term and scores
  
    - multi-subs          500
    - multi-sub           500
    - multi sub           500
    - multi subs          500
    - multiple subtitle   500
    - sub ita             300
    - sub eng             200
    - sub                 100
  
  - On new serie addition, if you want release with subtitles, select "subs" tag
  
- For sonarr create a language profile name multilanguage with wanted language italian and english, create one for with only italian and one with only english
- For sonarr, on show addition be carefull of:
  - select right language for the relese
  - select right type of shows, anime if anime, standard if tv shows, if not, correct episode may not be found
  - add "subs" tag if subtitles are wanted
  - select which episodes to download, ex. future episodes, missing episodes ecc.
  - check "start search for missing episodes" for search immedieatly for missing episodes
  
- For radarr do not set tags or custom profile, for each movie do a search and manually select the version to download, it's easier


# Automatic shutdown
The install.sh script set a service which will automatically turnoff the system at 01:30 am

After the installation, change take place if command `update the system services: sudo systemctl daemon-reload` is run

If not changes will take place after restart

# Uninstall
To uninstall run unistall.sh, docker and shh will be removed

The media folder will be mantained when running uninstall.sh

The service for automatic shutdown will be disabled and removed
