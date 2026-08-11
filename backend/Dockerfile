FROM python:3.11-slim AS builder
WORKDIR /build
COPY pyproject.toml requirements.lock ./
COPY app ./app
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.lock

FROM python:3.11-slim
ENV PATH=/venv/bin:$PATH PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN groupadd --system app && useradd --system --gid app --home /app app
WORKDIR /app
COPY --from=builder /venv /venv
COPY alembic.ini ./
COPY alembic ./alembic
COPY start.sh ./start.sh
RUN mkdir -p /app/data && chown -R app:app /app && chmod +x /app/start.sh
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health/ready',timeout=2)"
ENTRYPOINT ["./start.sh"]
