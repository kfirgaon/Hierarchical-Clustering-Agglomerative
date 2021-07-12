# -*- coding: utf-8 -*-
"""
Hierarchical-Clustering (Python)
@author: Roman Ratchitski & Kfir Gaon
"""
import time
from datetime import datetime
from sklearn.cluster import AgglomerativeClustering
import HierarchicalClustering as HierarchicalC
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
import os

wordCnt = 1 
splitFlag = True

"""
load_dist_matrix = Func that responsible for the loading of the distance matrix.
Input = Distance matrix from a file.
Output = Array that include the info from the file.
"""
def load_dist_matrix(file):
    npy_array = np.loadtxt(file, delimiter=",", dtype=np.float64)
    return npy_array


"""
distance_matrix_calc = This func will oparate ONLY if the data that we recive
from the file is NOT a distance matrix and we want to make a distance matrix.
Input = An matrix of nX2 that represent a coordinates.
Output = Distance matrix.
"""   
def distance_matrix_calc(data_matrix):
    distance_matrix = pairwise_distances(data_matrix,metric='euclidean')
    return distance_matrix


"""
load_data = This func will oparate ONLY if the data that we recive
from the file is NOT a distance matrix and we want to make a distance matrix.
Input = File with coordinates.
Output = Matrix with dimentions N*2 (each row represent a coordinate (x,y)).
"""
def load_data(file):
    #our Dataset
    global wordCnt
    data = open (file , 'r')                                        #Open the file with the coordinates for reading.
    dataRead = data.read()                                          #Read the data.
     
    dataString = dataRead.replace('\n',',')                         #In case of an "\n" instead of an coordinate, we replace the \n with "," 
    
    for i in range(0 , len(dataString),1):                          #We are counting the number of coordinates.
        if dataString[i] == ',':
            wordCnt+=1
    
    tempDataString = dataString.split(',')                          #Splitting the coordinates.
    for char in tempDataString:                                     #If the file containe an empty coordinate, we remove that one.
        if char == '':
            tempDataString.remove('')
            wordCnt-=1
    
    dataArray = np.array(tempDataString, dtype=np.float64)          #Change the str list to float array.
    data = np.array(dataArray).reshape(int(wordCnt/2),2)            #Change the float array into an 2d coordinate matrix that nX2.
    return distance_matrix_calc(data),distance_matrix_calc(data)    #Calculate the distance matrix and return it.

"""
hc_test = This func is execute clustering.
clustering = system clustering.
Input = distance_matrix.
Output = Clustered information.
"""
def hc_test(distance_matrix):
    global wordCnt
    "============================System Clustering================================================"
    print("System Clustring")
    start_time = time.time()
    system_clusteres = AgglomerativeClustering(n_clusters= 2, linkage='single', affinity='precomputed').fit_predict(distance_matrix)
    print(system_clusteres)
    hc_total_time = time.time() - start_time
    print("System Clustring Completed")
    print("--- %s seconds ---" % hc_total_time)
    print(" ")
    "==========================End System Clustering=============================================="   
    return system_clusteres , hc_total_time                     #Input = distance_matrix // Output = Clustered information.

"""
hc_test_my_opt = This func is execute ours clustering.
Input = distance_matrix.
Output = Clustered information.
"""
def hc_test_my_opt(distance_matrix):
    global wordCnt
    print("My Clustring")
    num_clusters = 2
    start_time = time.time()
    my_clustering = HierarchicalC.hierarchical_clustering_after_opt(distance_matrix,"single", num_clusters)
    print(my_clustering)
    my_hc_opt_total_time = time.time() - start_time
    print("My Clustring Completed")
    print("--- %s seconds ---" % my_hc_opt_total_time)
    print(" ")
    
    return my_clustering , my_hc_opt_total_time

"""
testFromFile = This func is execute all the operations of the program,
include clustering, reding from a file etc.
Input = File.
Output = Clustered information.
"""
def testFromFile(file):
    print("Loading file")
    start_time = time.time()                                        #Start time for the loading file.
    distance_matrix = load_dist_matrix(file)            #The place where we load an distance matrix.
    total_time = time.time() - start_time                           #The end of the loading file.
    print("Distance size: " + str(distance_matrix.shape))          #We are printing for an indication the distance matrix size.
    print("Loading File Completed")
    print("--- %s seconds ---" % total_time)                        #Printing the total time of the loading file.
    print(" ")

    system_clusteres, hc_total_time = hc_test(distance_matrix)     
    my_clustering, my_hc_opt_total_time = hc_test_my_opt(distance_matrix)
    print("--------------------------------------\n")
    
    return system_clusteres,my_clustering,hc_total_time,my_hc_opt_total_time

if __name__ == '__main__':
   
    system_clusteres,my_clustering,hc_total_time,my_hc_opt_total_time = testFromFile('data_2_4.txt')
    
    