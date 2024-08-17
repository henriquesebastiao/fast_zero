FROM python:3.12-slim
LABEL mantainer="contato@henriquesebastiao.com"

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY fast_zero ./fast_zero
COPY migrations ./migrations
COPY alembic.ini .
COPY entrypoint.sh .
COPY pyproject.toml .
COPY .env .

RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --without dev --no-interaction --no-ansi

EXPOSE 8000

CMD poetry run uvicorn --host 0.0.0.0 fast_zero.app:app