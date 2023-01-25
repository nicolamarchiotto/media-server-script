sudo docker run -d \
    --name filebrowser \
    -p 8081:8080 \
    -v /home/altair:/data \
    -v /home/altair/filebrowser:/config \
    --restart unless-stopped \
    hurlenko/filebrowser
