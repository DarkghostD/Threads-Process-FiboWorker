import multiprocessing
from time import time
import numpy as np

def fibo(n):
    if n < 2:
        return n
    return fibo(n-1) + fibo(n-2)

class FiboWorker(multiprocessing.Process):
    def __init__(self, vector, startIndex, endIndex, result_queue):
        multiprocessing.Process.__init__(self)
        self.vector = vector
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.result_queue = result_queue

    def run(self):
        for i in range(self.startIndex, self.endIndex):
            self.vector[i] = fibo(self.vector[i])
        self.result_queue.put((self.startIndex, self.endIndex, self.vector[self.startIndex:self.endIndex]))

def main():
    vectorLength = 144
    initial_value = 33
    num_cpus = multiprocessing.cpu_count()

    # Inicializar el vector
    vector = np.full(vectorLength, initial_value)

    print(f"Procesando un vector de longitud {vectorLength} con valor inicial {initial_value}")
    print(f"Utilizando {num_cpus} CPUs")

    # Dividir el trabajo entre los CPUs disponibles
    chunk_size = vectorLength // num_cpus
    processes = []
    result_queue = multiprocessing.Queue()

    ts = time()

    for i in range(num_cpus):
        startIndex = i * chunk_size
        endIndex = startIndex + chunk_size if i < num_cpus - 1 else vectorLength
        worker = FiboWorker(vector, startIndex, endIndex, result_queue)
        processes.append(worker)
        worker.start()

    # Recolectar resultados
    for _ in range(num_cpus):
        start, end, partial_result = result_queue.get()
        vector[start:end] = partial_result

    # Esperar a que todos los procesos terminen
    for process in processes:
        process.join()

    print(f"Tiempo total de ejecución: {time() - ts:.2f} segundos")
    print("Primeros 10 elementos del vector procesado:", vector[:10])
    print("Últimos 10 elementos del vector procesado:", vector[-10:])

if __name__ == "__main__":
    main()
