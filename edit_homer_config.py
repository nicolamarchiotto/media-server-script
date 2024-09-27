import yaml

env_file_path = ".env"  # Replace with the path to your file

config_values = {}
with open(env_file_path, "r") as file:
    for line in file:
        key, value = line.strip().split(" = ")
        key = key.strip()
        value = value.strip()
        config_values[key] = value

print(config_values)

homer_file_path = "homer-config/assets/config.yml"

with open(homer_file_path, "r") as file:
    data = yaml.safe_load(file)

# Updating the URL field in the services section

endpoint = ''
if 'DNS_ENTRY' in config_values:
    endpoint = 'http://'+str(config_values["DNS_ENTRY"])
else:
    endpoint = 'http://'+str(config_values["IP"])


if "services" in data:
    for group in data["services"]:
        if "items" in group:
            for service in group["items"]:
                if "url" in service:
                    name = service["name"]
                    if name == "Jellyfin":
                        service["url"] = endpoint+":"+str(config_values["JELLYFIN_PORT"])+"/web/index.html#!/home.html"
                    elif name == "Sonarr":
                        service["url"] = endpoint+":"+str(config_values["SONARR_PORT"])+"/"
                    elif name == "Radarr":
                        service["url"] = endpoint+":"+str(config_values["RADARR_PORT"])+"/"
                    elif name == "qBittorrent":
                        service["url"] = endpoint+":"+str(config_values["QBITTORRENT_PORT"])
                    elif name == "File Browser":
                        service["url"] = endpoint+":"+str(config_values["FILEBROWSER_PORT"])+"/files/"
                    elif name == "Jackett":
                        service["url"] = endpoint+":"+str(config_values["JACKETT_PORT"])+"/"
                    elif name == "Photoprism":
                        service["url"] = endpoint+":"+str(config_values["PHOTOPRISM_PORT"])+"/library/browse"
                    elif name == "Pihole":
                        service["url"] = endpoint+":"+str(config_values["PIHOLE_PORT"])+"/admin"
                    else:
                        print("Unmanaged case, exit", name)
                        exit()
                    
with open(homer_file_path, "w") as file:
    yaml.dump(data, file)