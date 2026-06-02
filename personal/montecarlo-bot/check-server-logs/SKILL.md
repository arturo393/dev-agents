---
name: Check Server Logs
description: Log fetcher and analyzer. SKILL.md = dynamic log analysis. agent.py = static fetcher.
---

# Check Server Logs

1. **SKILL.md** — análisis dinámico de logs (patrones, errores, crashes)
2. **`python3 agent.py discover`** — descubre log files, cuenta errores + fetch
3. **Aprendizaje** — codificá nuevos patrones de error

## 1. Revisión Dinámica

```bash
ssh arturo@100.74.53.2 "
  # Spikes de error
  echo '=== Error rate (last 1000 lines) ==='
  tail -1000 /home/arturo/monteCarlo/data/logs/bot_production.log 2>/dev/null |
    grep -oP '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}' | sort | uniq -c | tail -10

  # Rate limiting
  echo '=== 429 count ==='
  grep -c '429\|Too Many\|rate.*limit' /home/arturo/monteCarlo/data/logs/bot_production.log 2>/dev/null

  # Crash timeline
  echo '=== Restarts ==='
  grep -n 'starting\|Starting\|SIGSEGV\|SIGABRT\|SIGINT' \
    /home/arturo/monteCarlo/data/logs/bot_production.log 2>/dev/null | tail -10
"
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Fetch Estático

```bash
python3 agent.py fetch_logs           # default: 100 lines
python3 agent.py --lines 500          # custom lines
```

## 4. Aprendizaje

Si descubrís un nuevo patrón de error, codificalo:
```bash
echo '# $(date): nuevo log pattern' >> scripts/fetch_logs.sh
```
