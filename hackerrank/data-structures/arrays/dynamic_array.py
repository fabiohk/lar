def dynamicArray(n, queries):
    arr = [[] for _ in range(n)]
    last_answer = 0
    query_2_answers = []
    
    for query in queries:
        query_type, x, y = query
        if query_type == 1:
            idx = calculate_index(x, last_answer, n)
            arr[idx].append(y)
        if query_type == 2:
            idx = calculate_index(x, last_answer, n)
            last_answer = calculate_answer(arr, idx, y)
            query_2_answers.append(last_answer)
    
    return query_2_answers
    
def calculate_index(x, last_answer, n):
    return (x ^ last_answer) % n
    
def calculate_answer(arr, idx, y):
    return arr[idx][y % len(arr[idx])]