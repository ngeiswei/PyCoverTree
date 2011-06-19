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
from naiveNN import NN
from pylab import sqrt, dot, plot, show
from numpy import subtract
# from scipy import random
from random import random, seed
import time

def distance(p, q):
    # print "p =", p
    # print "q =", q
    x = subtract(p, q)
    return sqrt(dot(x, x))

def test_covertree():
    seed(1)

    n_points = 1000
    
    pts = [(random(), random()) for _ in xrange(n_points)]

    # print X

    gt = time.time
    
    t = gt()
    ct = CoverTree(distance, Node(pts[0]), 10)
    for i in xrange(1, len(pts)):
        ct.insert(Node(pts[i]))
    b_t = gt() - t
    print "Time to build a cover tree of", n_points, "2D points:", b_t, "seconds"

    query = (0.5,0.5)
    #cover-tree nearest neighbor
    t = gt()
    result = ct.nearest_neighbor(Node(query))
    print "result =", result
    ct_t = gt() - t
    print "Time to run a cover tree NN query:", ct_t, "seconds"
    
    #standard nearest neighbor
    t = gt()
    resultNN = NN(query, pts, distance)
    print "resultNN =", resultNN
    n_t = gt() - t
    print "Time to run a naive NN query:", n_t, "seconds"

    print "result =", result
    print "resultNN =", resultNN
    if(distance(result.data, resultNN) != 0):
        print "This is bad"
        print result.data, "!=", resultNN
    else:
        print "This is good"
        print "Cover tree query is", n_t/ct_t, "faster"

    plot(pts[0], pts[1], 'rx')
    plot([query[0]], [query[1]], 'go')
    plot([resultNN[0]], [resultNN[1]], 'y^')
    plot([result.data[0]], [result.data[1]], 'mo')
    

    # printDotty prints the tree that was generated in dotty format,
    # for more info on the format, see http://graphviz.org/
    # ct.printDotty()

    # show()


if __name__ == '__main__':
    test_covertree()
