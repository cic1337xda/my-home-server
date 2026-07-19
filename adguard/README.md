# AdGuard Home + Cloudflare (Hybrid DNS Setup)

Server Documentation: AdGuard Home (DNS-over-HTTPS / DNS-over-TLS)

## Environment Variables

Rename `.env.example` to `.env` and fill in your values:

| Variable | Description |
|----------|-------------|
| `CF_API_TOKEN` | Your Cloudflare API token for DNS challenges |
| `SSL_EMAIL` | Email for Let's Encrypt certificate registration |
| `DOMAIN_1` | Primary domain for DNS (e.g., dns.yourdomain.com) |
| `DOMAIN_2` | Secondary domain (optional) |
| `TZ` | Timezone (e.g., Asia/Kuala_Lumpur) |

## Architecture Overview

This project deploys a self-hosted AdGuard Home instance acting as a network-wide ad blocker and private DNS resolver. It utilizes a "Hybrid Setup" integrating Cloudflare for Dynamic DNS (DDNS) and Let's Encrypt for automated SSL provisioning via DNS challenges.

### Key Features
- **DNS-over-TLS (DoT):** Port 853 exposed for secure Android/Mobile connections
- **DNS-over-HTTPS (DoH):** Port 443 exposed for secure browser-based queries
- **Cloudflare DDNS:** Automatically updates the dynamic home IP to the DNS A-record
- **DNS Challenge SSL:** Bypasses the need for Port 80 validation, avoiding conflicts with reverse proxies

## Directory Structure

```
adguard/
├── docker-compose.yml       # Main Docker configuration
├── .env                     # (IGNORED) Contains API Tokens and Secrets
├── .env.example             # Template for environment variables
├── renew-cert.sh            # Script for Let's Encrypt SSL renewal
├── conf/                    # AdGuard configuration files
│   └── certs/               # SSL Certificates storage
└── work/                    # AdGuard operational data and query logs
```

## Port Forwarding

To allow external devices to securely query your DNS, forward these ports from your router:

| Port | Protocol | Purpose |
|------|----------|---------|
| 853 | TCP | Android Private DNS (DoT) |
| 443 | TCP/UDP | DNS-over-HTTPS (DoH/QUIC) |
| 80 | DISABLED | Not required due to DNS Challenge SSL |

## SSL Automation

SSL certificates are provisioned using Let's Encrypt via the DNS-01 Challenge. A cronjob executes `renew-cert.sh` on the 1st of every month at 4:00 AM.

## Quick Commands

```bash
# Start stack
docker compose up -d

# Stop stack
docker compose down

# View logs
docker logs -f adguardhome

# Manual SSL renewal
./renew-cert.sh
```