def knapsack(stations, budget):
    """
    Manual 0/1 Knapsack Dynamic Programming implementation
    Returns: selected_stations, rejected_stations, total_cost, total_benefit, remaining_budget, dp_table
    """
    n = len(stations)
    # Normalize budget to integer (e.g., in units of 1000 or 1 lakh if needed)
    # For simplicity, we'll assume budget and costs are integers
    W = int(budget)
    
    # dp[i][w] = max benefit using first i items with budget w
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        station = stations[i-1]
        cost = int(station['installation_cost'])
        benefit = int(station['benefit'])
        
        for w in range(W + 1):
            if cost <= w:
                dp[i][w] = max(benefit + dp[i-1][w-cost], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
                
    # Backtrack to find selected stations
    selected_stations = []
    rejected_stations = []
    w = W
    total_cost = 0
    total_benefit = 0
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            station = stations[i-1]
            selected_stations.append(station)
            total_cost += int(station['installation_cost'])
            total_benefit += int(station['benefit'])
            w -= int(station['installation_cost'])
        else:
            rejected_stations.append(stations[i-1])
            
    remaining_budget = budget - total_cost
    
    # Reverse to maintain original order if desired
    selected_stations.reverse()
    
    return selected_stations, rejected_stations, total_cost, total_benefit, remaining_budget, dp
