#!/usr/bin/env python
#
#File: test_covertree.py
#Author: Thomas Kollar
#email: tkollar@csail.mit.edu
#Date: 11/20/08
#All Rights Reserved. Copyright Thomas Kollar 2007
#
#
#
#  This is a tester for the cover tree nearest
#  neighbor algorithm.  For more information
#  please refer to the technical report entitled
#  "Fast Nearest Neighbors" by Thomas Kollar
#  or to "Cover Trees for Nearest Neighbor" by
#  John Langford, Sham Kakade and Alina Beygelzimer
#  
#  If you use this code in your research, kindly refer to the 
#  technical report.

from covertree import CoverTree, Node
import time
from nearest_neighbor import *
from pylab import *
from scipy import random

def test_covertree():
    random.seed(1)

    n_points = 10000
    
    # fill an array of dimension (2, n_points) with random numbers in [0,1)
    X = random.random((2, n_points))

    gt = time.time
    
    t = gt()
    ct = CoverTree(Node(X[:,0]), 10)
    for i in range(1, len(X[0])):
        ct.insert(Node(X[:,i]))
    print "Time to build a cover tree of", n_points, "2D points:", gt() - t, "seconds"

    query = [0.5,0.5]
    #cover-tree nearest neighbor
    t = gt()
    result = ct.nearest_neighbor(Node(query))
    print "Time to run a cover tree NN query:", gt() - t, "seconds"
    
    #standard nearest neighbor
    t = gt()
    resultNN = NN(query, X)
    print "Time to run a naive NN query:", gt() - t, "seconds"
    
    if(result.d(Node(resultNN)) != 0):
        print "this is bad"
        print result.data, resultNN

    plot(X[0], X[1], 'rx')
    plot([query[0]], [query[1]], 'go')
    plot([resultNN[0]], [resultNN[1]], 'y^')
    plot([result.data[0]], [result.data[1]], 'mo')
    

    #printDotty prints the tree that was generated
    # in dotty format, for more info on the format, see
    # http://graphviz.org/
    # ct.printDotty()
    
    # show()


if __name__ == '__main__':
    test_covertree()
