# Program Shutdown Web UI

A small Flask application to manage `mystartup.service` and the automatic shutdown schedule.

## Features

- Enable or disable `mystartup.service`
- Start or stop the service manually
- Reschedule the shutdown time
- Cancel a pending shutdown (`shutdown -c`)
- Script for generating service which starts application at startup

### Run app locally

```bash
sudo python3 app.py
```

Then open:

```text
http://localhost:5000
```