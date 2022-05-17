import threading
import numpy as np
from time import time

d1, s1, d2, s2 = 12, 12, 10, 10

# Создаем матрицы
M1 = np.random.randint(0, 100, (2**d1, 2**s1))
M2 = np.random.randint(0, 100, (2**d2, 2**s2))
M3 = np.zeros((2**d1, 2**s1))

print("Matrix M1: \n", M1)
print("Matrix M2: \n", M2)

# Считаем отношение размера матриц
dt = int(2**d1/2**d2)
# print("dt: \n", dt)

# количество шагов для второй матрицы
attitude1 = int(2**d1 / dt)
#attitude2 = int(2**d2 / dt)
# print("at1: \n", attitude1, "\nat2: \n", attitude2)

# Шаг
#step1 = int(attitude1 / 2)
#step2 = int(attitude2 / 2)
# print("step1: \n", step1, "\nstep2: \n", step2)

# Создаем задачу для потоков
def thread_task(start1, finish1, start2, finish2, M3, M2, M1):
    for i in range(start1, finish1):
        for j in range(start2, finish2):
            #lock.acquire()
            M3[dt*i:dt*(i+1), dt*j:dt*(j+1)] = M1[dt*i:dt*(i+1), dt*j:dt*(j+1)] - M2[i, j]
            #lock.release()

# Исполняемая функция с потоками
def main_task():
    #global M1, M2, M3
    #global dt, attitude1

    # создаем блокировку
    #lock = threading.Lock()

    # создаем потоки
    t1 = threading.Thread(target=thread_task,
                          args=(0, int(attitude1/4), 0, int(attitude1/4), M3, M2, M1, ))
    t2 = threading.Thread(target=thread_task,
                          args=(0, int(attitude1/4), int(attitude1/4), int(attitude1/2), M3, M2, M1, ))
    t3 = threading.Thread(target=thread_task,
                          args=(0, int(attitude1/4), int(attitude1 / 2), int(attitude1 * 0.75), M3, M2, M1,))
    t4 = threading.Thread(target=thread_task,
                          args=(0, int(attitude1/4), int(attitude1 * 0.75), int(attitude1), M3, M2, M1,))

    t5 = threading.Thread(target=thread_task,
                          args=(int(attitude1/4), int(attitude1 / 2), 0, int(attitude1 / 4), M3, M2, M1,))
    t6 = threading.Thread(target=thread_task,
                          args=(int(attitude1/4), int(attitude1 / 2), int(attitude1/4), int(attitude1/2), M3, M2, M1,))
    t7 = threading.Thread(target=thread_task,
                          args=(int(attitude1/4), int(attitude1 / 2), int(attitude1 / 2), int(attitude1 * 0.75), M3, M2, M1,))
    t8 = threading.Thread(target=thread_task,
                          args=(int(attitude1/4), int(attitude1 / 2), int(attitude1 * 0.75), int(attitude1), M3, M2, M1,))

    t9 = threading.Thread(target=thread_task,
                          args=(int(attitude1/2), int(attitude1 * 0.75), 0, int(attitude1/4), M3, M2, M1,))
    t10 = threading.Thread(target=thread_task,
                          args=(int(attitude1/2), int(attitude1 * 0.75), int(attitude1/4), int(attitude1/2), M3, M2, M1,))
    t11 = threading.Thread(target=thread_task,
                          args=(int(attitude1 / 2), int(attitude1 * 0.75), int(attitude1/2), int(attitude1 * 0.75), M3, M2, M1,))
    t12 = threading.Thread(target=thread_task,
                          args=(int(attitude1 / 2), int(attitude1 * 0.75), int(attitude1 * 0.75), int(attitude1), M3, M2, M1,))

    t13 = threading.Thread(target=thread_task,
                          args=(int(attitude1 * 0.75), int(attitude1), 0, int(attitude1 / 4), M3, M2, M1,))
    t14 = threading.Thread(target=thread_task,
                           args=(int(attitude1 * 0.75), int(attitude1), int(attitude1 / 4), int(attitude1 / 2), M3, M2, M1,))
    t15 = threading.Thread(target=thread_task,
                           args=(int(attitude1 * 0.75), int(attitude1), int(attitude1 / 2), int(attitude1 * 0.75), M3, M2, M1,))
    t16 = threading.Thread(target=thread_task,
                           args=(int(attitude1 * 0.75), int(attitude1), int(attitude1 * 0.75), int(attitude1), M3, M2, M1,))

    # начало работы потоков
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()

    # Ждем пока каждый поток завершит работу
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
    t11.join()
    t12.join()
    t13.join()
    t14.join()
    t15.join()
    t16.join()

if __name__ == "__main__":
    start_ap = time()

    for i in range(3):
        main_task()

    stop_ap = time()

    print("Matrix M3: \n", M3)
    print("Elapsed time: ", f'{stop_ap - start_ap}')