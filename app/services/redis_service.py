from app.databases.init_redis import redis_client


class RedisService:
    @staticmethod
    def set(key, value):
        return redis_client.set(key, value)

    @staticmethod
    def get(key):
        return redis_client.get(key)

    @staticmethod
    def delete(key):
        return redis_client.delete(key)
