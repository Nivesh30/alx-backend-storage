#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
import time
from functools import wraps

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def cache_page(url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"count:{url}"
            cached_content = redis_client.get(key)
            if cached_content:
                return cached_content.decode('utf-8')
            else:
                content = func(*args, **kwargs)
                redis_client.setex(key, 10, content)
                return content
        return wrapper
    return decorator

@cache_page("http://slowwly.robertomurray.co.uk/delay/10000/url/https://www.example.com")
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/10000/url/https://www.example.com"
    print(get_page(url))
    time.sleep(5)  # Simulate some delay
    print(get_page(url))  # Should retrieve from cache
