from time import time
import numpy as np
import sys

def fibo(n):
    if n < 2:
        return n
    return fibo(n-1) + fibo(n-2)


def main():
    vector_length = 144
    initial_value = 33

    if len(sys.argv) > 1:
        initial_value = int(sys.argv[1])

    # Vector initialiazing
    vector = np.full(vector_length, initial_value)

    print(f"Inicializacion de vector {vector_length}, valor inicial de {initial_value}")
    print("Procesando")

    ts = time()

    # Vector processing
    for i in range(vector_length):
        vector[i] = fibo(vector[i])
        print(f"Procesando {i}")

    print(f"Tiempo total: {time() - ts:.2f} ")
    print("Primeros vectores diez procesados", vector[:10])
    print("Ultimos diez vectores procesados", vector[-10:])

if __name__ == "__main__":
    main()
