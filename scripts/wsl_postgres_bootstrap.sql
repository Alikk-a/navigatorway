-- Run once in WSL:
--   sudo -u postgres psql -f scripts/wsl_postgres_bootstrap.sql

CREATE USER navigator WITH PASSWORD 'navigator';
CREATE DATABASE navigatorway OWNER navigator ENCODING 'UTF8' TEMPLATE template0;
GRANT ALL PRIVILEGES ON DATABASE navigatorway TO navigator;
