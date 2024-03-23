def naive_rotateLeft(d, arr):
    for _ in range(d):
        arr = do_one_left_rotation(arr)
    return arr
    
def rotateLeft(d, arr):
    n = len(arr)
    new_positions = [calculate_position(idx, d, n) for idx in range(n)]
    
    rotated_arr = arr.copy()
    for idx, new_position in enumerate(new_positions):
        rotated_arr[new_position] = arr[idx]
    return rotated_arr
    
def calculate_position(idx, d, n):
    return (idx-d+n) % n

def do_one_left_rotation(arr):
    rotated_arr = arr[1:]
    rotated_arr.append(arr[0])
    return rotated_arr