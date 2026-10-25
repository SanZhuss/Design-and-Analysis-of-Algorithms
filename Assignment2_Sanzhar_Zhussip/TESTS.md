# TESTS.md

## Test 1 - Integrated Flow

Purpose:
Verify complete ticket lifecycle.

Input:
```text
CONFIG 0
ADD 101 5 SW
FIND 101
TRIAGE
SERVE
FIND 101
END
```

Expected:
```text
ADDED 101 P=53
FOUND 101 WAITING P=53
TRIAGED 101 P=53
SERVED 101
NOT FOUND 101
```

Actual:
```text
ADDED 101 P=53
FOUND 101 WAITING P=53
TRIAGED 101 P=53
SERVED 101
NOT FOUND 101
```

Result: PASS

---

## Test 2 - Duplicate ID

Purpose:
Verify duplicate active IDs are rejected.

Input:
```text
CONFIG 0
ADD 101 5 SW
ADD 101 4 HW
END
```

Expected:
```text
ADDED 101 P=53
DUPLICATE 101
```

Actual:
```text
ADDED 101 P=53
DUPLICATE 101
```

Result: PASS

---

## Test 3 - Cancel Waiting Ticket

Purpose:
Verify cancelled waiting tickets are skipped during TRIAGE.

Input:
```text
CONFIG 0
ADD 101 5 SW
CANCEL 101
TRIAGE
END
```

Expected:
```text
ADDED 101 P=53
CANCELLED 101
EMPTY WAITING
```

Actual:
```text
ADDED 101 P=53
CANCELLED 101
EMPTY WAITING
```

Result: PASS

---

## Test 4 - Heap Priority Ordering

Purpose:
Verify SERVE returns tickets in descending priority order.

Input:
```text
CONFIG 0
ADD 101 1 SW
ADD 102 5 SW
ADD 103 3 SW
TRIAGE
TRIAGE
TRIAGE
SERVE
SERVE
SERVE
END
```

Expected:
```text
ADDED 101 P=13
ADDED 102 P=53
ADDED 103 P=33
TRIAGED 101 P=13
TRIAGED 102 P=53
TRIAGED 103 P=33
SERVED 102
SERVED 103
SERVED 101
```

Actual:
```text
ADDED 101 P=13
ADDED 102 P=53
ADDED 103 P=33
TRIAGED 101 P=13
TRIAGED 102 P=53
TRIAGED 103 P=33
SERVED 102
SERVED 103
SERVED 101
```

Result: PASS

---

## Test 5 - Equal Priority Tie Break

Purpose:
Verify arrival order resolves equal priorities.

Input:
```text
CONFIG 0
ADD 101 5 SW
ADD 102 5 SW
TRIAGE
TRIAGE
SERVE
SERVE
END
```

Expected:
```text
ADDED 101 P=53
ADDED 102 P=53
TRIAGED 101 P=53
TRIAGED 102 P=53
SERVED 101
SERVED 102
```

Actual:
```text
ADDED 101 P=53
ADDED 102 P=53
TRIAGED 101 P=53
TRIAGED 102 P=53
SERVED 101
SERVED 102
```

Result: PASS

---

## Test 6 - ID Reuse

Purpose:
Verify old ticket objects are ignored after cancellation.

Input:
```text
CONFIG 0
ADD 101 5 SW
CANCEL 101
ADD 101 2 HW
TRIAGE
END
```

Expected:
```text
ADDED 101 P=53
CANCELLED 101
ADDED 101 P=21
TRIAGED 101 P=21
```

Actual:
```text
ADDED 101 P=53
CANCELLED 101
ADDED 101 P=21
TRIAGED 101 P=21
```

Result: PASS