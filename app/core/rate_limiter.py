import time
from collections import defaultdict
from typing import Dict, Tuple
from app.core.config import settings


class InMemoryRateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.limit = settings.RATE_LIMIT_PER_MINUTE
        self.window_seconds = 60

    def _clean(self, api_key: str, now: float):
        window_start = now - self.window_seconds
        self.requests[api_key] = [
            t for t in self.requests[api_key] if t > window_start
        ]

    def check_rate_limit(self, api_key: str) -> Tuple[bool, int]:
        now = time.time()
        self._clean(api_key, now)

        if len(self.requests[api_key]) >= self.limit:
            return False, 0

        self.requests[api_key].append(now)
        remaining = self.limit - len(self.requests[api_key])

        return True, remaining

    def get_remaining(self, api_key: str) -> int:
        now = time.time()
        self._clean(api_key, now)
        return max(0, self.limit - len(self.requests[api_key]))


rate_limiter = InMemoryRateLimiter()