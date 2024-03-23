from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        i, j, k = 0, 0, 0
        nums1_copy = nums1.copy() # O(m+n)
        while i < m and j < n: # O(n) or O(m)
            if nums1_copy[i] <= nums2[j]:
                nums1[k] = nums1_copy[i]
                i += 1
            else:
                nums1[k] = nums2[j]
                j += 1
            k += 1
        
        if i >= m:
            while j < n: # O(n)
                nums1[k] = nums2[j]
                j += 1
                k += 1
        else:
            while i < m: # O(m)
                nums1[k] = nums1_copy[i]
                i += 1
                k += 1

    def naive_merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        self.concatenate(nums1, m, nums2, n) # O(n)
        nums1.sort() # O((m+n)log(m+n))
        return
        
    def concatenate(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        for i, j in zip(range(m, n+m), range(n)):
            nums1[i] = nums2[j]