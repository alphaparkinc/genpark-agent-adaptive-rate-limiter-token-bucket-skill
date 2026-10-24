import sys
import json
from client import AdaptiveRateLimiterTokenBucket

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "acquire_tokens",
                        "description": "Evaluates rate limit token availability and returns required wait time.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "tokens": {"type": "integer"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        args = params.get("arguments", {})
        limiter = AdaptiveRateLimiterTokenBucket()
        res = limiter.acquire(args.get("tokens", 1))
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    limiter = AdaptiveRateLimiterTokenBucket()
    print(json.dumps(limiter.acquire(1), indent=2))

if __name__ == "__main__":
    main()
