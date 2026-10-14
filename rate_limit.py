"""Rate limiting en mémoire (sliding window)."""
import time
from collections import defaultdict, deque
from threading import Lock


class RateLimiter:
    """Limite simple par IP + endpoint."""

    def __init__(self, max_per_minute: int = 60):
        self.max = max_per_minute
        self._hits: dict[str, deque] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str) -> tuple[bool, int]:
        """
        Retourne (autorisé, secondes_avant_reset).
        `key` = "ip:endpoint" par exemple.
        """
        now = time.time()
        with self._lock:
            q = self._hits[key]
            # Purge les entrées > 60 s
            while q and now - q[0] > 60:
                q.popleft()
            if len(q) >= self.max:
                wait = int(60 - (now - q[0])) + 1
                return False, max(1, wait)
            q.append(now)
            return True, 0

    def reset(self, key: str | None = None):
        with self._lock:
            if key is None:
                self._hits.clear()
            else:
                self._hits.pop(key, None)

    def stats(self) -> dict:
        with self._lock:
            return {
                "tracked_keys": len(self._hits),
                "total_hits": sum(len(q) for q in self._hits.values()),
            }