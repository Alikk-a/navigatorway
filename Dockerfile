FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .

RUN sed -i 's/\r$//' /app/deploy/entrypoint.sh \
    && chmod +x /app/deploy/entrypoint.sh \
    && useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
CMD ["gunicorn", "navigatorway.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
