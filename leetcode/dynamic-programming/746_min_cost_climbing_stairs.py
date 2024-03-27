class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        top = len(cost)
        min_cost_to_reach = [0 for i in range(top+1)]

        for i in range(2, top+1):
            min_cost_to_reach[i] = min(cost[i-1] + min_cost_to_reach[i-1], cost[i-2] + min_cost_to_reach[i-2])

        return min_cost_to_reach[top]