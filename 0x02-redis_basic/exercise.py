#!/usr/bin/env python3
"""exercise.py module"""

import redis
from uuid import uuid4
from typing import Union, Optional, Callable


class Cache:
    """Cache class for redis"""

    def __init__(self) -> None:
        """Init dunder method"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

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
