# phiresearch_compression/utils.py
import math

def calculate_shannon_entropy(data: bytes) -> float:
    """
    Calculates the Shannon entropy (order-0) of a given byte stream.
    """
    if not data:
        return 0.0

    byte_counts = [0] * 256
    for byte in data:
        byte_counts[byte] += 1

    length = len(data)
    entropy = 0.0
    for count in byte_counts:
        if count > 0:
            probability = count / length
            entropy -= probability * math.log2(probability)

    return entropy

def verify_efficiency(original_data: bytes, compressed_data: bytes) -> tuple[float, float, int]:
    """
    Calculates compression efficiency against the Shannon limit.

    Returns:
        A tuple containing:
        - (float): The Shannon efficiency as a percentage.
        - (float): The theoretical minimum compressed size in bytes.
        - (int): The actual compressed size in bytes.
    """
    if not original_data:
        return (100.0, 0.0, len(compressed_data))

    entropy = calculate_shannon_entropy(original_data)
    theoretical_minimum_bytes = (entropy * len(original_data)) / 8.0
    actual_compressed_bytes = len(compressed_data)

    if actual_compressed_bytes == 0:
        return (0.0, theoretical_minimum_bytes, 0)

    efficiency = (theoretical_minimum_bytes / actual_compressed_bytes) * 100.0
    return (efficiency, theoretical_minimum_bytes, actual_compressed_bytes)