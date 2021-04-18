VALUE_FOR_RESIZE = 0.66
START_SLOTS_COUNT = 10


class SimpleLinkedList:
    def __init__(self):
        self.array = []

    def find_by_key(self, key):
        for item in self.array:
            if item[0] == key:
                return item[1]
        return None

    def append(self, key, value):
        self.array.append((key, value))

    def delete_by_key(self, key):
        self.array = list(filter(lambda item: item[0] != key, self.array))

    def items(self):
        return self.array


# Хэш-таблица использующуя метод цепочек
class HashTable(object):

    def __init__(self, items=None):
        self.slots = [SimpleLinkedList() for i in range(START_SLOTS_COUNT)]
        self.size = 0

    def get_hash_index(self, key):
        return self.hash_str(key) & (len(self.slots) - 1)

    def hash_str(self, string):
        # алгоритм хэширования djb2
        hash = 5381
        for char in string[1:]:
            hash = (hash << 5) + hash + ord(char)
        return hash

    def contains(self, key):
        slot = self.slots[self.get_hash_index(key)]
        if slot.find_by_key(key) is not None:
            return True
        else:
            return False

    def get(self, key):
        slot = self.slots[self.get_hash_index(key)]
        return slot.find_by_key(key)

    def set(self, key, value):
        slot = self.slots[self.get_hash_index(key)]
        if not slot.delete_by_key(key):
            self.size += 1

        slot.append(key, value)

        if (self.size / len(self.slots)) > VALUE_FOR_RESIZE:
            self.resize()

    def delete(self, key):
        slot = self.slots[self.get_hash_index(key)]
        if slot.delete_by_key(key):
            self.size -= 1

    def get_items(self):
        items = []
        for slot in self.slots:
            for tpl in slot.items():
                items.append(tpl)
        return items

    def resize(self):
        items = self.get_items()
        self.size = 0
        self.slots = [SimpleLinkedList() for i in range(len(self.slots) * 2)]
        for key, value in items:
            self.set(key, value)
