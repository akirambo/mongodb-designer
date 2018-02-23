
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys
from sklearn.cluster import KMeans

def main():
    headers = []
    elems = []
    num_of_args = len(sys.argv)
    num_of_clusters = 20
    if num_of_args != 2 and num_of_args != 3:
        sys.exit('Please set arguments\n\t run.py FILENAME [NUMBER_OF_CLUSTERES(deault: 20])')

    if num_of_args == 3:
        num_of_clusters = int(sys.argv[2])
    filename = sys.argv[1]
    for i in range(10):
        for name in ['col', 'pid', 'p', 'car', 'find', 'write', 'cond']:
            headers.append(name + str(i))
    data = pd.read_csv(filename, names=headers)
    for i in range(10):
        for name in ['col', 'pid', 'p', 'car', 'find', 'write', 'cond']:
            elems.append(data[name + str(i)].tolist())
    print("NUMBER OF CLUSTERS", num_of_clusters)
    # Convert Dataframe(Pandas) to numpy array
    data2 = np.array(elems, np.int32)
    # Transpose data
    data2 = data2.T
    # k-means
    km = KMeans(n_clusters=num_of_clusters)
    result = km.fit_predict(data)
    # Show Samples for each cluster
    data['cluster_id'] = result
    np.savetxt('data/category.csv', data["cluster_id"], delimiter=' ', fmt='%i')
    print(data['cluster_id'].value_counts())
    # smaller value is better
    # print(km.inertia_)
    # print ('Distortion: %.2f'% km.inertia_)

if __name__ == "__main__":
    main()
