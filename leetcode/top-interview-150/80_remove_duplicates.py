from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        current_num = nums[0]
        k, current_num_count = 1, 1

        for i, num in enumerate(nums[1:], start=1):
            if current_num == num:
                current_num_count += 1
            else:
                current_num_count = 1
                current_num = num

            if current_num_count <= 2:
                k += 1
            else:
                nums[i] = 100_000

        nums.sort()
        return k