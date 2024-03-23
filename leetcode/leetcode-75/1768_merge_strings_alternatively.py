class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        results_for_each_n = [0 for _ in range(n+1)]
        results_for_each_n[1] = 1
        results_for_each_n[2] = 2

        for i in range(3, n+1):
            results_for_each_n[i] = results_for_each_n[i-1] + results_for_each_n[i-2]

        return results_for_each_n[n]