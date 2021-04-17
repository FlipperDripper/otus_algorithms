from linked_list import LinkedList

VALUE_FOR_RESIZE = 0.66
START_SLOTS_COUNT = 10

# Хэш-таблица использующуя метод цепочек
class HashTable(object):

    def __init__(self, items = None):        
        self.slots = [LinkedList() for i in range(START_SLOTS_COUNT)]
        self.size = 0

    def get_hash_index(self, key):
        return self._hash_str(key) & (len(self.slots)-1)

    def hash_str(self, string):
        # алгоритм хэширования djb2
        hash = 5381
        for char in string[1:]:
            hash = (hash << 5) + hash + ord(char)
        return hash

    def contains(self, key):
        slot = self.slots[self._get_hash_index(key)]
        if slot.find_by_key(key) is not None:
            return True
        else:
            return False

    def get(self, key):
        slot = self.slots[self._get_hash_index(key)]
        return slot.find_by_key(key)

    def set(self, key, value):
        slot = self.slots[self._get_hash_index(key)]
        if not slot.delete_by_key(key): 
            self.size += 1
            
        slot.append((key, value))
    
        if (self.size / len(self.slots)) > VALUE_FOR_RESIZE:
            self._resize()

    def delete(self, key):
        slot = self.slots[self._get_hash_index(key)]
        if slot.delete_by_key(key):
            self.size -= 1


    def get_items(self):
        return [items.extend(slot.items()) for slot in self.slots]


    def resize(self):
        items = self.get_items()
        self.size = 0
        self.slots = [LinkedList() for i in range(len(self.slots) * 2)]
        for key, value in items:
            self.set(key, value)