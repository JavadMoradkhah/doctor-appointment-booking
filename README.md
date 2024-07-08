### Fixtures

```shell
docker compose exec -it server python manage.py loaddata provinces.json
docker compose exec -it server python manage.py loaddata cities.json
docker compose exec -it server python manage.py loaddata insurances.json
docker compose exec -it server python manage.py loaddata facilities.json
```
