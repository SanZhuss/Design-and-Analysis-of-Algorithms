def binary(arr, start, end, target):
    if start > end:
        return -1

    median = (start + end) // 2

    if arr[median] == target:
        return median
    elif arr[median] < target:
        return binary(arr, median + 1, end, target)
    else:
        return binary(arr, start, median - 1, target)

def divideConquer(arr, start, end):
    if start == end:
        return arr[start]

    median = (start + end) // 2

    first_half = divideConquer(arr, start, median)
    second_half = divideConquer(arr, median + 1, end)

    if first_half > second_half:
        return first_half
    else:
        return second_half

def task1():
    n = int(input())
    if not n:
        print(0)
    arr = list(map(int, input().split()))

    if not arr:
        print(0)
    else:
        print(divideConquer(arr, 0, n - 1))

def task2():
    n = int(input())
    arr = list(map(int, input().split()))
    target = int(input())

    print(binary(arr, 0, n - 1, target))

#task1()
task2()