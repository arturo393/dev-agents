#!/bin/bash
# Check n8n webhook health
set -euo pipefail

HOST="100.74.53.2"
N8N_URL="http://${HOST}:5679"

echo "=== Webhook Health Check ==="

# Diagnóstico V2
echo -n "diagnostico-v2: "
CODE=$(curl -s -o /dev/null -w "%{http_code}" "${N8N_URL}/webhook/diagnostico-v2" 2>/dev/null || echo "000")
echo "${CODE}"

# Approval V2
echo -n "approval-v2: "
CODE=$(curl -s -o /dev/null -w "%{http_code}" "${N8N_URL}/webhook/approval-v2" 2>/dev/null || echo "000")
echo "${CODE}"

# n8n healthz
echo -n "n8n healthz: "
CODE=$(curl -s -o /dev/null -w "%{http_code}" "${N8N_URL}/healthz" 2>/dev/null || echo "000")
echo "${CODE}"

# WebhookId verification via DB
echo ""
echo "=== WebhookId in DB ==="
ssh "arturo@${HOST}" "docker exec -i das-n8n-db mysql -u n8n -pn8n_password n8n -e \"
SELECT we.id, we.name, we.active,
  JSON_EXTRACT(wn.resources, '\\\$.webhookId') AS webhookId
FROM workflow_entity we
JOIN workflow_history wn ON wn.workflowId = we.id
WHERE we.name LIKE '%Diagnóstico%' OR we.name LIKE '%Aprobación%'
ORDER BY we.id;
\"" 2>/dev/null || echo "DB query failed"
