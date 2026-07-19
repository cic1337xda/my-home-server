# Home Media Server (The \*arr Stack + Jellyfin)

An optimized, automated media ingestion and streaming ecosystem utilizing atomic moves (hardlinks) to conserve storage.

## Directory Structure

```
media-server/
├── docker-compose.yml       # Main configuration file
├── .env                     # (IGNORED) Environment variables
├── .env.example             # Template for environment variables
├── config/                  # App configurations (Database, Settings)
│   ├── bazarr/
│   ├── jellyfin/
│   ├── lidarr/
│   ├── prowlarr/
│   ├── qbittorrent/
│   ├── radarr/
│   └── sonarr/
├── data/                    # Storage (Hardlinks Enabled)
│   ├── torrents/            # Raw downloads from qBittorrent
│   └── media/               # Sorted media for Jellyfin
│       ├── movies/
│       ├── tv/
│       └── music/
└── synclyr2metadata/        # Metadata synchronization tool
```

## Service Access

Replace `<SERVER-IP>` with your server's local IP address.

| Service | Type | URL | Notes |
|---------|------|-----|-------|
| qBittorrent | Download Client | `http://<SERVER-IP>:8085` | Default user: admin |
| Prowlarr | Indexer Manager | `http://<SERVER-IP>:9696` | |
| Radarr | Movie Manager | `http://<SERVER-IP>:7878` | Root: /data/media/movies |
| Sonarr | TV Show Manager | `http://<SERVER-IP>:8989` | Root: /data/media/tv |
| Lidarr | Music Manager | `http://<SERVER-IP>:8686` | Root: /data/media/music |
| Bazarr | Subtitle Manager | `http://<SERVER-IP>:6767` | Provider: OpenSubtitles |
| Jellyfin | Media Player | `http://<SERVER-IP>:8096` | Libraries: movies, tv |

## Critical Configurations

### qBittorrent WebUI Fix
Add these to `config/qbittorrent/qBittorrent/qBittorrent.conf` under `[Preferences]`:
```ini
WebUI\CSRFProtection=false
WebUI\ClickjackingProtection=false
WebUI\HostHeaderValidation=false
```

### Download Client Settings (in Radarr/Sonarr)
- **Host:** qbittorrent
- **Port:** 8080 (Internal Docker port)
- **User:** admin

## Quick Commands

```bash
# Start the entire stack
docker compose up -d

# Stop the stack
docker compose down

# Restart a specific service
docker compose restart jellyfin

# View logs
docker compose logs -f qbittorrent
```