from math import gcd, isfinite
from functools import reduce


def knapsack(stations, budget):
    """Exact 0/1 knapsack DP, scaling all costs by their greatest common divisor."""
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 0:
        raise ValueError('Budget must be a non-negative integer')
    if not isinstance(stations, list) or any(not isinstance(s, dict) for s in stations):
        raise ValueError('Stations must be a list of objects')
    costs = []
    benefits = []
    for station in stations:
        cost, benefit = station.get('installation_cost'), station.get('benefit')
        if isinstance(cost, bool) or not isinstance(cost, int) or cost < 0:
            raise ValueError('Station costs must be non-negative integers')
        try:
            valid_benefit = not isinstance(benefit, bool) and isinstance(benefit, (int, float)) and isfinite(benefit) and benefit >= 0
        except OverflowError:
            valid_benefit = False
        if not valid_benefit:
            raise ValueError('Station benefits must be non-negative numbers')
        costs.append(cost)
        benefits.append(benefit)
    try:
        if not isfinite(sum(benefits)):
            raise ValueError('Total station benefit is too large')
    except OverflowError:
        raise ValueError('Total station benefit is too large')
    scale = reduce(gcd, costs, 0) or 1
    capacity = min(budget // scale, sum(costs) // scale)
    if (len(stations) + 1) * (capacity + 1) > 2000000:
        raise ValueError('Problem is too large; reduce the budget or number of stations')
    dp = [[0] * (capacity + 1) for _ in range(len(stations) + 1)]
    for i, station in enumerate(stations, 1):
        cost = costs[i - 1] // scale
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]
            if cost <= w:
                dp[i][w] = max(dp[i][w], station['benefit'] + dp[i-1][w-cost])
    selected = []
    w = capacity
    for i in range(len(stations), 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)
            w -= costs[i-1] // scale
    chosen = set(selected)
    yes = [s for i, s in enumerate(stations) if i in chosen]
    no = [s for i, s in enumerate(stations) if i not in chosen]
    cost = sum(s['installation_cost'] for s in yes)
    benefit = sum(s['benefit'] for s in yes)
    return yes, no, cost, benefit, budget-cost, dp
