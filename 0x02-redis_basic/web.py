#!/usr/bin/env python3
"""web.py module"""

import requests
import redis
from functools import wraps


r = redis.Redis()


def url_cache_count(func):
    """
    Decorator for caching and tracking URL access counts
    """

    @wraps(func)
    def wrapper(url):
        data = r.get("cached:" + url)
        if data:
            return data.decode("utf-8")

        content = func(url)
        count_key = "content:" + url

        r.incr(count_key)
        r.set("cached:" + url, content)
        r.expire("cached:" + url, 10)

        return content
    return wrapper


@url_cache_count
def get_page(url: str) -> str:
    """
    Obtains the HTML content of a url and returns it
    """

    return requests.get(url).text
