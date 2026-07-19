# Disk Health & Management (Linux/Debian)

Reference guide for monitoring and maintaining disk health on the home server.

## 1. Identifying Disks

Before performing any operations, identify the correct disk name:

```bash
# Tree view (easiest to read)
lsblk

# Detailed view with model & serial
sudo fdisk -l
```

Typical naming convention:

| Device | Description |
|--------|-------------|
| `/dev/sda` | First disk (usually OS or SSD) |
| `/dev/sdb` | Second disk (external/extra storage) |
| `/dev/sdc` | Third disk... and so on |

## 2. Installing Smartmontools

```bash
sudo apt update && sudo apt install smartmontools -y
```

## 3. Checking Disk Health (SMART)

### Internal SATA Disks

```bash
sudo smartctl -a /dev/sdb
```

### External USB Disks

If the above fails with "Unknown device type":

```bash
# Option 1: SAT (SCSI to ATA Translation)
sudo smartctl -a -d sat /dev/sdb

# Option 2: SCSI
sudo smartctl -a -d scsi /dev/sdb
```

## 4. Interpreting Results

### Overall Status
Look for: `SMART overall-health self-assessment test result`
- **PASSED** = Disk is healthy
- **FAILED** = Disk is failing — backup data immediately

### Critical Attributes (RAW_VALUE column)

| ID | Attribute | Expected Value | Meaning if > 0 |
|----|-----------|----------------|----------------|
| 5 | Reallocated_Sector_Ct | 0 | Physical damage exists |
| 197 | Current_Pending_Sector | 0 | Data stuck due to bad sectors |
| 198 | Offline_Uncorrectable | 0 | Unrepairable damage |
| 199 | UDMA_CRC_Error_Count | 0 | Faulty cable or port |

### Age & Runtime
Look for ID# 9 (Power_On_Hours). Divide by 24 for days, by 8760 for years.

## 5. Running Self-Tests

### Short Test (2-5 minutes)
Checks the electronic board and basic mechanics:

```bash
sudo smartctl -t short /dev/sdb
```

### Long Test (hours, depends on size)
Scans every sector from start to finish:

```bash
sudo smartctl -t long /dev/sdb
```

### View Test Results
Run `sudo smartctl -a /dev/sdb` again and check the "Self-test execution status" section.

## 6. Automation

### Netdata Monitoring
Netdata auto-detects S.M.A.R.T. stats. Open Dashboard > Right Menu > Disks > Smartd.

### Scheduled Monthly Check (Cron)
```bash
0 4 1 * * /usr/sbin/smartctl -t short /dev/sdb
```