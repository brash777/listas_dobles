class Patient:
    SPECIALTIES = {
        "emergency":    {"color": "#EF4444", "priority": 1},
        "cardiology":   {"color": "#F97316", "priority": 2},
        "pediatrics":   {"color": "#8B5CF6", "priority": 3},
        "medicine":     {"color": "#3B82F6", "priority": 4},
        "dentistry":    {"color": "#10B981", "priority": 5},
    }

    def __init__(self, name: str, id_number: str, specialty: str, age: int):
        self.name = name
        self.id_number = id_number
        self.specialty = specialty.lower()
        self.age = age
        self.queue_number: int | None = None

    def to_dict(self):
        info = self.SPECIALTIES.get(self.specialty, {"color": "#6B7280", "priority": 9})
        return {
            "name": self.name,
            "id_number": self.id_number,
            "specialty": self.specialty.capitalize(),
            "age": self.age,
            "turn": self.queue_number,
            "color": info["color"]
        }

    def __str__(self):
        return (f"Turn #{self.queue_number:03d} | {self.name} | "
                f"ID: {self.id_number} | {self.specialty.capitalize()} | Age: {self.age}")


class Node:
    def __init__(self, patient: Patient):
        self.patient: Patient = patient
        self.next: Node | None = None
        self.prev: Node | None = None


class HospitalDoubleList:
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.length: int = 0
        self._turn_counter: int = 1

    def add_to_back(self, patient: Patient) -> Node:
        patient.queue_number = self._turn_counter
        self._turn_counter += 1
        new_node = Node(patient)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.length += 1
        return new_node

    def add_to_front(self, patient: Patient) -> Node:
        patient.queue_number = self._turn_counter
        self._turn_counter += 1
        new_node = Node(patient)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.length += 1
        return new_node

    def serve_next(self) -> Patient | None:
        if self.head is None:
            return None

        patient = self.head.patient
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        self.length -= 1
        return patient

    def remove_by_id(self, id_number: str) -> Patient | None:
        current = self.head
        while current:
            if current.patient.id_number == id_number:
                if current == self.head and current == self.tail:
                    self.head = None
                    self.tail = None
                elif current == self.head:
                    self.head = current.next
                    self.head.prev = None
                elif current == self.tail:
                    self.tail = current.prev
                    self.tail.next = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev

                self.length -= 1
                return current.patient
            current = current.next
        return None

    def find_by_id(self, id_number: str) -> Patient | None:
        current = self.head
        while current:
            if current.patient.id_number == id_number:
                return current.patient
            current = current.next
        return None

    def traverse_forward(self) -> list[dict]:
        result = []
        current = self.head
        while current:
            result.append(current.patient.to_dict())
            current = current.next
        return result

    def is_empty(self) -> bool:
        return self.head is None

    def __len__(self):
        return self.length
