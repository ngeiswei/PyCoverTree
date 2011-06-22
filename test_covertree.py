#!/usr/bin/env python
#
# File: test_covertree.py
# Date of creation: 11/20/08
# Copyright (c) 2007, Thomas Kollar <tkollar@csail.mit.edu>
# Copyright (c) 2011, Nil Geisweiller <ngeiswei@gmail.com>
# All rights reserved.
#
# This is a tester for the cover tree nearest neighbor algorithm.  For
# more information please refer to the technical report entitled "Fast
# Nearest Neighbors" by Thomas Kollar or to "Cover Trees for Nearest
# Neighbor" by John Langford, Sham Kakade and Alina Beygelzimer
#  
# If you use this code in your research, kindly refer to the technical
# report.

from covertree import CoverTree
from naiveknn import knn
from pylab import sqrt, dot, plot, show
from numpy import subtract
# from scipy import random
from random import random, seed
import time

def distance(p, q):
    # print "distance"
    # print "p =", p
    # print "q =", q
    x = subtract(p, q)
    return sqrt(dot(x, x))

def test_covertree():
    seed(1)

    n_points = 1000

    k = 1
    
    pts = [(random(), random()) for _ in xrange(n_points)]

    gt = time.time
    
    t = gt()
    ct = CoverTree(distance)
    for p in pts:
        ct.insert(p)
    b_t = gt() - t
    print "Time to build a cover tree of", n_points, "2D points:", b_t, "seconds"

    query = (0.5,0.5)
    #cover-tree nearest neighbor
    t = gt()
    results = ct.knn(query, k)
    # print "result =", result
    ct_t = gt() - t
    print "Time to run a cover tree NN query:", ct_t, "seconds"
    
    # standard nearest neighbor
    t = gt()
    naive_results = knn(query, pts, distance, k)
    # print "resultNN =", resultNN
    n_t = gt() - t
    print "Time to run a naive NN query:", n_t, "seconds"

    if all([distance(r, nr) != 0 for r, nr in zip(results, naive_results)]):
        print "This is bad"
        print results, "!=", naive_results
    else:
        print "This is good"
        print "Cover tree query is", n_t/ct_t, "faster"


    # test find
    if ct.find(results[0]):
        print "This is good (covertree.find works)"
    else:
        print "This is bad (covertree.find doesn't work)"

    plot(pts[0], pts[1], 'rx')
    plot([query[0]], [query[1]], 'go')
    plot([naive_results[0][0]], [naive_results[0][1]], 'y^')
    plot([results[0][0]], [results[0][1]], 'mo')
    

    # printDotty prints the tree that was generated in dotty format,
    # for more info on the format, see http://graphviz.org/
    # ct.printDotty()

    # show()


if __name__ == '__main__':
    test_covertree()
