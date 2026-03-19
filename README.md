# Change Data Capture (CDC) Demo

This repository is a local CDC playground that provisions:

- Kafka + Zookeeper
- Debezium Connect + Debezium UI
- Postgres (logical replication enabled)

It also includes `main.py`, a small script that generates synthetic `transactions` rows and inserts them into Postgres.

## Requirements

- `docker compose`
- A valid `DB_PASSWORD` (see `.env.example`)

## Setup

1. Copy env vars

```bash
cp .env.example .env
```

2. Start the stack

```bash
docker compose up --build -d
```

3. Insert a sample transaction

```bash
python main.py
```

## Configuration

The Postgres connection settings for `main.py` are read from:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

Refer to `.env.example` for defaults.
