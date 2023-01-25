sudo docker run -d \
    --name filebrowser \
    -p 8081:8080 \
    -v ~:/data \
    -v ~/dockers/filebrowser:/config \
    --restart unless-stopped \
    hurlenko/filebrowser
