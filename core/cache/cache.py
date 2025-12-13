from django.core.cache import cache

from core.cache.prefix import CacheKeyPrefix


class Cache:
    @staticmethod
    def set(
        prefix: CacheKeyPrefix,
        key: str,
        value: int,
        timeout: int,
    ) -> None:
        cache.set(
            key=f"{prefix.value}:{key}",
            value=value,
            timeout=timeout,
        )
