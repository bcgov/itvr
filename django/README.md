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

To keep track of CRA wage request we need to manage a sequence of numbers.

Create a migration file.

```bash
python manage.py makemigrations api --empty -n create_cra_wage_request_sequence
```

Adding custom sql to the migration file.

```sql
create sequence api_cra_wage_request_id_seq;
select nextval('api_cra_wage_request_id_seq'); -- Increment sequence
select currval('api_cra_wage_request_id_seq'); -- List current value
```

Rollback the migration.

```bash
python manage.py showmigrations api
python manage.py migrate api 0001_initial
```
tbd
