# Nginx Proxy Manager (NPM)

Core reverse proxy handling SSL termination and subdomain routing for all services.

## Environment Variables

Rename `.env.example` to `.env` and fill in your values:

| Variable | Description |
|----------|-------------|
| `TZ` | Timezone (e.g., Asia/Kuala_Lumpur) |
| `NPM_DATA_DIR` | Data directory for NPM |
| `NPM_LETSENCRYPT_DIR` | Let's Encrypt certificates directory |
| `PORT_HTTP` | HTTP port (80) |
| `PORT_HTTPS` | HTTPS port (443) |
| `PORT_ADMIN` | Admin dashboard port (81) |

## Architecture Overview

Nginx Proxy Manager functions as the core "Reverse Proxy" for the infrastructure:

- **Ingress Traffic Routing** (Ports 80 & 443)
- **SSL/TLS Termination** (Let's Encrypt automation)
- **Subdomain routing** to backend services

All backend services connect via `pwn20wnd-network` (shared Docker network).

## Port Bindings

| Port | Protocol | Purpose |
|------|----------|---------|
| 80 | HTTP | SSL validation / redirect |
| 443 | HTTPS | Secure traffic |
| 81 | HTTP | Admin dashboard |

## Adding a New Subdomain (SOP)

### 1. DNS Configuration (Cloudflare)
- Record Type: CNAME
- Name: `service-name`
- Target: `dns.yourdomain.com`
- Proxy Status: DNS Only (Grey Cloud)

### 2. Host Firewall (UFW)
```bash
sudo ufw allow <backend-port>/tcp
```

### 3. NPM Dashboard Configuration
- Navigate to: Proxy Hosts > Add Proxy Host
- Domain Names: `service-name.yourdomain.com`
- Scheme: http
- Forward Host: Container name or IP
- Forward Port: Backend service port
- Enable: "Block Common Exploits" & "Websockets Support"

### 4. SSL/TLS
- Select: "Request a new SSL Certificate"
- Enable: "Force SSL" & "HTTP/2 Support"
- Provide email and agree to TOS

## Troubleshooting

- **502 Bad Gateway:** Backend container not reachable - verify container is running and port is correct.
- **504 Gateway Time-out:** Backend not responding in time - check host firewall and app health.
- **SSL Generation Error:** Let's Encrypt verification failed - check port 80 forwarding and DNS propagation.