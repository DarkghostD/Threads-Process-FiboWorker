from threading import Thread
from time import time
import numpy as np
import multiprocessing
import sys

def fibo(n):
    if n < 2:
        return n
    return fibo(n-1) + fibo(n-2)

class FiboWorker(Thread):
    def __init__(self, vector, startIndex, endIndex):
        Thread.__init__(self)
        self.vector = vector
        self.startIndex = startIndex
        self.endIndex = endIndex

    def run(self):
        for i in range(self.startIndex, self.endIndex):
            self.vector[i] = fibo(self.vector[i])
        print(f"[{self.name}] Procesado desde {self.startIndex} hasta {self.endIndex-1}")

def main():
    vectorLength = 144
    initialValue = 33

    if len(sys.argv) > 1:
        initialValue = int(sys.argv[1])

    num_cpus = multiprocessing.cpu_count()

    # Inicializar el vector
    vector = np.full(vectorLength, initialValue)

    print(f"Procesando un vector de longitud {vectorLength} con valor inicial {initialValue}")
    print(f"Utilizando {num_cpus} hilos")

    # Dividir el trabajo entre los hilos
    chunk_size = vectorLength // num_cpus
    hilos = []

    ts = time()

    for x in range(num_cpus):
        startIndex = x * chunk_size
        endIndex = startIndex + chunk_size if x < num_cpus - 1 else vectorLength
        print(f"Trabajador {x} comienza")
        worker = FiboWorker(vector, startIndex, endIndex)
        worker.start()
        hilos.append(worker)

    for x, hilo in enumerate(hilos):
        print(f"Esperando por trabajador {x}")
        hilo.join()

    print(f"Tiempo de ejecución: {time() - ts:.2f} segundos")
    print("Primeros 10 elementos del vector procesado:", vector[:10])
    print("Últimos 10 elementos del vector procesado:", vector[-10:])

if __name__ == "__main__":
    main()
