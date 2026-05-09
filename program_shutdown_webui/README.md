# Program Shutdown Web UI

A small Flask application to manage `mystartup.service` and the scheduled shutdown time.

## Features

- Enable or disable `mystartup.service`
- Manually start or stop `mystartup.service`
- Shutdown and reboot system in a minute
- Cancel scheduled reboot and shutdown time
- Change `mystartup.service` shutdown scheduled time  
- Reschedule active shutdown time

## Install

- Run install_flask_service.sh, script for generating service which starts Flask app at startup

### Debug

```bash
sudo python3 app.py
```

Then open:

```text
http://localhost:5000
```