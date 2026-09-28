#!/bin/sh
set -e

host="${POSTGRES_HOST:-db}"
port="${POSTGRES_PORT:-5432}"
user="${POSTGRES_USER:-navigator}"

echo "Waiting for PostgreSQL at ${host}:${port}..."
until pg_isready -h "$host" -p "$port" -U "$user" >/dev/null 2>&1; do
  sleep 2
done
echo "PostgreSQL is ready."

exec "$@"
