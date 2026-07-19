# High Swap Memory Usage — Optimization Guide

Troubleshooting log for resolving critical swap memory alerts on a 12GB RAM Docker media server.

## Problem Description

- **Symptom:** Netdata sent "Critical Alert: System swap memory utilization = 100%"
- **Root Cause:**
  1. qBittorrent downloading multiple files simultaneously
  2. RAM (12GB) filled up with file cache
  3. Default swap file was too small, causing potential system hang

## Solution Summary

- **A:** Increase swap file size from default to 16GB
- **B:** Optimize swappiness value to prioritize physical RAM
- **C:** Limit qBittorrent memory usage

---

## A: Increase Swap Size to 16GB

Prerequisite: Ensure SSD has >20GB free space (`df -h /`)

```bash
# 1. Disable current swap
sudo swapoff -a

# 2. Remove old swap file (if exists)
sudo rm /swapfile

# 3. Create new 16GB swap file
sudo fallocate -l 16G /swapfile

# 4. Set secure permissions (root only)
sudo chmod 600 /swapfile

# 5. Initialize swap area
sudo mkswap /swapfile

# 6. Enable the new swap
sudo swapon /swapfile

# 7. Make permanent (add to /etc/fstab)
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## B: Optimize Swappiness

Goal: Force Linux to use RAM until almost full before touching swap.

```bash
# 1. Check current value (default is usually 60)
cat /proc/sys/vm/swappiness

# 2. Set to 10 (temporary)
sudo sysctl vm.swappiness=10

# 3. Make permanent
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
```

---

## C: Limit Application Memory (qBittorrent)

Goal: Prevent qBittorrent from hogging all available RAM for caching.

Navigate to: qBittorrent WebUI > Tools > Options > Advanced

| Setting | Value |
|---------|-------|
| Disk Cache | Manual: 256 MiB |
| Physical memory (RAM) usage limit | Enable, set to 1024 MiB (1GB) |

Save settings after making changes.

---

## Verification

```bash
# 1. Check swap size
free -h
# Expected: Swap: 15Gi or 16Gi

# 2. Check swappiness
cat /proc/sys/vm/swappiness
# Expected: 10

# 3. Check Docker stats
docker stats
# qBittorrent should stabilize around ~1GB usage
```