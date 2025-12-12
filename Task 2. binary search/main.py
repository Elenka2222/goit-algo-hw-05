# Binary search with iteration counter and upper bound

def binary_search_bounds(arr, x):
    count = 0
    low, high = 0, len(arr) - 1
    upper = None  # upper bound (smallest value >= x)

    while low <= high:
        count += 1
        mid = (low + high) // 2

        # update upper bound if current element fits the condition
        if arr[mid] >= x and (upper is None or arr[mid] < upper):
            upper = arr[mid]

        # choose search direction
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    return count, upper


# Example
if __name__ == "__main__":
    arr = [1.1, 2.5, 3.3, 5.0, 8.2]
    x = 4.0
    print(binary_search_bounds(arr, x))  # Expected: (2, 5.0)
