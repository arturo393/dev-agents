---
mode: ask
description: "Sincronizar Git y Jira para el instalador (commit, push, comentario, worklog y registro)."
---

Sincroniza el avance técnico del instalador con Jira usando el skill git-jira-sync (scope workspace).

Entradas:
1. Issue Jira: ${input:issueKey:Clave Jira, por ejemplo ID-1373}
2. Repo path: ${input:repoPath:Ruta repo dentro del workspace, por ejemplo products/drs/sw-drsmonitoring/master-installer-v2}
3. Commit message: ${input:commitMessage:Mensaje commit (opcional)}
4. Push: ${input:push:true/false}
5. Worklog: ${input:worklog:Tiempo Jira, por ejemplo 30m (opcional)}
6. Jira comment: ${input:jiraComment:Comentario de evidencia (opcional)}

Pasos esperados:
1. Revisar git status y commits recientes.
2. Si hay commit message, crear commit no interactivo.
3. Si push=true, subir cambios.
4. Consultar estado Jira actual.
5. Si hay jiraComment, agregar comentario.
6. Si hay worklog, registrar worklog.
7. Actualizar el registro local en un archivo de trazabilidad del repo objetivo (por defecto reports/jira_sync_registry.md).
8. Entregar resumen final con antes/despues.
