from client import AdaptiveRateLimiterTokenBucket

limiter = AdaptiveRateLimiterTokenBucket(capacity=5, refill_rate_per_sec=2.0)
req1 = limiter.acquire(3)
req2 = limiter.acquire(3)

print("=== Adaptive Rate Limiter Telemetry ===")
print("Request 1:", req1)
print("Request 2:", req2)
limiter.record_throttle_event()
print("Backoff applied. New effective refill:", limiter.refill_rate * limiter.backoff_multiplier)
