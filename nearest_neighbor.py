#File: nearest_neighbor.py
#Author: Thomas Kollar
#email: tkollar@csail.mit.edu
#Date: 11/20/08
#All Rights Reserved. Copyright Thomas Kollar 2007
#
#
#  This is a set of functions for performing simple nearest neighbors.

import sys
from scipy import *
from copy import *
import time
from random import *
from pylab import *
from sorting import quicksort

def NNs(inPts, modPts):
    return transpose(list(NN(inPts[:,i], modPts) for i in range(len(inPts[0]))))

def NN(pt, pts):
    minElt = pts[:,0]
    minDist = distance(minElt, pt)
    
    for i in range(len(pts[0])):
        if(distance(pts[:,i], pt) < minDist):
            minElt = pts[:,i]
            minDist = distance(pts[:,i], pt)
                
    return minElt

def kNN(pt, pts, num=1):
    pts = array(pts)
    minElt = pts[0]
    dists = []

    #get the distsances to each of the points
    for oPt in pts:
        dists.append(distance(oPt, pt))

    sort_dists, I = quicksort(dists)

    knn_pts = []
    for i in range(num):
        knn_pts.append(pts[I[i]])
    
    return array(knn_pts), I[0:num], sort_dists[0:num]


def kNN_g0(pt, pts, num=1):
    pts = array(pts)
    minElt = pts[0]
    dists = []

    #get the distsances to each of the points
    for oPt in pts:
        dists.append(distance(oPt, pt))

    sort_dists, I = quicksort(dists)

    #while we don't have enough points, keep adding them
    knn_pts = []
    knn_ind = []
    knn_dist = []
    i=0

    while(len(knn_pts)<num and i<len(pts)):
        if(not sort_dists[i]==0):
            knn_pts.append(pts[I[i]])
            knn_ind.append(I[i])
            knn_dist.append(sort_dists[i])
        i=i+1
    
    return array(knn_pts), knn_ind, knn_dist

def distance(p, q):
    x = p-q
    return sqrt(dot(x, x))

def test1():
    a = range(10)
    a.reverse()
    print a 
    for i in range(10):
        myNN, indexset, dists = kNN(1, a, i)
        myNN2, indexset2, dists2 = kNN_g0(1, a, i)

        print "1****"
        print myNN
        print indexset
        print dists
        print "2****"
        print myNN2
        print dists2
        print indexset2

def test2():
    a = range(10)

    test_set = []
    for i in a:
        test_set.append([i,i])
    test_set.reverse()

    test_set = array(test_set)
    print test_set
    
    for i in range(10):
        myNN, indexset, dists = kNN([1,1], test_set, i)
        myNN2, indexset2, dists2 = kNN_g0([1,1], test_set, i)

        print ">>>>>>>>>>", i, "<<<<<<<<<<<"
        print "1****"
        print myNN
        #print indexset
        #print dists
        print "2****"
        print myNN2
        #print dists2
        #print indexset2



    
if __name__=="__main__":
    test1()
    #test2()
    #test4()
