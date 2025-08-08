# phiresearch_systems/balancing.py
import math
import hashlib
from typing import List

class PhiBalancer:
    """
    A production-ready, high-performance load balancer using Golden Ratio (phi)
    distribution. This method provides mathematically optimal, even distribution
    with minimal computational overhead. It is stateless and thread-safe.
    """
    def __init__(self, servers: List[str]):
        if not isinstance(servers, (list, tuple)):
            raise TypeError("Server list must be a list or tuple.")
        if not servers:
            raise ValueError("Server list cannot be empty.")
        if not all(isinstance(server, str) for server in servers):
            raise TypeError("All server entries must be strings.")
        
        self.servers = tuple(servers) # Use tuple for immutability
        self.num_servers = len(self.servers)
        
        # This specific large prime is a "golden ratio prime" which works
        # exceptionally well for multiplicative hashing. The value is derived from
        # floor(2^64 / φ) where φ is the golden ratio, providing optimal distribution
        # properties for hash table operations.
        self.hash_multiplier = 11400714819323198485

    def get_server_for_request(self, request_id: str) -> str:
        """
        Determines the optimal server for a given request ID.
        This operation is extremely fast, suitable for high-frequency environments.
        Uses deterministic hashing to ensure reproducible results.
        """
        if not isinstance(request_id, str):
            raise TypeError("Request ID must be a string.")
        
        # Use SHA-256 for deterministic, reproducible hashing
        # This avoids Python's hash randomization which can vary between runs
        request_hash = int(hashlib.sha256(request_id.encode('utf-8')).hexdigest()[:16], 16)
        
        # Golden Ratio (Fibonacci) Hashing
        # This is a fast, integer-only operation.
        scaled_hash = (request_hash * self.hash_multiplier) & (2**64 - 1)
        
        # Map the hash to a server index.
        # The multiplication and shift is faster than floating point division.
        index = (scaled_hash * self.num_servers) >> 64
        
        return self.servers[index]