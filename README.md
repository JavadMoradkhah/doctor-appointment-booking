### Fixtures

```shell
docker compose exec -it server python manage.py loaddata ./fixtures/provinces.json
docker compose exec -it server python manage.py loaddata ./fixtures/cities.json
```
