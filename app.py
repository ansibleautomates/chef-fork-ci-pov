"""Small synthetic application for a fork PR CI proof of value."""

import json


def total_cost(items, discount=0):
    if not 0 <= discount <= 100:
        raise ValueError("discount must be between 0 and 100")
    if any(price < 0 for price in items):
        raise ValueError("prices must be nonnegative")
    return round(sum(items) * (1 - discount / 100), 2)


if __name__ == "__main__":
    print(json.dumps({"application": "fork-ci-pov", "total": total_cost([10, 20], 10)}))
