---
description: 'Ansible conventions and best practices'
applyTo: '**/*.yaml, **/*.yml'
---

# Ansible Conventions and Best Practices

## General Instructions

- Use Ansible to configure and manage infrastructure.
- Use version control for your Ansible configurations.
- Keep things simple; only use advanced features when necessary
- Give every play, block, and task a concise but descriptive `name`
  - Start names with an action verb that indicates the operation being performed, such as "Install," "Configure," or "Copy"
  - Capitalize the first letter of the task name
  - Omit periods from the end of task names for brevity
  - Omit the role name from role tasks; Ansible will automatically display the role name when running a role
  - When including tasks from a separate file, you may include the filename in each task name to make tasks easier to locate (e.g., `<TASK_FILENAME> : <TASK_NAME>`)
- Use comments to provide additional context about **what**, **how**, and/or **why** something is being done
  - Don't include redundant comments
- Use dynamic inventory for cloud resources
  - Use tags to dynamically create groups based on environment, function, location, etc.
  - Use `group_vars` to set variables based on these attributes
- Use idempotent Ansible modules whenever possible; avoid `shell`, `command`, and `raw`, as they break idempotency
  - If you have to use `shell` or `command`, use the `creates:` or `removes:` parameter, where feasible, to prevent unnecessary execution
- Use [fully qualified collection names (FQCN)](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html#term-Fully-Qualified-Collection-Name-FQCN) to ensure the correct module or plugin is selected
  - Use the `ansible.builtin` collection for [builtin modules and plugins](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#plugin-index)
- Group related tasks together to improve readability and modularity
- For modules where `state` is optional, explicitly set `state: present` or `state: absent` to improve clarity and consistency
- Use the lowest privileges necessary to perform a task
  - Only set `become: true` at the play level or on an `include:` statement, if all included tasks require super user privileges; otherwise, specify `become: true` at the task level
  - Only set `become: true` on a task if it requires super user privileges

## Secret Management

- When using Ansible alone, store secrets using Ansible Vault
  - Use the following process to make it easy to find where vaulted variables are defined
    1. Create a `group_vars/` subdirectory named after the group
    2. Inside this subdirectory, create two files named `vars` and `vault`
    3. In the `vars` file, define all of the variables needed, including any sensitive ones
    4. Copy all of the sensitive variables over to the `vault` file and prefix these variables with `vault_`
    5. Adjust the variables in the `vars` file to point to the matching `vault_` variables using Jinja2 syntax: `db_password: "{{ vault_db_password }}"`
    6. Encrypt the `vault` file to protect its contents
    7. Use the variable name from the `vars` file in your playbooks
- When using other tools with Ansible (e.g., Terraform), store secrets in a third-party secrets management tool (e.g., Hashicorp Vault, AWS Secrets Manager, etc.)
  - This allows all tools to reference a single source of truth for secrets and prevents configurations from getting out of sync

## Style

- Use 2-space indentation and always indent lists
- Separate each of the following with a single blank line:
  - Two host blocks
  - Two task blocks
  - Host and include blocks
- Use `snake_case` for variable names
- Sort variables alphabetically when defining them in `vars:` maps or variable files
- Always use multi-line map syntax, regardless of how many pairs exist in the map
  - It improves readability and reduces changeset collisions for version control
- Prefer single quotes over double quotes
  - The only time you should use double quotes is when they are nested within single quotes (e.g. Jinja map reference), or when your string requires escaping characters (e.g., using "\n" to represent a newline)
  - If you must write a long string, use folded block scalar syntax (i.e., `>`) to replace newlines with spaces or literal block scalar syntax (i.e., `|`) to preserve newlines; omit all special quoting
- The `host` section of a play should follow this general order:
  - `hosts` declaration
  - Host options in alphabetical order (e.g., `become`, `remote_user`, `vars`)
  - `pre_tasks`
  - `roles`
  - `tasks`
- Each task should follow this general order:
  - `name`
  - Task declaration (e.g., `service:`, `package:`)
  - Task parameters (using multi-line map syntax)
  - Loop operators (e.g., `loop`)
  - Task options in alphabetical order (e.g. `become`, `ignore_errors`, `register`)
  - `tags`
- For `include` statements, quote filenames and only use blank lines between `include` statements if they are multi-line (e.g., they have tags)

## Linting

- Use `ansible-lint` and `yamllint` to check syntax and enforce project standards
- Use `ansible-playbook --syntax-check` to check for syntax errors

## Error Handling

- Use `ignore_errors: true` only when a task is genuinely optional (e.g., an apt fallback when the artifact bundle is the primary source); always add a comment explaining why
- For tasks that may safely fail, prefer `failed_when: false` over `ignore_errors: true` when you still want to capture the result via `register`
- When chaining multiple fallback strategies (artifact → apt → git), each fallback task must have `ignore_errors: true` and a comment identifying it as a fallback

## Tags

- Assign tags to every task so sections can be run independently with `--tags`
- Use consistent tag names that reflect functional sections, not playbook filenames:
  - `admin_user`, `icinga_modules`, `director`, `network_maps`, `drsconfig`, `graphite`, `theme`, `ssh_keys`, `permissions`, `monitoring`
- A task may have multiple tags when it is shared between sections (e.g., `tags: [theme, drsconfig]`)

## DRS Installer Project Conventions

Rules specific to `products/drs/sw-drsmonitoring/master-installer-v2/`:

- **Offline-first**: always prefer copying from `{{ drs_artifacts_root }}/src/...` before falling back to `apt`, `git clone`, or network sources. Document online-only fallbacks with a `# ONLINE FALLBACK:` comment.
- **Module installation order**: artifact bundle → apt (`--reinstall`) → git clone. Never use bare `git:` as the only install method for a production module.
- **MySQL auth**: use `login_unix_socket: /var/run/mysqld/mysqld.sock` on all `community.mysql.*` tasks executed as root — `/root/.my.cnf` handles credentials. Never pass `{{ mysql_root_password }}` in a `shell:` command (it appears in Ansible logs).
- **community.mysql FQCN**: always use `community.mysql.mysql_db` and `community.mysql.mysql_user` — never bare `mysql_db` or `mysql_user`.
- **Module enablement**: enable IcingaWeb2 modules via `ansible.builtin.file state=link` under `/etc/icingaweb2/enabledModules/`. `icingacli module enable` does not exist in IcingaWeb2 2.x.
- **Secrets in URLs**: never embed `gitlabuser:gitlabpassword` in a `git:` `repo:` URL. Pre-download in the offline bundle instead.
- **`changed_when`**: set `changed_when: false` on `systemd daemon_reload` tasks; set `changed_when: true` only on `shell`/`command` tasks that always make a change (e.g., `chown`, `chmod`).
- **`remote_src`**: always use boolean `true`/`false`, never `yes`/`no`.
- Use `ansible-playbook --check --diff` to perform a dry-run of playbook execution

<!-- 
These guidelines were based on, or copied from, the following sources:

- [Ansible Documentation - Tips and Tricks](https://docs.ansible.com/ansible/latest/tips_tricks/index.html)
- [Whitecloud Ansible Styleguide](https://github.com/whitecloud/ansible-styleguide)
-->
