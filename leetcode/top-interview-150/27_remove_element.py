from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        i = 0
        elements_tested = 0
        n = len(nums)

        while elements_tested < n:
            elements_tested += 1
            if nums[i] == val:
                last_idx = n-(k+1)
                current_idx = i
                nums[last_idx], nums[current_idx] = nums[current_idx], nums[last_idx]
                k += 1
            else:
                i += 1

        return n-k