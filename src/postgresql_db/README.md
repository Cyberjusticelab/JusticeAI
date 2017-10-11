# PostgreSQL Database

## Connect via command line

Bring up all services:

```
./cjl up -d
```

Connect via `psql`:
```
./cjl run --rm postgresql_db "psql -h postgresql_db -U postgres"
```

The above command will prompt you to enter the database password.


