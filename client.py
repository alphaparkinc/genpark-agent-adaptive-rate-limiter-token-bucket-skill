"""Adaptive Rate Limiter Token Bucket Engine.
100% Python Standard Library.
"""

import time
from typing import Dict, Any

class AdaptiveRateLimiterTokenBucket:
    """Manages API request throughput, smooths burst spikes, and scales down rate upon 429 signals."""
    def __init__(self, capacity: int = 10, refill_rate_per_sec: float = 5.0):
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate_per_sec
        self.last_update = time.time()
        self.backoff_multiplier = 1.0

    def _refill(self):
        now = time.time()
        delta = now - self.last_update
        self.tokens = min(float(self.capacity), self.tokens + (delta * self.refill_rate * self.backoff_multiplier))
        self.last_update = now

    def acquire(self, requested_tokens: int = 1) -> Dict[str, Any]:
        self._refill()
        if self.tokens >= requested_tokens:
            self.tokens -= requested_tokens
            return {"allowed": True, "tokens_remaining": round(self.tokens, 2), "wait_ms": 0}
        needed = requested_tokens - self.tokens
        wait_seconds = needed / max(0.1, self.refill_rate * self.backoff_multiplier)
        return {"allowed": False, "tokens_remaining": round(self.tokens, 2), "wait_ms": int(wait_seconds * 1000)}

    def record_throttle_event(self):
        self.backoff_multiplier = max(0.2, self.backoff_multiplier * 0.5)

    def record_success_event(self):
        self.backoff_multiplier = min(1.0, self.backoff_multiplier * 1.1)
