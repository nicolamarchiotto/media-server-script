# Home Media Server

Code for automaically setup a home media server with contanairized services. The web UIs can accessed from an unique page, by default on localhost:80

## List of all the servicses

| Services    | Default port | Default Credentials  | Involved Folders                |
|-------------|:------------:|---------------------:|--------------------------------:|
| Homer       | 80           |                      |                                 |
| qBitTorrent | 8080         | admin, adminadmin    | ~/media                         |
| Filebrowser | 8081         | admin, admin         | /                               |
| Jellyfin    | 8096         |                      | ~/media/shows, ~/media/movies   |
| Sonarr      | 8989         |                      |                                 |
| Radarr      | 7878         |                      |                                 |
| Jackett     | 9117         |                      |                                 |
| Photoprism  | 2342         | admin, insecure      | ~/Pictures                      |
| Pihole      | 8084         | pihole               |                                 |

## install.sh

To change the port configuration, do not edit the docker-compose.yml file directly. Edit the .env file instead. Be carefull to not introduce new lines in the .env file

The install.sh script perform the following actions

- Install openssh-server if not already installed on the system
- Install docker engine
- runs the edit edit_homer_config.py python script, install PyYAML as prerequisites
  - The script retrieve the docker condfiguration from the .env file and edits the Homer config.yml file accordingly
- create a service which will **automatically turnoff the system at 01:30 am**, might need to reboot manually to apply the changes
- creates all the containers from the docker-compose.yml

## uninstall.sh


To uninstall run unistall.sh, docker and shh will be removed

## HW setup
- Script was tested with ubunru 22.04.03 LTS server
- Docker engine and ssh can be installed directly via the ubuntu installer
- Run on system with intel i5 8th gen, 8 Gb of ram, 256GB ssd for hosting the system, 1TB of hdd for media
- Space required for whole installation is 20 GB

# Setup notes

## Homer

Web UI for quickly access the server services. If the .env variable DNS_ENTRY is set, the link will redirect to DNS_ENTRY:SERVICE_PORT. If not, the link will point to IP:SERVICE_PORT

To set your local dns, use Pihole, further instructions below.

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


In the photo sync app, go to settings->configure endpoints
For IOS there's an option for a photosync endpoint
For Android you must select WebDAV, past the endpoint of the photoprism web page in the server field, the other fields should autocompile

## Pihole

Follow the installations steps of the official [github repo](https://github.com/pi-hole/docker-pi-hole/?tab=readme-ov-file#installing-on-ubuntu-or-fedora)

Under the Local DNS -> DNS Records create an entry for your server host system. The domain name should be under the form of www.yourName.local

Remember to set your server endpoint as a dns option in your modem router.

Usefull block list can be found [here](https://firebog.net/)
