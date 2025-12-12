class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        h = self.hash_function(key)
        for pair in self.table[h]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[h].append([key, value])

    def get(self, key):
        h = self.hash_function(key)
        for pair in self.table[h]:
            if pair[0] == key:
                return pair[1]
        return None

    # ------------------- DELETE METHOD -------------------
    def delete(self, key):
        h = self.hash_function(key)
        for i, pair in enumerate(self.table[h]):
            if pair[0] == key:
                self.table[h].pop(i)
                return True
        return False

# ------------------- TEST -------------------
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(H.get("apple"))    # 10
print(H.get("orange"))   # 20
print(H.get("banana"))   # 30

H.delete("orange")
print(H.get("orange"))   # None
