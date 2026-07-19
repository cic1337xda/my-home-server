# Utility Scripts Overview

Python helper scripts for maintaining and managing the Docker homelab environment.

---

## `restart_all.py` — Rolling Restart Protocol

**Purpose:** Safely restarts all Docker Compose projects in the repository.

**Workflow:**
1. Iterates through every subdirectory in `docker-containers/`
2. For each directory containing a `docker-compose.yml`, runs `docker compose down`
3. Then runs `docker compose up -d` to reinitialize with updated configs

**Use case:** After making global configuration changes (e.g., updating `.env` files across multiple services), run this script to apply all changes at once instead of restarting each service individually.

**Usage:**
```bash
python3 troubleshoot/restart_all.py
```

---

## `check_tz.py` — Timezone Compliance Checker

**Purpose:** Audits all Docker Compose files to ensure every service has the correct timezone configured (`Asia/Kuala_Lumpur`).

**What it checks:**
- `environment` block for `TZ=Asia/Kuala_Lumpur` (both dict and list formats)
- `volumes` block for `/etc/localtime:/etc/localtime` bind mounts (alternative method)

**Output:** Lists any services missing the timezone configuration, making it easy to identify and fix compliance gaps.

**Usage:**
```bash
python3 troubleshoot/check_tz.py
```

---

## `fix_tz.py` — Automated Timezone Remediation

**Purpose:** Automatically injects the correct timezone (`Asia/Kuala_Lumpur`) into any Docker Compose service that is missing it.

**Safety features:**
- Creates a `.bak` backup of the original file before modification
- Only modifies files that are non-compliant
- Supports both list and dict format environment variables

**Use case:** After running `check_tz.py` and identifying non-compliant services, run this script to fix them all automatically.

**Usage:**
```bash
python3 troubleshoot/fix_tz.py
```

**Note:** After running this script, you must restart the affected containers:
```bash
docker compose down && docker compose up -d
```