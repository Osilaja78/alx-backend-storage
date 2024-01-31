#!/usr/bin/env python3
"""exercise.py module"""

import redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts how many times the methods of
    the Cache class are called.

    Args: method - a callable function from the Cache class
    Return: a callable
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increments the count for key"""

        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that store the history of inputs and
    outputs for a particular function.

    Args: method - a callable function from the Cache class
    Return: a callable
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Appends ":inputs" and ":outputs" to create
        input and output list keys
        """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output
    return wrapper


def replay(func: Callable) -> None:
    """
    Displays the history of calls of a particular function.

    Args: func - function whose history to display
    Return: nothing
    """

    r = redis.Redis()
    func_name = func.__qualname__
    calls = r.get(func_name)

    try:
        calls = int(calls.decode("utf-8"))
    except Exception:
        calls = 0

    print(f"{func_name} was called {calls} times:")
    inputs = r.lrange(f"{func_name}:inputs", 0, -1)
    outputs = r.lrange(f"{func_name}:outputs", 0, -1)

    for i, o in zip(inputs, outputs):
        try:
            i = i.decode("utf-8")
            o = o.decode("utf-8")
        except Exception:
            i = ""
            o = ""

        print(f"{func_name}(*{i}) -> {o}")


class Cache:
    """Cache class for redis"""

    def __init__(self) -> None:
        """Init dunder method"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store method that stores the input data in Redis.
        Args:
            data: input data, could be an str, int, bytes or float
        Return: key of the stored data (uuid)
        """

        random_key = str(uuid4())
        self._redis.set(random_key, data)

        return random_key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        Get method to retrieve stored data from Redis.
        Args:
            key: the key of the stored data
            fn: callable to convert the data to the desired format.
        Return: the stored data.
        """

        data = self._redis.get(key)
        if fn:
            data = fn(data)

        return data

    def get_str(self, key: str) -> str:
        """
        Automatically parametrize Cache.get with the correct
        conversion function.
        Args:
            key: the key of the stored data
        Return: the stored data
        """

        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Automatically parametrize Cache.get with the correct
        conversion function.
        Args:
            key: the key of the stored data
        Return: the stored data
        """

        data = self._redis.get(key)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0

        return data
