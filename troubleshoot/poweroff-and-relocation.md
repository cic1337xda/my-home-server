# Server Relocation & Power Management SOP

Standard Operating Procedure for safely shutting down, relocating, and restarting the home server (ASUS X555LJ laptop).

## Phase 1: Graceful Shutdown (Before Moving)

### 1. Stop All Docker Containers Gracefully

Send a `SIGTERM` signal so all applications and databases can flush their cache to disk.

```bash
sudo docker stop $(sudo docker ps -q)
```

Wait for all containers to stop before proceeding.

### 2. Flush Remaining Data from RAM to Disk

Ensures no cached data is lost:

```bash
sync; sync; sync
```

### 3. Unmount External Drives

Release filesystems safely:

```bash
sudo umount /mnt/hdd1tb
sudo umount /mnt/backup_usb
```

If you get a "target is busy" error, check which process is using the drive:

```bash
lsof +D /mnt/hdd1tb
```

### 4. Power Off the Server

```bash
sudo poweroff
```

Wait until the fan stops spinning before unplugging any cables.

---

## Phase 2: Startup After Relocation

After plugging everything in at the new location and powering on:

### 1. Verify Disk Detection

```bash
lsblk
```

You should see all your disks listed with their sizes.

### 2. Mount Drives (Using fstab)

Mount using the `/etc/fstab` configuration (UUID-based) to avoid device name changes:

```bash
sudo mount -a
```

### 3. Verify Permissions

Check that mounted directories have correct ownership:

```bash
ls -l /mnt/
```

- Nextcloud data should be owned by `www-data` or root
- Media files should be owned by the user/group (e.g., `1000:1000`)

**Warning:** Do NOT run `chown` or `chmod -R` on mounted drives — Nextcloud is very sensitive to permission changes.

### 4. Restart Docker Daemon

```bash
sudo systemctl restart docker
```

### 5. Start All Containers

```bash
sudo docker start $(sudo docker ps -a -q)
```

Or navigate to each service directory and run:

```bash
docker compose up -d
```

---

## Verification Checklist

| Check | Command |
|-------|---------|
| Disks detected | `lsblk` |
| Drives mounted | `df -h` |
| Containers running | `docker ps` |
| Network connectivity | `ping 8.8.8.8` |
| Services accessible | `curl http://localhost:<port>` |