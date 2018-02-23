
python bin/random_execute.py

# To decide the number of clusters.
# python bin/elbow.py data/data.csv

python bin/kmeans.py data/data.csv 3

python bin/generate_trainingdata.py data/data.csv data/category.csv

python modelbank_gen.py data/data_with_category.csv
