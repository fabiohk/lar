class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        while n > 0:
            space, is_valid_space = self.find_empty_space(flowerbed)
            if not is_valid_space:
                break
            flowerbed[space] = 1
            n -= 1
        return n == 0

    def find_empty_space(self, flowerbed: List[int]) -> Tuple[int, bool]:
        for i, space in enumerate(flowerbed):
            if space == 0:
                is_previous_empty = flowerbed[i-1] == 0 if i-1 >= 0 else True
                is_next_empty = flowerbed[i+1] == 0 if i+1 < len(flowerbed) else True
                if is_previous_empty and is_next_empty:
                    return i, True
        return -1, False