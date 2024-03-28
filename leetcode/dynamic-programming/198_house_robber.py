from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int: # O(n^2)
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums)

        n = len(nums)
        max_money_to_rob_house = [0 for _ in range(n+1)] # O(n)
        max_money_to_rob_house[1] = nums[0]
        max_money_to_rob_house[2] = max(nums[0], nums[1])

        for i, num in enumerate(nums[2:], start=2): # O(n)
            max_money_to_rob_house[i+1] = num + max(max_money_to_rob_house[:i]) # O(n)

        return max(max_money_to_rob_house) # O(n)