def bubble_sort(arr):
    last_swap = len(arr)
    temp = None
    for j in range(len(arr)):
        temp_swap = 0
        for i in range(1, last_swap):
            if arr[i - 1] > arr[i]:
                temp = arr[i - 1]
                arr[i-1] = arr[i]
                arr[i] = temp
                temp_swap = i
        last_swap = temp_swap
    return arr
            

def binary_search(arr, val, start, end):
    if start == end:
        if arr[start] > val:
            return start
        else:
            return start+1
    if start > end:
        return start
 
    mid = (start+end)//2
    if arr[mid] < val:
        return binary_search(arr, val, mid+1, end)
    elif arr[mid] > val:
        return binary_search(arr, val, start, mid-1)
    else:
        return mid
 
 
def insertion_sort(arr):
    for i in range(1, len(arr)):
        val = arr[i]
        j = binary_search(arr, val, 0, i-1)
        arr = arr[:j] + [val] + arr[j:i] + arr[i+1:]
    return arr

def shell_sort(arr):
    n = len(arr)
    gap = n//2
    while gap > 0:
  
        for i in range(gap,n):
            temp = arr[i]
            j = i
            while  j >= gap and arr[j-gap] >temp:
                arr[j] = arr[j-gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

# Седжвик
# https://oeis.org/A036562
def gap_1(n: int) -> int:
    def gap():
        k = 1
        while True:
            g = (4 ** k) + (3 * 2 ** (k - 1)) + 1
            k += 1
            yield int(g)

    result = [0, 1]
    for g in gap():
        if g < n:
            result.append(g)
        else:
            break

    return result

# Papernov & Stasevich
# https://oeis.org/A083318
def gap_2(n: int):
    def gap():
        k = -1
        while True:
            g = (2 ** k) + 1
            k += 1
            yield int(g)

    result = [0]
    for g in gap():
        if g < n:
            result.append(g)
        else:
            break

    return result
 
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
 
    if l < n and arr[largest] < arr[l]:
        largest = l
 

    if r < n and arr[largest] < arr[r]:
        largest = r
 
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        heapify(arr, n, largest) 
 
def heap_sort(arr):
    n = len(arr)
 
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
 
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr
