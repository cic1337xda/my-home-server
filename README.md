# pwn20wnd's Homelab — Self-Hosted Infrastructure on Bare Metal

[![Debian](https://img.shields.io/badge/OS-Debian%2013%20(Trixie)-A81D33?style=flat&logo=debian)](https://www.debian.org/)
[![Docker](https://img.shields.io/badge/Containerization-Docker%20%26%20Compose-2496ED?style=flat&logo=docker)](https://www.docker.com/)
A comprehensive, self-hosted Docker infrastructure deployed on a bare-metal laptop (ASUS X555LJ). This repository showcases the architecture, configuration, and services powering my home server — built with a strong emphasis on security, privacy, automation, and media management.

---

## Hardware Specifications

| Component | Detail |
|-----------|--------|
| **Model** | ASUS X555LJ (Used Laptop) |
| **CPU** | Intel Core i7-5500U (4 cores @ 3.00 GHz) |
| **GPU** | NVIDIA GeForce 920M + Intel HD Graphics 5500 |
| **RAM** | 11.59 GB (6.10 GB in use) |
| **Storage** | 466.95 GB SSD (ext4) |
| **External** | 915.82 GB HDD (ext4) + 57.76 GB USB (exfat) |

---

## Architecture Overview

```
                           ┌─────────────────────────────────┐
                           │         Cloudflare Tunnel        │
                           │    (Proxy / SSL / DDNS)          │
                           └────────────┬────────────────────┘
                                        │
                           ┌────────────▼────────────────────┐
                           │   Nginx Proxy Manager (NPM)      │
                           │   Reverse Proxy / SSL Terminator │
                           └────────────┬────────────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
 ┌────────▼────────┐          ┌─────────▼────────┐         ┌─────────▼────────┐
 │   Security      │          │   Monitoring      │         │   Media Stack    │
 │  ─────────────  │          │  ───────────────  │         │  ───────────────  │
 │  • CrowdSec IPS │          │  • Grafana        │         │  • qBittorrent   │
 │  • AdGuard Home │          │  • Netdata        │         │  • Prowlarr      │
 │  • Cloudflare   │          │  • Prometheus     │         │  • Radarr/Sonarr │
 │  • UFW          │          │                   │         │  • Jellyfin      │
 └─────────────────┘          └───────────────────┘         └───────────────────┘
                                                                        │
          ┌─────────────────────────────┬─────────────────────────────┐
          │                             │                             │
 ┌────────▼────────┐          ┌─────────▼────────┐         ┌─────────▼────────┐
 │  Cloud & Tools  │          │  Automation       │         │  Infrastructure  │
 │  ─────────────  │          │  ───────────────  │         │  ───────────────  │
 │  • Nextcloud    │          │  • n8n            │         │  • Portainer     │
 │  • Immich       │          │  • FlareSolverr   │         │  • Glance        │
 │  • Stirling-PDF │          │  • DDNS           │         │  • Code-Server   │
 │  • Open WebUI   │          │                   │         │  • pgAdmin       │
 │  • OnlyOffice   │          │                   │         │                  │
 └─────────────────┘          └───────────────────┘         └───────────────────┘
```

---

## Services

### 🔐 Security & Networking
| Service | Description |
|---------|-------------|
| [Nginx Proxy Manager](npm/) | Reverse proxy with SSL termination |
| [CrowdSec](crowdsec/) | Hybrid IPS (Docker Agent + Host Bouncer) |
| [AdGuard Home](adguard/) | Network-wide ad blocking & DNS privacy |
| [Cloudflare DDNS](ddns/) | Dynamic DNS updater |

### 📊 Monitoring & Telemetry
| Service | Description |
|---------|-------------|
| [Grafana & Prometheus](graphana/) | Real-time hardware & service metrics |
| [Netdata](netdata/) | High-resolution host monitoring |

### 🎬 Media Stack (The \*arr Ecosystem)
| Service | Description |
|---------|-------------|
| qBittorrent | Download client |
| Prowlarr | Indexer manager |
| Radarr | Movie automation |
| Sonarr | TV series automation |
| Lidarr | Music management |
| Bazarr | Subtitle management |
| Jellyfin | Media streaming server |
| [FlareSolverr](flaresolverr/) | Cloudflare bypass proxy |

### ☁️ Cloud & Productivity
| Service | Description |
|---------|-------------|
| [Nextcloud](nextcloud/) | File sync & sharing with OnlyOffice |
| [Immich](immich/) | AI-powered photo backup (Google Photos alternative) |
| [Stirling-PDF](stirling-pdf/) | Offline PDF manipulation |
| [Open WebUI](open-webui/) | LLM chat interface (OpenRouter) |

### ⚙️ Automation & Management
| Service | Description |
|---------|-------------|
| [n8n](n8n-docker/) | Workflow automation |
| [Portainer](portainer/) | Docker container management |
| [Glance](glance/) | Unified homelab dashboard |
| [Code-Server](code-server/) | VS Code in browser |
| [pgAdmin](pgadmin/) | PostgreSQL administration |

### 🛠️ Networking
| Service | Description |
|---------|-------------|
| [9Router](9Router/) | Custom router management |

---

## Security Practices

- **All `.env` files** containing passwords, API keys, and tokens are excluded from version control via `.gitignore` (`.env.example` templates provided for reference).
- **CrowdSec Hybrid Architecture:** Docker agent parses NPM logs; host-level bouncer enforces bans via iptables/nftables — even if Docker fails, protection remains active.
- **Cloudflare Proxy + SSL:** All public-facing traffic is routed through Cloudflare with Full (Strict) SSL encryption.
- **Application data volumes** (databases, user data, logs, certificates) are strictly excluded from the repository.

---

## Getting Started

### Prerequisites
- Docker Engine & Docker Compose
- A domain name with Cloudflare DNS
- Basic networking knowledge

### Quick Start

```bash
# Clone the repository
git clone https://github.com/pwn20wnd/docker-containers.git
cd docker-containers

# Copy and configure environment variables
cp adguard/.env.example adguard/.env
# ... repeat for each service

# Start a service
cd adguard && docker compose up -d
```

Each service directory contains its own `README.md` with detailed setup instructions and a `.env.example` template.

---

## Project Structure

```
docker-containers/
├── 9Router/              # Custom router configuration
├── adguard/              # AdGuard Home DNS
├── code-server/          # VS Code in browser
├── crowdsec/             # IPS security
├── ddns/                 # Cloudflare DDNS
├── flaresolverr/         # Cloudflare bypass
├── glance/               # Homelab dashboard
├── graphana/             # Monitoring stack
├── immich/               # Photo backup
├── media-server/         # *arr stack + Jellyfin
├── n8n-docker/           # Workflow automation
├── netdata/              # System monitoring
├── nextcloud/            # File sync & share
├── npm/                  # Nginx Proxy Manager
├── open-webui/           # LLM interface
├── pgadmin/              # Database admin
├── portainer/            # Docker management
├── stirling-pdf/         # PDF tools
├── troubleshoot/         # Personal notes & scripts
├── backup/               # Archived files (gitignored)
├── client-projects/      # Portfolio projects
├── .gitignore            # Git exclusion rules
└── README.md             # This file
```

