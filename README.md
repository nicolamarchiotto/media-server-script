# Home Media Server

Code for automaically setup a home media server with containerized services. <br>
The web UIs can accessed from an unique page, by default on localhost:8082

## List of all the servicses

| Services    | Default port | Default Credentials            | Folders of Interest (.env)      | Base Image                                         |
|-------------|:------------:|-------------------------------:|--------------------------------:|---------------------------------------------------:|
| Homer       | 8082         |                                |                                 | b4bz/homer:v23.10.1                                |
| qBitTorrent | 8080         | admin, *tmp pw in docker logs* | $MEDIA_FOLDER                   | lscr.io/linuxserver/qbittorrent:4.6.2-libtorrentv1 | 
| Filebrowser | 8081         | admin, admin                   | $MEDIA_FOLDER                   | hurlenko/filebrowser:v2.26.0                       | 
| Jellyfin    | 8096         |                                | $SHOWS_FOLDER, $MOVIES_FOLDER   | lscr.io/linuxserver/jellyfin:10.8.13               | 
| Sonarr      | 8989         |                                | $SHOWS_FOLDER                   | lscr.io/linuxserver/sonarr:4.0.0                   | 
| Radarr      | 7878         |                                | $MOVIES_FOLDER                  | lscr.io/linuxserver/radarr:5.2.6                   | 
| Jackett     | 9117         |                                |                                 | lscr.io/linuxserver/jackett:0.21.1448              | 
| Photoprism  | 2342         | admin, insecure                | $PICTURES_FOLDER                | photoprism/photoprism:231128                       | 
 

# install.sh
**Change the port configuration using the .env file, do not edit the docker-compose.yml file directly.**<br>
Be carefull to not introduce new lines in the .env file

The install.sh script perform the following actions

- Install openssh-server if not already installed on the system
- Install docker engine
- runs the edit edit_homer_config.py python script, install PyYAML as prerequisites
  - The script retrieve the docker condfiguration from the .env file and edits the Homer config.yml file accordingly
- create a service which will **automatically turnoff the system at 01:30 am**, might need to reboot manually to apply the changes
- creates all the containers from the docker-compose.yml

## uninstall.sh
- To uninstall run unistall.sh, docker and shh will be removed
- The media folder will be mantained when running uninstall.sh
- The service for automatic shutdown will be disabled and removed

## HW setup
- Script was tested with ubunru 22.04.03 LTS server
- Docker engine and ssh can be installed directly via the ubuntu installer
- Run on system with intel i5 8th gen, 8 Gb of ram, 256GB ssd for hosting the system, 1TB of hdd for media
- Space required for whole installation is 20 GB

# Setup notes

## Radarr and Sonarr

To be set on web interface:
- Set client torrent as qbittorrent, address is localhost:8080, set your qbittorrent installation credentials
- Set indexers using jackett, settings -> indexers -> add -> torznab
  get the url clicking the _copy torznab feed_ of your jackett entries
  api key is the jackett api key
  set categories accordingly to the indexer
- For **Sonarr**, exploit custom formats to automatically retrieve episode with **subtitles**
  - create the following custom formats, each one must have a required condition on the release title, the string to be matched are the following
  - the regular expression should be \bstring2bematched\b
    - multi-subs          
    - multi-sub           
    - multi sub   
    - multi subs          
    - multiple subtitles          
    - multiple subtitle  
    - sub ita             
    - sub eng             
    - sub
    - subs                 
  - On the _Profile_ section, create a new profile HD-1080p-subs starting from the HD-1080p one
    - Assign to each custom format previously created a score of 10
    - Set the Minimum Custom Format Score as 10
  - When adding a new serie, set as quality profile _HD-1080p-subs_
  - **Select Series Type, anime if anime, standard if tv shows, if not, correct episodes may not be found**
  
- For **Radarr** do not use custom profiles, for each movie do a search and manually select the version to download, it's easier

## Photoprism
Photoprism is a media manager for photos and videos.<br>
It is possible to sync a phone's media using the Photo Sync App, available for Android and IOS
To sync with photoprism, it is necessary to purchase the NAS option in the Photo Sync App, 2€ at March 2023.<br>
To set the server's endpoint for sync, access to the photo prism web interface settings->services->connect via webdav to rietreve 
your server url. Sync will work only in your local network unless you expose your ip to the network

In the Photo Sync App, go to settings->configure endpoints.<br>
For IOS there's an option for a photosync endpoint.<br>
For Android you must select WebDAV, past the endpoint of the photoprism web page in the server field, the other fields should autocompile
