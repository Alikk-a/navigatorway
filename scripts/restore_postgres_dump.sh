#!/usr/bin/env bash
# Restore navigatorway PostgreSQL from dump.sql (pg_dump plain SQL).
# Run in WSL from project root:
#   bash scripts/restore_postgres_dump.sh
#   bash scripts/restore_postgres_dump.sh /path/to/dump.sql

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DUMP="${1:-$ROOT/dump.sql}"
DB_NAME="${POSTGRES_DB:-navigatorway}"
DB_USER="${POSTGRES_USER:-navigator}"
DB_OWNER="${POSTGRES_OWNER:-$DB_USER}"

if [[ ! -f "$DUMP" ]]; then
  echo "Dump not found: $DUMP" >&2
  exit 1
fi

echo "==> Terminate connections to $DB_NAME"
sudo -u postgres psql -v ON_ERROR_STOP=1 -d postgres <<SQL
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '${DB_NAME}' AND pid <> pg_backend_pid();
SQL

echo "==> Recreate database $DB_NAME (owner: $DB_OWNER)"
sudo -u postgres psql -v ON_ERROR_STOP=1 -d postgres <<SQL
DROP DATABASE IF EXISTS ${DB_NAME};
CREATE DATABASE ${DB_NAME} OWNER ${DB_OWNER} ENCODING 'UTF8' TEMPLATE template0;
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_OWNER};
SQL

echo "==> Import dump (map role navigator_naviway -> ${DB_OWNER})"
# Production dump owner is navigator_naviway; local .env uses navigator.
sed 's/navigator_naviway/'"${DB_OWNER}"'/g' "$DUMP" | sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB_NAME"

echo "==> Grants on public schema"
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB_NAME" <<SQL
GRANT ALL ON SCHEMA public TO ${DB_OWNER};
GRANT ALL ON ALL TABLES IN SCHEMA public TO ${DB_OWNER};
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO ${DB_OWNER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${DB_OWNER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${DB_OWNER};
SQL

echo "==> Done. Rows in naviway_page:"
sudo -u postgres psql -d "$DB_NAME" -c "SELECT COUNT(*) AS pages FROM naviway_page;"
