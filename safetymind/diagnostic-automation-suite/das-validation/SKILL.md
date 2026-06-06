---
name: DAS Validation Agent
description: Validates webhook health, agent health, container status, and n8n configuration for SafetyMind Diagnostic Automation Suite.
---

# DAS Validation Agent

1. **SKILL.md** — revisión dinámica del ecosistema DAS
2. **`python3 agent.py discover`** — descubre servidor, contenedores + ejecuta auditorías
3. **Aprendizaje** — codificá nuevos failure modes

## 1. Revisión Dinámica

### Webhooks n8n

```bash
# Diagnóstico V2
curl -v http://100.74.53.2:5679/webhook/diagnostico-v2 2>&1 | head -30

# Approval V2
curl -v http://100.74.53.2:5679/webhook/approval-v2 2>&1 | head -30

# ¿Qué workflows están activos?
ssh arturo@100.74.53.2 "docker exec -i das-n8n-db mysql -u n8n -pn8n_password n8n -e \"select id,name,active from workflow_entity\""
```

### SQL: Verificar webhookId y nodos

```bash
ssh arturo@100.74.53.2 "docker exec -i das-n8n-db mysql -u n8n -pn8n_password n8n -e \"
SELECT we.id, we.name, we.active,
  JSON_EXTRACT(wn.resources, '\\$.webhookId') AS webhookId
FROM workflow_entity we
JOIN workflow_history wn ON wn.workflowId = we.id
WHERE we.name LIKE '%Diagnóstico%' OR we.name LIKE '%Aprobación%'
ORDER BY we.id;
\""
```

### Agente

```bash
# Health check
curl -s http://100.74.53.2:8002/health | python3 -m json.tool

# Últimos logs
ssh arturo@100.74.53.2 "docker logs das-agent --tail 20"
```

### Contenedores

```bash
ssh arturo@100.74.53.2 "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Auditorías Estáticas

```bash
# Todas las auditorías
python3 agent.py audit
```

Cada auditoría:
- **webhook** — prueba `diagnostico-v2` y `approval-v2` endpoints
- **agent** — verifica `/health` y reporta status
- **containers** — lista contenedores Docker y su estado

## 4. Aprendizaje

Si descubrís un nuevo failure mode (webhook caído, contenedor muerto, error de expresión n8n), codificalo:

```bash
echo '# $(date): nuevo failure mode' >> scripts/check-webhook.sh
```

Luego documentá el patrón en `SKILL.md` sección 1 para que el próximo análisis lo capture automáticamente.
