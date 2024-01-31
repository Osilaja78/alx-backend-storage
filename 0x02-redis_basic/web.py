#!/usr/bin/env python3
"""web.py module"""

import requests
import redis
from functools import wraps
from typing import Callable


r = redis.Redis()


def url_cache_count(method: Callable) -> Callable:
    """
    Decorator for caching and tracking URL access counts
    """

    @wraps(method)
    def wrapper(url):
        """Wrapper function to increment and set expiry"""

        print(r.incr(f"count:{url}"))
        data = r.get(f"cached:{url}")
        if data:
            return data.decode("utf-8")

        content = method(url)
        r.setex(f"cached:{url}", 10, content)

        return content
    return wrapper


@url_cache_count
def get_page(url: str) -> str:
    """
    Obtains the HTML content of a url and returns it
    """

    return requests.get(url).text
