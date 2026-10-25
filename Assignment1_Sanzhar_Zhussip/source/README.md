Student name: Sanzhar Zhussip;
Group: SE-2515

Programming language: Python

Task1

Time Complexity: O(n)
Space Complexity: O(log n)

Base Case:
start == end

Recursive Calls:
divideConquer(arr, start, median)
divideConquer(arr, median + 1, end)


Task 2

Time Complexity: O(log n)
Space Complexity: O(log n)

Base Case:
start > end

Recursive Calls:
binary(arr, median + 1, end, target)
binary(arr, start, median - 1, target)

Explanation:

In first task, I used divide and conquer algorithm to separate array to small pieces. After base case they returned maximum value from small and divided arrays.

In second task, I used binary search for sorted array to find number that equal to target. Main function of this algorithm, is to find middle of array and compare with target which side it would be advantageous to use.