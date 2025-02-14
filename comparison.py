import time
import sys
import matplotlib.pyplot as plt

m = 101
# Função hash
def h(x):
    return x % m

class MerkleTree:
    def __init__(self):
        self.leaves = []
        self.root = None

    def build_tree(self, leaves):
        if not leaves:
            return None
        current_layer = leaves[:]
        while len(current_layer) > 1:
            if len(current_layer) % 2 == 1:
                current_layer.append(current_layer[-1])
            next_layer = []
            for i in range(0, len(current_layer), 2):
                combined = current_layer[i] + current_layer[i+1]
                parent = h(combined)
                next_layer.append(parent)
            current_layer = next_layer
        return current_layer[0]

    def insert(self, value):
        self.leaves.append(h(value))
        self.root = self.build_tree(self.leaves)

    def remove(self, index):
        if 0 <= index < len(self.leaves):
            self.leaves.pop(index)
            self.root = self.build_tree(self.leaves)

    def validate(self):
        return self.root == self.build_tree(self.leaves)

    def memory_usage(self):
        return sys.getsizeof(self.leaves) + sys.getsizeof(self.root)

class HashChain:
    def __init__(self):
        self.data = []
        self.chain = []

    def insert(self, value):
        self.data.append(value)
        if not self.chain:
            new_hash = h(value)
        else:
            new_hash = h(self.chain[-1] + value)
        self.chain.append(new_hash)

    def remove(self, index):
        if 0 <= index < len(self.data):
            self.data.pop(index)
            self.chain = []
            for x in self.data:
                if not self.chain:
                    new_hash = h(x)
                else:
                    new_hash = h(self.chain[-1] + x)
                self.chain.append(new_hash)

    def validate(self):
        computed_chain = []
        for x in self.data:
            if not computed_chain:
                new_hash = h(x)
            else:
                new_hash = h(computed_chain[-1] + x)
            computed_chain.append(new_hash)
        return computed_chain == self.chain

    def memory_usage(self):
        return sys.getsizeof(self.data) + sys.getsizeof(self.chain)

def measure_time(func, n_reps=10):
    times = []
    for _ in range(n_reps):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / n_reps

sizes = [100, 500, 1000, 5000]

mt_insertion_times = []
hc_insertion_times = []

mt_removal_times = []
hc_removal_times = []

mt_validation_times = []
hc_validation_times = []

mt_memory = []
hc_memory = []

for n in sizes:
    # --- Merkle Tree ---
    mt = MerkleTree()
    # Inserção
    for i in range(n):
        mt.insert(i)
    # Mede o tempo de inserção
    mt_ins_time = measure_time(lambda: mt.insert(n + 1))
    mt_insertion_times.append(mt_ins_time)
    # Mede o tempo de remoção
    mt_rem_time = measure_time(lambda: mt.remove(len(mt.leaves)-1))
    mt_removal_times.append(mt_rem_time)
    # Mede o tempo de validação da integridade
    mt_val_time = measure_time(lambda: mt.validate())
    mt_validation_times.append(mt_val_time)
    # Mede o uso de memória (shallow)
    mt_mem = mt.memory_usage()
    mt_memory.append(mt_mem)

    # --- Hash Chain ---
    hc = HashChain()
    for i in range(n):
        hc.insert(i)
    # Mede o tempo de inserção
    hc_ins_time = measure_time(lambda: hc.insert(n + 1))
    hc_insertion_times.append(hc_ins_time)
    # Mede o tempo de remoção
    hc_rem_time = measure_time(lambda: hc.remove(len(hc.data)-1))
    hc_removal_times.append(hc_rem_time)
    # Mede o tempo de validação da integridade
    hc_val_time = measure_time(lambda: hc.validate())
    hc_validation_times.append(hc_val_time)
    # Mede o uso de memória (shallow)
    hc_mem = hc.memory_usage()
    hc_memory.append(hc_mem)

# Converter os tempos para milissegundos para facilitar a visualização
mt_insertion_ms = [t * 1000 for t in mt_insertion_times]
hc_insertion_ms = [t * 1000 for t in hc_insertion_times]

mt_removal_ms = [t * 1000 for t in mt_removal_times]
hc_removal_ms = [t * 1000 for t in hc_removal_times]

mt_validation_ms = [t * 1000 for t in mt_validation_times]
hc_validation_ms = [t * 1000 for t in hc_validation_times]

plt.figure(figsize=(10, 8))
plt.plot(sizes, mt_insertion_times, marker='o', label='Merkle Tree')
plt.plot(sizes, hc_insertion_times, marker='o', label='Hash Chain')
plt.xlabel("Número de Elementos")
plt.ylabel("Tempo de Inserção (ms)")
plt.title("Comparação do Tempo de Inserção")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 8))
plt.plot(sizes, mt_removal_times, marker='o', label='Merkle Tree')
plt.plot(sizes, hc_removal_times, marker='o', label='Hash Chain')
plt.xlabel("Número de Elementos")
plt.ylabel("Tempo de Remoção (ms)")
plt.title("Comparação do Tempo de Remoção")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 8))
plt.plot(sizes, mt_validation_times, marker='o', label='Merkle Tree')
plt.plot(sizes, hc_validation_times, marker='o', label='Hash Chain')
plt.xlabel("Número de Elementos")
plt.ylabel("Tempo de Validação (ms)")
plt.title("Comparação do Tempo de Validação")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 8))
plt.plot(sizes, mt_memory, marker='o', label='Merkle Tree')
plt.plot(sizes, hc_memory, marker='o', label='Hash Chain')
plt.xlabel("Número de Elementos")
plt.ylabel("Uso de Memória (bytes)")
plt.title("Comparação do Uso de Memória")
plt.legend()
plt.grid(True)
plt.show()
