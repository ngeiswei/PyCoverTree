# File: naiveNN.py
# Author: Nil Geisweiller
# email: ngeiswei@gmail.com
# Date: 
# All Rights Reserved. Copyright Nil Geisweiller 2011
#
# This function to perform maive nearest neighbors.

from heapq import nsmallest 

def kNN(pt, pts, dist_f, k = 1):
    '''Return the k-nearest points in pts to pt using a naive
    algorithm. dist_f is a function that computes the distance between
    2 points'''
    return nsmallest(k, pts, lambda x: dist_f(pt, x))

def NN(pt, pts, dist_f):
    '''Like kNN but return the nearest point in pts'''
    return kNN(pt, pts, dist_f)[0]
