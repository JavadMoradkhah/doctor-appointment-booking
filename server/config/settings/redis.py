import redis

# Redis Settings

REDIS = redis.Redis(
    host="redis", port=6379, db=0, charset="utf-8", decode_responses=True
)