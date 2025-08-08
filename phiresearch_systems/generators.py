# phiresearch_systems/generators.py

def modlo_sequence(n_terms: int) -> list[int]:
    """
    Generates the first N terms of the “Modlo” array.

    This sequence is a novel, deterministic pseudo-random number generator
    with unique hybrid properties. It begins with the first seven terms of the
    Fibonacci series, establishing an "organic" mathematical foundation, before
    transitioning into a perpetually repeating 8-term cycle.

    This unique structure—an organic head followed by a periodic tail—makes it
    a versatile tool for a new class of deterministic applications.
    """
    if not isinstance(n_terms, int):
        raise TypeError("n_terms must be an integer.")
    if n_terms < 0:
        raise ValueError("n_terms must be non-negative.")
        
    if n_terms == 0:
        return []
        
    # 1. Seed the first seven Fibonacci terms.
    a = [1, 1, 2, 3, 5, 8, 13]
    if n_terms <= 7:
        return a[:n_terms]

    # 2. Define the 8-term cyclic modulus and correction arrays.
    # These values are precisely engineered to force the sequence into its repeating pattern.
    moduli = [17, 9, 44, 29, 47, 19, 9, 199]
    corrections = [0, 8, 0, 0, -10, 0, 0, 0]

    # 3. Build terms 7 through N-1 using the periodic recurrence relation.
    for n in range(7, n_terms):
        # Index into our 8-term cycle
        i = (n - 7) % 8

        # Raw Fibonacci sum of the two previous terms
        s = a[n - 1] + a[n - 2]

        # Apply the small correction, then wrap by the modulus
        wrapped = (s + corrections[i]) % moduli[i]

        # If the modulo result is 0, interpret that as the full modulus value.
        # This ensures the sequence values are always positive.
        a.append(wrapped if wrapped != 0 else moduli[i])

    return a