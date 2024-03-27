from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        elements_in_array_map = {}

        for num in nums:
            if num not in elements_in_array_map:
                elements_in_array_map[num] = 1
            else:
                elements_in_array_map[num] += 1

        k = 0
        for num in elements_in_array_map.keys():
            nums[k] = num
            k += 1
        return k