def create_redis_key(prefix: str, id: str):
    return f"{prefix}:{id}"
