# System Monitor Dashboard

A live system monitoring dashboard built with Flask and containerized with Podman.

## What it does
- Shows real-time CPU usage with visual progress bar
- Shows RAM usage (used / total)
- Shows Disk usage (used / total)
- Updates automatically every 3 seconds
- Runs fully inside a container

## Tech Stack
- Python + Flask (web server)
- psutil (system stats)
- Podman (containerization)
- Docker Hub (image registry)

## Architecture
Browser → Flask API (/api/stats) → psutil reads system → JSON response → dashboard updates

## Run it yourself

Pull and run directly from Docker Hub — no setup needed:
```bash
podman run -p 5000:5000 aurora3243/system-monitor:v1
```
Then open http://localhost:5000

## Build from source
```bash
git clone https://github.com/AURORA3243/system-monitor
cd system-monitor
podman build -t system-monitor .
podman run -p 5000:5000 system-monitor
```

## Docker Hub
https://hub.docker.com/r/aurora3243/system-monitor
