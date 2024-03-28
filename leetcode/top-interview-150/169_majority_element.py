from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        candidate, count = nums[0], 1 # O(1) space

        for num in nums: # O(n)
            if candidate == num:
                count += 1
            else:
                count -= 1

            if count == 0:
                candidate = num
                count += 1

        return candidate
    
    def naive_majorityElement(self, nums: List[int]) -> int:
        elements_map = {} # O(n) space

        for num in nums: # O(n)
            if num not in elements_map:
                elements_map[num] = 1
            else:
                elements_map[num] += 1
        
        majority_element, majority_count = 0, 0 # O(1) space
        for num, count in elements_map.items(): # O(n)
            if count > majority_count:
                majority_element, majority_count = num, count
            
        return majority_element