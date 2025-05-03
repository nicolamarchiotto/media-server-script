# Home Media Server

Code for automaically setup a home media server with contanairized services. Web UIs can accessed from an unique page, by default on localhost:8080. The service can be configured to be accessed with an unique url using Nginx Proxy Manager and Pihole

## HW setup
- Script was tested with ubuntu 22.04.03 LTS server
- Docker engine and ssh can be installed directly via the ubuntu installer
- Run on system with intel i5 8th gen, 8 Gb of ram, 256GB ssd for hosting the system, 1TB of hdd for media
- Space required for whole installation is 20 GB

## List of all the servicses

| Services    | Default port | Default Credentials  | Involved Folders                |
|-------------|:------------:|---------------------:|--------------------------------:|
| Homer       | 8080         |                      |                                 |
| qBitTorrent | 8090         | admin, adminadmin    | ~/media                         |
| Filebrowser | 8084         | admin, admin         | /                               |
| Jellyfin    | 8096         |                      | ~/media/shows, ~/media/movies   |
| Sonarr      | 8989         |                      |                                 |
| Radarr      | 7878         |                      |                                 |
| Jackett     | 9117         |                      |                                 |
| Photoprism  | 2342         | admin, insecure      | ~/Pictures                      |
| Pihole      | 8085         | pihole               |                                 |
| NPM         | 81           | admin@example.com, changeme               |            |

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

# Setup notes

## Radarr and Sonarr

To be set on web interface:
- Set client torrent as qbittorrent, address is ip:8090, set your qbittorrent installation credentials
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

### WebDav

To set the server's endpoint for sync, access to the photo prism web interface settings->services->connect via webdav to rietreve 
your server url. Sync will work only in your local network unless you expose your ip to the network

In the photo sync app, go to settings->configure endpoints
For IOS there's an option for a photosync endpoint
For Android you must select WebDAV, past the endpoint of the photoprism web page in the server field, the other fields should autocompile

### PhotoPrism endpoint - 05/03/2025

In photosync app, go to settings->configure PhotoPrism
Enter endpoint, port, credentials and destination folder

## Pihole

Official repo at [pihole](https://github.com/pi-hole/docker-pi-hole/?tab=readme-ov-file#installing-on-ubuntu-or-fedora)

Remember to set your server ip as a dns option in your modem router.

Usefull block list can be found [here](https://firebog.net/)


## Local DNS configuration with ssl certificates

The following step will allow you to access the services on your server via an unique name, the services will only be accessible under your local network, access from outside your local network is not in the scope of the project. Remeber to set the server ip as a secondory dns on your modem router. Disclaimer: Connection to webUI services may be slow, did not identify cause

### Acquire a domain

- Free at [duckdns](https://www.duckdns.org/)
- Purchasing one, i.e. at [cloudfare](https://www.cloudflare.com) or at [porkbun](https://porkbun.com/) 

### Pihole

- Under Local DNS, set an entry with as Domain the domain you purchased i.e demo.net, and as IP Address the local ip of your server 
- Under CNAME, set entries for your services with as domain, the subdomain of your service i.e. jellyfin.demo.net, as target the domain you purchased i.e. demo.net

### Nginx Proxy Manager, duckdns example

- Set SLL certificate with wildcard using the token and domain you acquired on duckdns
- Set proxy hosts for your subdomain/services

Notes in proxy entries definiton:
- Domain names: yoursubdomain.demo.net, i.e. jellyfin.demo.net
- scheme: http
- Forward Hostname / IP: demo.net
- Forward Port: port of the exposed service
- In ssl: select the previously defined ssl certificate
- Do not force ssl

Usefull videos

- https://www.youtube.com/watch?v=qlcVx-k-02E
- https://www.youtube.com/watch?v=nmE28_BA83w&t=20s
- https://www.youtube.com/watch?v=hS76TQO0A8s&t=5s

### Add a new entry

- Add a cname record in pihole for your new service
- Add a new proxy host entry in NPM

### Photoprism does not detect photo, can't connect using photosync

Photoprism requires uses web socket to for communication between front and backend. Enable "Websocket Support" in its NPM proxy entry

### Can't access QBittorrent using NPM 

Turn off the following options from qbittorrent webUI:

- Options->WebUI->Security->Enable Cross-Site Request Forgery (CSRF) protection
- Options->WebUI->Security->Enable Host header validation

### Can't access Pihole using NPM

In NPM proxy host entry for pihole, go in advanced and paste the following Custom Nginx Configuration

Replace 192.168.0.1:80 with your pihole_ip:pihole_port

```
location / {
  proxy_pass http://192.168.0.1:80/admin/;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_hide_header X-Frame-Options;
  proxy_set_header X-Frame-Options "SAMEORIGIN";
  proxy_read_timeout 90;
}
location /admin {
  proxy_pass http://192.168.0.1:80/admin/;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_hide_header X-Frame-Options;
  proxy_set_header X-Frame-Options "SAMEORIGIN";
  proxy_read_timeout 90;
}
```

