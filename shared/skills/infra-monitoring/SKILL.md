---
name: Infrastructure Monitoring
description: Audits the full monitoring stack: Docker, Prometheus, Grafana, Portal, Node Exporter, DWService tunnel, and system resources.
---

# Infrastructure Monitoring

This skill checks the health of the entire infrastructure stack running on the master node (192.168.1.149).

## Usage

### Full Stack Check
```bash
./.agent/skills/infrastructure_monitoring/scripts/check_all.sh
```

### Individual Checks
```bash
# Docker containers + healthchecks
./.agent/skills/infrastructure_monitoring/scripts/check_stack.sh

# System resources (disk, RAM, CPU, uptime)
./.agent/skills/infrastructure_monitoring/scripts/check_system.sh

# DWService tunnel status
./.agent/skills/infrastructure_monitoring/scripts/check_dwservice.sh
```

## What It Checks
- **Docker Stack:** All containers (portal, prometheus, grafana, node-exporter, watchdog, traefik, DAS, AR) — status, ports, health
- **Prometheus:** Scrape targets, remote-write receiver, TSDB status
- **Grafana:** API health, dashboard provisioning
- **Portal:** API /api/health endpoint
- **System Resources:** Disk usage, RAM, CPU load, uptime
- **DWService Tunnel:** Remote access agent persistence
