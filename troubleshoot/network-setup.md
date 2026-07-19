# Docker Network Setup (Bridge Network)

Guide for creating and configuring a dedicated Docker bridge network for inter-container communication.

## 1. Overview

This setup creates a dedicated bridge network allowing Nginx Proxy Manager (NPM) to communicate with other containers using their container names instead of IP addresses.

## 2. Create the Network

Run this once:

```bash
docker network create pwn20wnd-network
```

## 3. Configure Nginx Proxy Manager

Add the network to your NPM `docker-compose.yml`:

```yaml
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    container_name: nginx-proxy-manager
    # ... other settings ...
    networks:
      - default
      - pwn20wnd-network

networks:
  pwn20wnd-network:
    external: true
```

## 4. Configure Backend Containers

For every container you want to expose:

```yaml
services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    # ... other settings ...
    networks:
      - pwn20wnd-network

networks:
  pwn20wnd-network:
    external: true
```

## 5. Adding a Proxy Host in NPM

When configuring a proxy host in the NPM dashboard:

| Field | Value |
|-------|-------|
| Domain Names | `subdomain.yourdomain.com` |
| Scheme | `http` |
| Forward Hostname | `portainer` (container name) |
| Forward Port | `9000` (internal app port) |

## 6. Troubleshooting

If you get "502 Bad Gateway":

1. Ensure both containers are running
2. Verify both have `pwn20wnd-network` in their networks config
3. Confirm `networks: pwn20wnd-network: external: true` is at the bottom of both files
4. Restart containers: `docker compose up -d`