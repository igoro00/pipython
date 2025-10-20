"""K-means clustering using pure Python.

This program is intended to group multidimensional data using the k-means
clustering algorithm. The data should be supplied as a CSV file. The clusters
are determined based on the normalized data. The program reports cluster sizes,
the number of algorithm iterations, and the final within-cluster sum of
squares.
"""

import csv
import math
import random
import sys

data = []
min_vals = []
max_vals = []

def distance(point:list[float], center:list[float]):
    temp = 0.0
    for dimension in range(len(point)):
        point_x = normalize(point[dimension], dimension)
        center_x = normalize(center[dimension], dimension)
        temp += (point_x - center_x)**2
    return math.sqrt(temp)

def normalize(val:float, dimension:int)->float:
    range_val = (max_vals[dimension]-min_vals[dimension])
    return (val - min_vals[dimension]) / range_val

def initialize_centers(n_centers:int)->list[list[float]]:
    return random.sample(data, n_centers)

def assign_clusters(centers:list[list[float]])->tuple[list[int], float]:
    labels = []
    wcss = 0.0
    for point in data:
        dists:list[float] = []
        for center in centers:
            dists.append(distance(point, center))
        min_dist = min(dists)
        labels.append(dists.index(min_dist))
        wcss += min_dist**2
    return labels, wcss

def update_centers(centers: list[list[float]], labels: list[int]):
    for c in range(len(centers)):
        cluster = []
        for (i, point) in enumerate(data):
            if labels[i] == c:
                cluster.append(point)
        if len(cluster) > 0:
            unzipped = list(zip(*cluster))
            centers[c] = [sum(dimension)/len(dimension) for dimension in unzipped]

def kmeans(n_clusters):
    centers = initialize_centers(n_clusters)
    old_labels = None
    n_iters = 0
    while True:
        n_iters += 1
        labels, wcss = assign_clusters(centers)
        if labels == old_labels:
            return labels, wcss, n_iters
        update_centers(centers, labels)
        old_labels = labels

def load_data(filename: str)-> list[list[float]]:
    with open(filename, newline='') as f:
        data_reader = csv.reader(f, quoting = csv.QUOTE_NONNUMERIC)
        return list(data_reader)

if __name__ == "__main__":
    data = load_data(sys.argv[-1])
    unzipped = list(zip(*data))
    min_vals = [min(dimension) for dimension in unzipped]
    max_vals = [max(dimension) for dimension in unzipped]
    labels, wcss, n_iters = kmeans(3)
    print("Cluster sizes:")
    for c in range(3):
        print(f"{c + 1} -", labels.count(c))
    print("Iterations:", n_iters)
    print("WCSS:", wcss)