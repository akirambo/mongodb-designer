
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def main():
    headers = []
    elems = []
    num_of_args = len(sys.argv)
    max_of_clusters = 11
    min_of_clusters = 1
    if num_of_args != 2 and num_of_args != 3 and num_of_args != 4:
        sys.exit('Please set arguments\n\t run.py FILENAME [MAX(default:11)] [MIN(default:1)]')

    if num_of_args == 3:
        max_of_clusters = int(sys.argv[2])
    elif num_of_args == 4:
        min_of_clusters = int(sys.argv[3])
    filename = sys.argv[1]
    for i in range(10):
        for name in ['col', 'pid', 'p', 'car', 'find', 'write', 'cond']:
            headers.append(name + str(i))
    data = pd.read_csv("debug.csv", names=headers)
    for i in range(10):
        for name in ['col', 'pid', 'p', 'car', 'find', 'write', 'cond']:
            elems.append(data[name + str(i)].tolist())
    print("NUMBER OF CLUSTERS", num_of_clusters)
    # Convert Dataframe(Pandas) to numpy array
    data2 = np.array(elems, np.int32)
    # Transpose data
    data2 = data2.T
    # k-means
    distortions = []
    for i  in range(min_of_clusters, max_of_clusters):
        print("Trial", i)
        km = KMeans(n_clusters=i,
                    init='k-means++',
                    n_init=10,
                    max_iter=300,
                    random_state=0)
        km.fit(data)                    
        distortions.append(km.inertia_)   # km.fitするとkm.inertia_が得られる
    plt.plot(range(1,11),distortions,marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()

if __name__ == "__main__":
    main()
