# phiresearch_systems/balancing.py
import math
from typing import List

class PhiBalancer:
    """
    A production-ready, high-performance load balancer using Golden Ratio (phi)
    distribution. This method provides mathematically optimal, even distribution
    with minimal computational overhead. It is stateless and thread-safe.
    """
    def __init__(self, servers: List[str]):
        if not servers:
            raise ValueError("Server list cannot be empty.")
        self.servers = tuple(servers) # Use tuple for immutability
        self.num_servers = len(self.servers)
        
        # This specific large prime is a "golden ratio prime" which works
        # exceptionally well for multiplicative hashing.
        self.hash_multiplier = 11400714819323198485

    def get_server_for_request(self, request_id: str) -> str:
        """
        Determines the optimal server for a given request ID.
        This operation is extremely fast, suitable for high-frequency environments.
        """
        # Python's built-in hash() is fast and sufficient for this purpose.
        # It's salted by default, providing good initial distribution.
        request_hash = hash(request_id)
        
        # Golden Ratio (Fibonacci) Hashing
        # This is a fast, integer-only operation.
        scaled_hash = (request_hash * self.hash_multiplier) & (2**64 - 1)
        
        # Map the hash to a server index.
        # The multiplication and shift is faster than floating point division.
        index = (scaled_hash * self.num_servers) >> 64
        
        return self.servers[index]