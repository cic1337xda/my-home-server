# CrowdSec + Nginx Proxy Manager (Hybrid IPS)

Server Documentation: CrowdSec Hybrid Security Architecture

## Environment Variables

Rename `.env.example` to `.env` and fill in your values:

| Variable | Description |
|----------|-------------|
| `TZ` | Timezone (e.g., Asia/Kuala_Lumpur) |
| `GID` | System Group ID (run `id` command) |
| `NPM_LOGS_DIR` | Path to NPM access logs |
| `CROWDSEC_LAPI_PORT` | Local API port (default: 8082) |
| `API_KEY` | CrowdSec API key for the firewall bouncer |

## Architecture Overview

This deployment utilizes a "Hybrid" security architecture:

- **[A] The Agent (Log Parser):** Runs containerized via Docker. Analyzes access logs from Nginx Proxy Manager (NPM).
- **[B] The Bouncer (Firewall):** Runs natively on the Host OS via systemd. Enforces IP bans at the kernel level (iptables/nftables).

This architecture guarantees that even if the Docker daemon fails, the Host Firewall remains active.

## Directory Structure

```
crowdsec/
├── docker-compose.yml       # Main Docker configuration
├── .env                     # (IGNORED) Contains secrets
├── .env.example             # Template for environment variables
├── acquis.yaml              # Log acquisition configuration
├── config/                  # CrowdSec parsers, scenarios, collections
└── data/                    # CrowdSec operational data
```

## Operational Commands

All `cscli` commands must be executed via `docker exec`:

```bash
# List active bouncers
docker exec crowdsec cscli bouncers list

# View active bans
docker exec crowdsec cscli decisions list

# Manually ban an IP
docker exec crowdsec cscli decisions add --ip 1.2.3.4 --reason "Manual"

# Remove a ban
docker exec crowdsec cscli decisions delete --ip 1.2.3.4

# Update threat intelligence
docker exec crowdsec cscli hub update
docker exec crowdsec cscli hub upgrade
```

## Troubleshooting

```bash
# Check host bouncer logs
tail -n 50 /var/log/crowdsec-firewall-bouncer.log

# Restart host bouncer
systemctl restart crowdsec-firewall-bouncer

# Restart Docker agent
docker compose restart crowdsec
```