#!/usr/bin/env python3
"""exercise.py module"""

import redis
from uuid import uuid4
from typing import Union


class Cache:
    """Cache class for redis"""

    def __init__(self) -> None:
        """Init dunder method"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, int, bytes, float]) -> str:
        """
        Store method that stores the input data in Redis.
        Args:
            data: input data, could be an str, int, bytes or float
        Return: key of the stored data (uuid)
        """

        random_key = str(uuid4())
        self._redis.set(random_key, data)

        return random_key
