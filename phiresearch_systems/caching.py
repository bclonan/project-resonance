from typing import Optional
from collections import OrderedDict
import math

class PhiCache:
    """
    A fixed-size cache that combines Least Recently Used (LRU) with a
    Fibonacci-based weighting system for eviction. Items that are accessed
    frequently are given higher "resonance" weights, making them less likely
    to be evicted than older, less important items.
    """
    def __init__(self, capacity: int = 256):
        if not isinstance(capacity, int):
            raise TypeError("Cache capacity must be an integer.")
        if capacity <= 0:
            raise ValueError("Cache capacity must be positive.")
        self.cache = OrderedDict()
        self.capacity = capacity
        self.phi = (1 + math.sqrt(5)) / 2
        # Precompute Fibonacci numbers to use as weights
        self.fib_weights = [0, 1]
        while len(self.fib_weights) < 30: # Support high access counts
            self.fib_weights.append(self.fib_weights[-1] + self.fib_weights[-2])

    def _get_weight(self, access_count: int) -> int:
        """Maps access count to a Fibonacci weight."""
        index = min(access_count, len(self.fib_weights) - 1)
        return self.fib_weights[index]

    def get(self, key: str) -> Optional[str]:
        """
        Retrieves an item from the cache. If found, its access count is
        incremented, and it's moved to the end (most recently used).
        """
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string.")
        
        if key not in self.cache:
            return None
        
        value, access_count = self.cache[key]
        access_count += 1
        self.cache[key] = (value, access_count)
        self.cache.move_to_end(key)
        return value

    def put(self, key: str, value: str):
        """
        Adds an item to the cache. If the cache is full, it evicts the
        item with the lowest score (a combination of recency and weight).
        """
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string.")
        if not isinstance(value, str):
            raise TypeError("Cache value must be a string.")
        
        if key in self.cache:
            # Update existing key
            _, access_count = self.cache[key]
            self.cache[key] = (value, access_count + 1)
            self.cache.move_to_end(key)
        else:
            # Add new key
            self.cache[key] = (value, 1) # Start with access count of 1
            if len(self.cache) > self.capacity:
                self._evict()

    def _evict(self):
        """
        Evicts the least valuable item. The value is determined by its
        Fibonacci weight divided by its age (position in the LRU order).
        This prioritizes keeping high-weight items even if they are old.
        
        Optimized version that finds the minimum in a single pass.
        """
        if not self.cache:
            return
            
        lowest_score = float('inf')
        key_to_evict = None
        
        # Single pass through items from oldest to newest
        for i, (key, (value, access_count)) in enumerate(self.cache.items()):
            weight = self._get_weight(access_count)
            # Score = weight / age (older items have smaller i)
            # The phi factor slightly boosts the score of newer items.
            score = weight / (math.pow(i + 1, self.phi - 1))
            
            if score < lowest_score:
                lowest_score = score
                key_to_evict = key
        
        if key_to_evict:
            del self.cache[key_to_evict]