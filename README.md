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

The media folder will be mantained when running uninstall.sh

The service for automatic shutdown will be disabled and removed

# Setup Notes

## Homer

Web UI for quickly access the server services. If the .env variable DNS_ENTRY is set, the link will redirect to DNS_ENTRY:SERVICE_PORT. If not, the link will point to IP:SERVICE_PORT

To set your local dns, use Pihole, further instructions below.

## Radarr and Sonarr

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

## Photoprism
Photoprism is a media manager for photos and videos
Its purpose is to manage the media of different devices, mainly my phone
It is possible to sync phone's media using the Photo Sync App, available for Android and IOS
To sync with photoprism, it is necessary to purchase the NAS option in the Photo Sync App, 2€ at March 2023
To set the server's endpoint for sync, access to the photo prism web interface settings->services->connect via webdav to rietreve 
your server url, sync will work only in your local network unless you expose your ip to the network

In the photo sync app, go to settings->configure endpoints
For IOS there's an option for a photosync endpoint
For Android you must select WebDAV, past the endpoint of the photoprism web page in the server field, the other fields should autocompile

## Pihole

Follow the installations steps of the official [github repo](https://github.com/pi-hole/docker-pi-hole/?tab=readme-ov-file#installing-on-ubuntu-or-fedora)

Under the Local DNS -> DNS Records create an entry for your server host system. The domain name should be under the form of www.yourName.local

Remember to set your server endpoint as a dns option in your modem router.