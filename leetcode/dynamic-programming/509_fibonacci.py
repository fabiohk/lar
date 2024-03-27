class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1

        f_1, f_2 = 1, 0
        f = 0
        for _ in range(2, n+1):
            f = f_1 + f_2
            f_1, f_2 = f, f_1
        return f