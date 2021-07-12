# -*- coding: utf-8 -*-
"""
Hierarchical-Clustering (Python)
@author: Roman Ratchitski & Kfir Gaon
"""
import numpy as np
import sys
    
    
def hierarchical_clustering_before_opt(input,linkage,no_of_clusters):
    clusters = {}
    row_index = -1
    col_index = -1
    array = []
    

    for n in range(input.shape[0]):
        array.append(n)

    clusters[0] = array.copy()

    for k in range(1, input.shape[0]):
        #for Single Linkage
        if(linkage == "single" or linkage =="Single"):
            np.fill_diagonal(input,sys.maxsize)
            min_val = sys.maxsize
            for i in range(0,input.shape[0]):
                for j in range(0,i):
                    if(input[i][j]<=min_val):
                        min_val = input[i][j]
                        row_index = i
                        col_index = j
            for i in range(0,input.shape[0]):
                if(i != col_index):
                    #we calculate the distance of every data point from newly formed cluster and update the matrix.
                    if(i > col_index):
                        firstValue = input[i][col_index]
                    else:
                        firstValue = input[col_index][i] 
                    if(i > row_index):
                        secValue = input[i][row_index] 
                    else:
                        secValue = input[row_index][i]
                    temp = min(firstValue,secValue)
                    #elif(i < col_index):
                        #temp = min(input[col_index][i],input[row_index][i])
                    #we update the matrix symmetrically as our distance matrix should always be symmetric
                    input[col_index][i] = temp
                    #input[i][col_index] = temp
                
        
        if(linkage == "single" or linkage =="Single"):
            for i in range (0,input.shape[0]):
                input[row_index][i] = sys.maxsize
                input[i][row_index] = sys.maxsize
        
        #Manipulating the dictionary to keep track of cluster formation in each step
        #if k=0,then all datapoints are clusters
        minimum = min(row_index,col_index)
        maximum = max(row_index,col_index)
        for n in range(len(array)):
            if(array[n]==maximum):
                array[n] = minimum
        clusters[k] = array.copy()
        
    return clusters
    

def hierarchical_clustering_after_opt(dist_mtx,linkage, n_clusters=2):
    #shape that returns a tuple with each index having the number of corresponding elements.
    #Which means that the array has n dimensions, and each dimension has n elements.
    num_of_points = dist_mtx.shape[0];          
    
    # clusters as size of the points, in the end it will be size 'n_clusters'
    clusters_list = [[i] for i in range(num_of_points)]                         #We init the cluster list with the coordinates list. At the begining each coordinate is a cluster.
    result_clusters = np.zeros(shape=(num_of_points), dtype=np.int32)

    dist_mtx = np.copy(dist_mtx)
    dist_mtx[dist_mtx == 0] = np.nan                                            #We are putting nan (value that not number) at the main diagonal.
    
    min_index = np.zeros(shape=(num_of_points), dtype=np.float64)               #min_index is array that store the index of the min value, at size "num_of_points", type - float64.
    min_index_val = np.zeros(shape=(num_of_points), dtype=np.float64)           #min_index_val is array that store the value of the min index, at size "num_of_points", type - float64.
    for i in range(num_of_points):                                              #Find the min value at each column.
        min_values_location = np.where(dist_mtx[:,i]==np.nanmin(dist_mtx[:,i]))
        min_index[i] = min_values_location[0][0]                                # The index is the col, The value is the row at the distance matrix.
        min_index_val[i] = dist_mtx[min_values_location[0][0], i]               # The index is the col, The value is the row at the distance matrix.


    n_clusters_current = num_of_points                                          #n_clusters_current = is to insure the number of clusters.
    # iterate until we have n_clusters clusters
    while n_clusters_current > n_clusters:
        #We take the min value from the min_index_val
        min_values_location = np.where(min_index_val==np.nanmin(min_index_val)) 
        #min_i is the row index
        min_i = min_values_location[0][0]
        #min_j is the col index
        min_j = np.int64(min_index[min_i])
        if min_j < min_i:
            min_i, min_j = min_j, min_i

        # single-linkage clustering, replace the col&row as min of i, j
        dist_mtx[:,min_i] = np.minimum(dist_mtx[:, min_i], dist_mtx[:, min_j])  #The minimum is equivalent to np.where(x1 <= x2, x1, x2) 
        dist_mtx[min_i,:] = np.minimum(dist_mtx[min_i, :], dist_mtx[min_j, :])  #The minimum is equivalent to np.where(x1 <= x2, x1, x2) 

        # unite the two closest clusters
        clusters_list[min_i].extend(clusters_list[min_j])
        clusters_list[min_j].clear()

        min_index[min_j] = np.nan
        min_index_val[min_j] = np.nan
        min_index[min_index == min_j] = min_i

        min_values_location = np.where(dist_mtx[:,min_i]==np.nanmin(dist_mtx[:,min_i]))
        min_index[min_i] = min_values_location[0][0]
        min_index_val[min_i] = dist_mtx[min_values_location[0][0], min_i]

        n_clusters_current -= 1


    cluster_in = 0
    # post-processing, calculating the clusters vector
    for cluster_i, cluster in enumerate(clusters_list):
        if len(cluster) == 0:
            continue

        for i in cluster:
            result_clusters[i] = cluster_in

        cluster_in += 1

    return result_clusters