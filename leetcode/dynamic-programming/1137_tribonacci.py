class Solution:
    def tribonacci(self, n: int) -> int:
        if n == 0:
            return 0
        if n <= 2:
            return 1
        
        f = 0
        f_1, f_2, f_3 = 1, 1, 0
        for _ in range(3, n+1):
            f = f_1 + f_2 + f_3
            f_1, f_2, f_3 = f, f_1, f_2
        return f