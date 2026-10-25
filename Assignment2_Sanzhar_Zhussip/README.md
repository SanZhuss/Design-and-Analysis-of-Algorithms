# Assignment 2 submission

Student name: Zhussip Sanzhar
Student ID: 251355
Language: Python
Variant: 5

Complexity:
ADD: O(1 + a/M)
FIND: O(1 + a/M)
CANCEL: O(1 + a/M)
TRIAGE: O(log h + k)
SERVE: O(log h + k)

AI usage:
Used ChatGPT to explain data structures and review implementation. All code was tested and verified manually.

Queue invariant:
Head points to the first node, tail points to the last node. FIFO order is preserved.

Heap invariant:
Parent always has higher priority than its children. Equal priorities are resolved by smaller arrivalOrder.

Hash invariant:
Each active ticket ID appears at most once in the hash table. Collisions are handled with linked chains.

Stale-entry strategy:
Object identity is checked using isActive(). ID equality alone is not sufficient.

Design decisions:
Queue is implemented as a singly linked list.
Hash table uses separate chaining for collisions.

Run instructions:
python main.py < input.txt