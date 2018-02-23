# mongodb-designer

## What does MongoDB designer do
It is diffcult and costly work to decide physical design for MongoDB ( indexing, sharding, denormalization). To reduce designing work. This tool decide physical design for a target workload using the data set of previous execution. This tool is also able to generate training data (it requires mongodb service).

## Requierments
Python 3.x ~


## How to collect training data
### 1. Execute queries randomly & collect information
Execute mongodb queries & Collect Metrics & Performance data (debug.csv)
input : None
output : data/data.csv
```
Overview:
        Parameter Generator

        Usage:
	random_execute.py [-c <D>] [-d <D>] [-f <D>] [-i <D>] [-m <D>]
               [-o <NAME>] [-q <D>] [-s <D>] [-w <D>]
               [--server <IP_ADDRESS>] [--port <PORT>]
               [--database <NAME>] [--collection <NAME>]
               [--no-run <True/False>] [--tracer <True/False>]
```


## How to design your workload
### 1. Execute Elbow Method to decide the number of clusters
input : data/data.csv
output : graph
```
Overview:
	python elbow.py data/data.csv
```

### 2. Execute Clustering (k-means)
Execute kmeans analysis
input : data/data.csv
output : data/category.csv  
```
Overview:
	python kmeans.py data/data.csv [NUMBER_OF_CLUSTERS(default: 20)]
```

### 3. Generate Training data
Execute kmeans analysis and Generate Training data
input : data/data.csv, data/category.csv
output : data/data_with_category.csv, data/training_data.csv
```
Overview:
	python generate_trainingdata.py data/data.csv data/category.csv
```

### 4. Generate Model Bank
Execute kmeans analysis and Generate Training data
input : data/data_with_category.csv
output : data/datamodel_meta.csv  
```
Overview:
	python modelbank_gen.py data/data_with_category.csv
```

## How to Training

```
Overview:
	python bin/ml_workload_classify.py data/training_data.csv
```

## License
Copyright (c) 2017, Carnegie Mellon University. All rights reserved.
