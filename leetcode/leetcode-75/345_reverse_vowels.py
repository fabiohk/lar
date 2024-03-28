class Solution:
    def reverseVowels(self, s: str) -> str:
        string_as_array = [c for c in s]

        positions_to_swap = []
        for i, c in enumerate(s):
            if c.lower() in ['a', 'e', 'i', 'o', 'u']:
                positions_to_swap.append(i)
        
        n = len(positions_to_swap)
        for i in range(n // 2):
            position_a = positions_to_swap[i]
            position_b = positions_to_swap[n-i-1]
            string_as_array[position_a], string_as_array[position_b] = string_as_array[position_b], string_as_array[position_a]

        return "".join(string_as_array)