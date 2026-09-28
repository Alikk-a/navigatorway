# Развёртывание navigatorway (Docker, ручные команды)

Production-стек: **PostgreSQL 16**, **Gunicorn**, **Nginx**.  
Для legacy-импорта MariaDB используйте отдельный [`docker-compose.yml`](../docker-compose.yml) — **не** этот compose.

```bash
docker compose -f docker-compose.prod.yml <команда>
```

Далее все команды выполняются **из корня репозитория** на сервере по SSH.

## Требования

- Docker Engine и плагин Compose v2.
- Домен (или IP) в `DJANGO_ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` (для HTTPS).
- Файл `dump.sql` (в git не хранится) — перенос на сервер через `scp` / `rsync`.

## 1. Клонирование

Первый `git clone` может занять заметное время: каталог `media/` в репозитории (~сотни МБ).

```bash
git clone https://github.com/Alikk-a/navigatorway.git
cd navigatorway
git checkout main   # или актуальная ветка по умолчанию
```

Каталог `./media` появится из git; отдельный rsync для первого деплоя **не нужен**.

## 2. Переменные окружения

```bash
cp .env.production.example .env
sed -i 's/\r$//' .env   # если файл редактировали в Windows
nano .env   # секреты, пароль БД, Tailscale IP, домены
```

Обязательно задайте `DJANGO_SECRET_KEY` и `POSTGRES_PASSWORD`.  
Подставьте **Tailscale IP** сервера в `DJANGO_ALLOWED_HOSTS` и в `CSRF_TRUSTED_ORIGINS` (с портом `NGINX_PUBLISH_PORT`, по умолчанию **8088**).

## 3. Сборка образов

```bash
docker compose -f docker-compose.prod.yml build
```

## 4. Запуск PostgreSQL

```bash
docker compose -f docker-compose.prod.yml up -d db
docker compose -f docker-compose.prod.yml ps
```

Дождитесь статуса `healthy` у сервиса `db`.

## 5. Импорт БД (один раз, пустой volume `pgdata`)

Скопируйте `dump.sql` на сервер (например в каталог проекта).

Владелец объектов в дампе — `navigator_naviway`; замените на значение `POSTGRES_USER` из `.env` (обычно `navigator`):

```bash
set -a && source .env && set +a

# Пересоздать БД в контейнере (осторожно: удаляет данные в volume)
docker compose -f docker-compose.prod.yml exec -T db psql -U "${POSTGRES_USER}" -d postgres <<SQL
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${POSTGRES_DB}' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS ${POSTGRES_DB};
CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER} ENCODING 'UTF8' TEMPLATE template0;
GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};
SQL

sed "s/navigator_naviway/${POSTGRES_USER}/g" dump.sql \
  | docker compose -f docker-compose.prod.yml exec -T db psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"

docker compose -f docker-compose.prod.yml exec -T db psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" <<SQL
GRANT ALL ON SCHEMA public TO ${POSTGRES_USER};
GRANT ALL ON ALL TABLES IN SCHEMA public TO ${POSTGRES_USER};
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO ${POSTGRES_USER};
SQL
```

Проверка:

```bash
docker compose -f docker-compose.prod.yml exec -T db psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "SELECT COUNT(*) FROM naviway_page;"
```

Локальный аналог: [`scripts/restore_postgres_dump.sh`](../scripts/restore_postgres_dump.sh).

## 6. Статика

Том `staticfiles` при первом использовании создаётся от root; `collectstatic` запускайте от root:

```bash
docker compose -f docker-compose.prod.yml run --rm --user root web python manage.py collectstatic --noinput
```

## 7. Media

Файлы в `./media` (bind-mount в `web` и `nginx`). После `git pull` обновляются вместе с кодом.

**Rsync с живого прода** — только если на старом сервере есть загрузки, которых ещё нет в git:

```bash
rsync -avz user@old-host:/path/to/media/ ./media/
```

Не используйте пустой named volume для media без копирования — он скроет файлы из репозитория.

## 8. Запуск всего стека

```bash
docker compose -f docker-compose.prod.yml up -d
```

Nginx публикуется на хосте как **`${NGINX_PUBLISH_PORT:-8088}`** → контейнер `:80` (см. `.env`).  
Сервис `web` (Gunicorn) снаружи не публикуется.

### Доступ до переноса DNS

- **Tailscale:** `http://<tailscale-ip>:8088/` (порт из `NGINX_PUBLISH_PORT`).
- На сервере с **Traefik/Dokploy** на `:80` не пробрасывайте этот nginx на 80 — будет конфликт.

### Cloudflare Tunnel

В панели Cloudflare укажите origin на этот хост и порт, например `http://127.0.0.1:8088` (или IP сервера в tailnet).  
Когда домен пойдёт через туннель с HTTPS, оставьте `DJANGO_BEHIND_PROXY=1` и добавьте `https://ваш-домен` в `CSRF_TRUSTED_ORIGINS` и домен в `DJANGO_ALLOWED_HOSTS`.

## 9. Проверки

- Главная страница, пункты меню.
- `/admin/` (при необходимости: `docker compose -f docker-compose.prod.yml run --rm web python manage.py createsuperuser`).
- Пример файла: `/media/...` (ответ 200 от nginx).
- `/static/...` (ответ 200).
- При `DJANGO_DEBUG=False` маршрут `/__debug__/` недоступен.

## 10. Обновление версии

```bash
git pull
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml run --rm --user root web python manage.py collectstatic --noinput
docker compose -f docker-compose.prod.yml up -d --build
```

При новых миграциях в репозитории:

```bash
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate --plan
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate
```

## HTTPS

По умолчанию nginx в контейнере отдаёт только HTTP на внутреннем `:80`; снаружи — выбранный порт (8088).

**Рекомендуемый вариант:** TLS на **Cloudflare Tunnel** (или Cloudflare proxy), origin → `http://127.0.0.1:8088`.

Альтернатива без Cloudflare: certbot на хосте + отдельный reverse-proxy (не занимать `:80`, если там Traefik).

## Суперпользователь Django

```bash
docker compose -f docker-compose.prod.yml run --rm web python manage.py createsuperuser
```
