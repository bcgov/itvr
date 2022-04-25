# Backend

## Database

Log into Docker database.

```bash
docker-compose exec db psql itvr postgres
```

Convert models into migration files. The run migrations.

```bash
docker exec -t -i itvr_api_1 bash
python manage.py makemigrations
python manage.py migrate
```
