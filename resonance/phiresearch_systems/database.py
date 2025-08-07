# phiresearch_systems/database.py
from typing import List
from .balancing import PhiBalancer

class PhiDB:
    """
    A production-ready sharding router for a distributed database.
    It ensures mathematical coherence with the load balancer by re-using
    the exact same PhiBalancer logic, which is the core of the Resonance
    Hypothesis.
    """
    def __init__(self, db_shards: List[str]):
        if not db_shards:
            raise ValueError("Database shard list cannot be empty.")
        
        # The router is a direct instance of the proven PhiBalancer.
        self.router = PhiBalancer(db_shards)

    def get_shard_for_key(self, key: str) -> str:
        """
        Determines which database shard is responsible for a given key.
        This ensures that data related to a specific user/request is likely
        to be handled by the same application server and database shard,
        improving cache locality and performance.
        """
        return self.router.get_server_for_request(key)