from mpi4py import MPI
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score

comm = MPI.COMM_WORLD
numprocs = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    df = pd.read_csv('car.data.csv', delimiter=',')

    df.rename(columns={'vhigh': 'buying', 'vhigh.1': 'maint',
                       '2': 'doors', '2.1': 'persons',
                       'small': 'lug_boot', 'low': 'safety'}, inplace=True)
    df = df.drop('unacc', axis=1)

    # Приводим все значения в таблице к численным значениям

    df.loc[(df.buying == 'vhigh'), ('buying', 'maint')] = int(5)
    df.loc[(df.buying == 'high'), ('buying', 'maint')] = int(4)
    df.loc[(df.buying == 'med'), ('buying', 'maint')] = int(3)
    df.loc[(df.buying == 'low'), ('buying', 'maint')] = int(2)

    df.loc[(df.lug_boot == 'big'), 'lug_boot'] = int(4)
    df.loc[(df.lug_boot == 'med'), 'lug_boot'] = int(3)
    df.loc[(df.lug_boot == 'small'), 'lug_boot'] = int(2)

    df.loc[(df.doors == '5more'), 'doors'] = int(5)
    df.loc[(df.persons == 'more'), 'persons'] = int(5)

    df.loc[(df.safety == 'high'), 'safety'] = int(4)
    df.loc[(df.safety == 'med'), 'safety'] = int(3)
    df.loc[(df.safety == 'low'), 'safety'] = int(2)
    # print(df.head())

    # Создаем выборку значений для кластеризации

    x = df.values[:]
    for i in range(len(x)):
        for j in range(6):
            x[i, j] = float(x[i, j]) / 5
    y = np.array(x.flatten(), dtype=float)

else:
    y = np.zeros(shape=(10362,), dtype=float)

t_start = MPI.Wtime()
comm.Bcast([y, MPI.FLOAT], root=0)
index_dbi = np.ndarray(1, dtype=float)
index_dbi[0] = 5
max_index = np.ndarray(1, dtype=float)
max_index[0] = 10

y = np.reshape(y, (1727, 6))

# Кластеризизируем данные и вычисляем индекс Дависа-Болдуина

num_clusters = rank + 2
for i in range(3):
    # Метод к-средних - KMeans
    km = KMeans(init='k-means++', n_clusters=num_clusters, random_state=42)
    km.fit(y)
    labels = km.labels_
    # Индекс Дависа-Болдуина
    RS_score = davies_bouldin_score(y, labels)
    ss = float(RS_score)
    if ss < index_dbi[0]:
        index_dbi[0] = ss

print(f"I'm {rank} rank, my index_dbi = {index_dbi[0]} for {num_clusters} clusters")

comm.Barrier()
comm.Reduce(index_dbi, max_index, op=MPI.MIN, root=0)

t_diff = MPI.Wtime() - t_start

if rank == 0:
    print(f'Best dbi index equal: {max_index[0]}')
    print('Time worked programm equal: {0}'.format(t_diff))