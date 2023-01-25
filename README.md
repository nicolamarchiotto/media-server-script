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

Instructions fot radarr and sonarr to be set on web interface:
- Set client torrent as qbittorrent, address is localhost:8080, credentials admin-adminadmin
- Set client (qbittorrent) download folder:
- For radarr /downloads/movies, for sonarr /downloads/shows
- Set indexers using jackett, check online tutorials

The install.sh script set a service which will automatically turnoff the system at 01:30

After the installation, update the system services: sudo systemctl daemon-reload 

To uninstall run unistall.sh, docker and shh will be removed
The media folder will be mantained when running uninstall.sh
The service for automatic shutdown will be disabled and removed