import random
from typing import Dict, List

def build_bloom_sequence(n: int, bloom_mix: Dict[str, int], seed: int = 7) -> List[str]:
    random.seed(seed)

    levels: List[str] = []
    for level, pct in bloom_mix.items():
        if pct <= 0:
            continue
        count = round((pct / 100) * n)
        levels.extend([level] * count)

    # fix length exactly n
    most_common = max(bloom_mix, key=bloom_mix.get)

    while len(levels) < n:
        levels.append(most_common)
    while len(levels) > n:
        levels.pop()

    random.shuffle(levels)
    return levels
