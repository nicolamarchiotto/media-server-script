import yaml

env_file_path = ".env"  # Replace with the path to your file

config_values = {}
with open(env_file_path, "r") as file:
    for line in file:
        key, value = line.strip().split(" = ")
        key = key.strip()
        value = value.strip()
        config_values[key] = value

homer_file_path = "homer-config/assets/config.yml"

with open(homer_file_path, "r") as file:
    data = yaml.safe_load(file)

# Updating the URL field in the services section
if "services" in data:
    for group in data["services"]:
        if "items" in group:
            for service in group["items"]:
                if "url" in service:
                    name = service["name"]
                    if name == "Jellyfin":
                        service["url"] = str(config_values["JELLYFIN_URL"])
                    elif name == "Sonarr":
                        service["url"] = str(config_values["SONARR_URL"])
                    elif name == "Radarr":
                        service["url"] = str(config_values["RADARR_URL"])
                    elif name == "qBittorrent":
                        service["url"] = str(config_values["QBITTORRENT_URL"])
                    elif name == "File Browser":
                        service["url"] = str(config_values["FILEBROWSER_URL"])
                    elif name == "Jackett":
                        service["url"] = str(config_values["JACKETT_URL"])
                    elif name == "Photoprism":
                        service["url"] = str(config_values["PHOTOPRISM_URL"])
                    elif name == "Pihole":
                        service["url"] = str(config_values["PIHOLE_URL"])
                    elif name == "NPM":
                        service["url"] = str(config_values["NPM_URL"])
                    elif name == "UrBackup":
                        service["url"] = str(config_values["URBACKUP_URL"])
                    else:
                        print("Unmanaged case, exit", name)
                        exit()
                    
with open(homer_file_path, "w") as file:
    yaml.dump(data, file)

print("Edit homer config succesful")
