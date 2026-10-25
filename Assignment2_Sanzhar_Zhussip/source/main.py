# Assignment 2 starter. Complete TODO bodies; keep the published I/O contract.
import sys

class Ticket:
    def __init__(self, ident, severity, category, score, arrival):
        self.id, self.severity, self.category = ident, severity, category
        self.priorityScore, self.arrivalOrder = score, arrival
        self.state = "WAITING"

class QueueNode:
    def __init__(self, ticket, next_node=None):
        self.ticket, self.next = ticket, next_node

class HashEntry:
    def __init__(self, key, ticket, next_entry=None):
        self.key, self.ticket, self.next = key, ticket, next_entry

class TicketQueue:
    def __init__(self):
        self.head = None
        self.tail = None


    def enqueue(self, ticket):
        new_node = QueueNode(ticket)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node


    def dequeue(self):
        if self.head is None:
            return None
        ticket = self.head.ticket
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return ticket


    def peek(self):
        if self.head is None:
            return None
        return self.head.ticket


    def isEmpty(self):
        return self.head is None

class BinaryMaxHeap:
    def __init__(self):
        self.items: list[Ticket] = []


    def insert(self, value: Ticket | None) -> None:
        if value is None:
            return
        self.items.append(value)
        index = len(self.items) - 1
        self.siftUp(index)


    def peekMax(self) -> Ticket | None:
        if self.isEmpty():
            return None
        return self.items[0]


    def removeMax(self) -> Ticket | None:
        if self.isEmpty():
            return None
        maxTicket = self.items[0]
        if len(self.items) == 1:
            self.items.pop()
            return maxTicket
        last = self.items.pop()
        self.items[0] = last
        self.siftDown(0)
        return maxTicket


    def isEmpty(self):
        return len(self.items) == 0


    def higher(self, a: Ticket | None, b: Ticket | None) -> bool:
        if a.priorityScore > b.priorityScore:
            return True
        if a.priorityScore < b.priorityScore:
            return False
        return a.arrivalOrder < b.arrivalOrder


    def siftUp(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if not self.higher(self.items[index],self.items[parent]):break
            self.items[index], self.items[parent] = self.items[parent], self.items[index]
            index = parent


    def siftDown(self, index: int) -> None:
        size = len(self.items)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index
            if left < size and self.higher(self.items[left],self.items[largest]):
                largest = left
            if right < size and self.higher(self.items[right],self.items[largest]):
                largest = right
            if largest == index:
                break
            self.items[index], self.items[largest] = self.items[largest], self.items[index]
            index = largest


class TicketHashTable:
    def __init__(self, bucket_count: int):
        self.buckets: list[HashEntry | None] = [None] * bucket_count


    def put(self, key, value):
        index = key % len(self.buckets)
        current = self.buckets[index]
        while current is not None:
            if current.key == key:
                current.ticket = value
                return
            current = current.next
        newEntry = HashEntry(key, value)
        newEntry.next = self.buckets[index]
        self.buckets[index] = newEntry


    def get(self, key: int) -> Ticket | None:
        index = key % len(self.buckets)
        current = self.buckets[index]
        while current is not None:
            if current.key == key:
                return current.ticket
            current = current.next
        return None


    def contains(self, key: int) -> bool:
        return self.get(key) is not None


    def remove(self, key: int) -> Ticket | None:
        index = key % len(self.buckets)
        current = self.buckets[index]
        previous = None
        while current is not None:
            if current.key == key:
                if previous is None:
                    self.buckets[index] = current.next
                else:
                    previous.next = current.next
                return current.ticket
            previous = current
            current = current.next
        return None


class Dispatcher:
    def __init__(self, variant: int):
        self.variant = variant
        sizes = [7, 11, 13, 17, 19]
        self.waiting = TicketQueue()
        self.ready = BinaryMaxHeap()
        self.active = TicketHashTable(sizes[variant % 5])
        self.arrivalCounter = 0
        self.bonuses = [
            {"SW": 3, "HW": 1, "ACC": 2},
            {"SW": 1, "HW": 2, "ACC": 3},
            {"SW": 2, "HW": 3, "ACC": 1},
            {"SW": 3, "HW": 2, "ACC": 1},
            {"SW": 2, "HW": 1, "ACC": 3},
        ]

    def handle(self, line: str) -> str:
        parts = [x for x in line.strip(' ').split(' ') if x]
        if parts[0] == "ADD":
            if len(parts) != 4:
                return "INVALID"
            idText = parts[1]
            severityText = parts[2]
            category = parts[3]
            if not idText.isdigit():
                return "INVALID"
            ticketId = int(idText)
            if ticketId < 1 or ticketId > 1000000000:
                return "INVALID"
            if not severityText.isdigit():
                return "INVALID"
            severity = int(severityText)
            if category not in ("SW", "HW", "ACC"):
                return "INVALID"

            if self.active.contains(ticketId):
                return f"DUPLICATE {ticketId}"

            bonus = self.bonuses[self.variant % 5][category]
            score = severity * 10 + bonus
            self.arrivalCounter += 1
            ticket = Ticket(
                ticketId,
                severity,
                category,
                score,
                self.arrivalCounter
            )
            self.active.put(ticketId, ticket)
            self.waiting.enqueue(ticket)

            return f"ADDED {ticketId} P={score}"

        if parts[0] == "TRIAGE":
            if len(parts) != 1:
                return "INVALID"

            while not self.waiting.isEmpty():
                ticket = self.waiting.dequeue()
                if not self.isActive(ticket, "WAITING"):
                    continue
                ticket.state = "READY"
                self.ready.insert(ticket)
                return f"TRIAGED {ticket.id} P={ticket.priorityScore}"

            return "EMPTY WAITING"

        if parts[0] == "SERVE":
            if len(parts) != 1:
                return "INVALID"

            while not self.ready.isEmpty():
                ticket = self.ready.removeMax()
                if not self.isActive(ticket, "READY"):
                    continue
                self.active.remove(ticket.id)
                return f"SERVED {ticket.id}"

            return "EMPTY READY"

        if parts[0] == "FIND":
            if len(parts) != 2:
                return "INVALID"
            if not parts[1].isdigit():
                return "INVALID"

            ticketId = int(parts[1])
            ticket = self.active.get(ticketId)

            if ticket is None:
                return f"NOT FOUND {ticketId}"

            return (
                f"FOUND {ticket.id} "
                f"{ticket.state} "
                f"P={ticket.priorityScore}"
            )

        if parts[0] == "CANCEL":
            if len(parts) != 2:
                return "INVALID"
            if not parts[1].isdigit():
                return "INVALID"

            ticketId = int(parts[1])
            ticket = self.active.remove(ticketId)

            if ticket is None:
                return f"NOT FOUND {ticketId}"

            return f"CANCELLED {ticketId}"

        return "INVALID"

    def isActive(self, value: Ticket | None, expectedState: str) -> bool:
        if value is None:
            return False
        activeTicket = self.active.get(value.id)
        if activeTicket is not value:
            return False
        return value.state == expectedState


def main():
    lines = sys.stdin.read().splitlines()
    first = [x for x in lines[0].strip(' ').split(' ') if x] if lines else []
    if len(first) != 2 or first[0] != 'CONFIG' or len(first[1]) != 1 or first[1] not in '0123456789':
        print('INVALID')
        return
    app = Dispatcher(int(first[1]))
    for line in lines[1:]:
        if line.strip(' ') == 'END': break
        print(app.handle(line))

if __name__ == '__main__':
    try: main()
    except NotImplementedError as error:
        print(str(error) + ': implement this method before public tests can pass.', file=sys.stderr)
        sys.exit(2)
