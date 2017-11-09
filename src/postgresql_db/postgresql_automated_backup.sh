#!/usr/bin/env bash

export PGPASSWORD=$(printf '%s' "$POSTGRES_PASSWORD")

cd /home/ubu1/JusticeAI/ && \
./cjl run --rm -e PGPASSWORD='$PGPASSWORD' postgresql_db "pg_dump -h postgresql_db -U postgres -p 5432" > /home/ubu1/data/pg-dumps/dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
