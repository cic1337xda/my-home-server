# Nextcloud + OnlyOffice (Cloudflare Optimized)

Enterprise-grade file synchronization and sharing platform with real-time document editing.

## Environment Variables

Rename `.env.example` to `.env` and fill in your values:

| Variable | Description |
|----------|-------------|
| `TZ` | Timezone (e.g., Asia/Kuala_Lumpur) |
| `NEXTCLOUD_ROOT_DIR` | Root data directory for Nextcloud |
| `NEXTCLOUD_DOMAIN` | Domain (e.g., nextcloud.yourdomain.com) |
| `NEXTCLOUD_PORT` | Port mapping |
| `ONLYOFFICE_PORT` | OnlyOffice document server port |
| `MYSQL_ROOT_PASSWORD` | MariaDB root password |
| `MYSQL_DATABASE` | Database name |
| `MYSQL_USER` | Database user |
| `MYSQL_PASSWORD` | Database user password |
| `ONLYOFFICE_JWT_SECRET` | JWT secret for OnlyOffice |

## Architecture & Setup

### Reverse Proxy (Cloudflare) Configuration

Essential settings to append to `/var/www/html/config/config.php`:

```php
'trusted_proxies' => ['172.16.0.0/12', '192.168.0.0/16', '10.0.0.0/8'],
'overwritehost' => 'nextcloud.yourdomain.com',
'overwriteprotocol' => 'https',
'overwrite.cli.url' => 'https://nextcloud.yourdomain.com',

'memcache.distributed' => '\\OC\\Memcache\\Redis',
'memcache.locking' => '\\OC\\Memcache\\Redis',
'redis' => array(
  'host' => 'redis',
  'password' => '',
  'port' => 6379,
),

'maintenance_window_start' => 2,
'default_phone_region' => 'MY',
```

## Maintenance (OCC Commands)

```bash
# Manual upgrade
docker exec -u www-data nextcloud-app php occ upgrade

# Disable maintenance mode
docker exec -u www-data nextcloud-app php occ maintenance:mode --off

# Repair missing indices
docker exec -u www-data nextcloud-app php occ db:add-missing-indices

# Repair file cache
docker exec -u www-data nextcloud-app php occ maintenance:repair --include-expensive

# Disable problematic apps
docker exec -u www-data nextcloud-app php occ app:disable app_api
```

## Troubleshooting

- **Upgrade stuck at richdocumentscode?** Disable the app and re-run upgrade.
- **"Maintenance Mode" loop?** Run `maintenance:mode --off`.
- **Transactional file locking errors?** Ensure Redis container is running.
- **Background jobs not running?** Check the `nextcloud-cron` container is active.
