echo creating folders "in" home
echo -e "\n"
echo creating media folders "if" it does not exist
if [ ! -d "~/media" ] then mkdir ~/media fi
if [ ! -d "~/media/movies" ] then mkdir ~/media/movies
if [ ! -d "~/media/shows" ] then mkdir ~/media/shows fi
mkdir -p ~/jellyfin
mkdir -p ~/sonar
mkdir -p ~/radar
mkdir -p ~/qbittorrent
mkdir -p ~/filebrowser
mkdir -p ~/jackett