# File: covertree.py
# Date of creation: 05/04/07
# Copyright (c) 2007, Thomas Kollar <tkollar@csail.mit.edu>
# Copyright (c) 2011, Nil Geisweiller <ngeiswei@gmail.com>
# All rights reserved.
#
# This is a class for the cover tree nearest neighbor algorithm.  For
# more information please refer to the technical report entitled "Fast
# Nearest Neighbors" by Thomas Kollar or to "Cover Trees for Nearest
# Neighbor" by John Langford, Sham Kakade and Alina Beygelzimer
#  
# If you use this code in your research, kindly refer to the technical
# report.

from copy import deepcopy
from random import choice
import sys

class CoverTree:

    #the Node representation of the data
    class Node:
        #data is an array of values
        def __init__(self, data=None):
            self.data = data
            self.children = {}      # dict mapping level and children
            self.parent = None
    
        #addChild adds a child to a particular Node and a given level
        def addChild(self, child, level):
            try:
                # in case level is not in self.children yet
                if(child not in self.children[level]):
                    self.children[level].append(child)
            except(KeyError):
                self.children[level] = [child]
            child.parent = self
    
        #getChildren gets the children of a Node at a particular level
        def getChildren(self, level):
            retLst = [self]
            try:
                retLst.extend(self.children[level])
            except(KeyError):
                pass
            
            return retLst
    
        def removeConnections(self, level):
            if(self.parent != None):
                #print self.parent.children
                self.parent.children[level+1].remove(self)
                self.parent = None
    
        def __str__(self):
            return str(self.data)
        
        def __repr__(self):
            return str(self.data)

    
    #
    # Overview: initalization method
    #
    # Input: distance function, root, maxlevel, minlevel Here root is
    #  a point, maxlevel is the largest number that we care about
    #  (e.g. base^(maxlevel) should be our maximum number), just as
    #  base^(minlevel) should be the minimum distance between Nodes.
    # Output:
    #
    def __init__(self, distance, root = None,
                 maxlevel = 10, minlevel = -10, base = 2):
        self.distance = distance
        self.root = root
        self.maxlevel = maxlevel
        self.minlevel = minlevel
        self.base = base


    #
    #Overview: insert an element p into the tree
    #
    #Input: p
    #Output: True if the node is inserted, False otherwise
    #
    def insert(self, p):
        if self.root == None:
            self.root = self.Node(p)
        else:
            return self.insert_rec(p, [self.root], self.maxlevel)

    #
    # Overview: get the nearest neighbor of an element
    #
    # Input: point p
    #
    # Output: Nearest point with respect to the distance metric
    #          self.distance()
    #
    def nearest_neighbor(self, p):
        return self.nearest_neighbor_iter(p).data

    #
    # Overview: find an element in the tree
    #
    # Input: Node p
    # Output: The Node if it exists as well as the level on
    #           which it was found
    #
    def find(self, p):
        return self.find_rec(p, [self.root], self.maxlevel)


    #
    #Overview:insert an element p in to the cover tree
    #             based on the current level, recursive
    #
    #Input: point p, Cover Qi(list of nodes?), integer level i
    #Output: boolean, True if the node is not inserted, False otherwise
    #
    def insert_rec(self, p, Qi, i):
        # print "p =", p
        # get the children of the current level
        # and the distance o the nearest child
        # TODO distances of Qi is computed as well and is redundant with (3) and (4)
        Q, Q_p_ds = self.getChildren(p, Qi, i)
        
        d_p_Q = min(Q_p_ds)
        
        if(d_p_Q == 0.0):
            print "already an element", p
            return True

        if(d_p_Q > self.base**i):
            return False
        else:
            #construct Q_i-1
            Qi_next = [q for q, d in zip(Q, Q_p_ds) if d <= self.base**i]
            # TODO (3)
            d_p_Qi = self.getDist(p, Qi)
            
            myIns = self.insert_rec(p, Qi_next, i-1)
            if(not myIns and d_p_Qi <= self.base**i):
                # TODO (4)
                possParents = [q for q in Qi
                               if self.distance(p, q.data) <= self.base**i]
                choice(possParents).addChild(self.Node(p), i)
                return True
            else:
                return myIns
            
    #
    #Overview:get the nearest neighbor, iterative
    #
    #Input: query point p
    #Output: the nearest Node 
    #
    def nearest_neighbor_iter(self, p):
        Qcurr = [self.root]
        for l in reversed(xrange(self.minlevel, self.maxlevel + 1)):

            #get the children of the current Q and
            #the best distance at the same time
            Q, Q_p_ds = self.getChildren(p, Qcurr, l)

            d_p_Q = min(Q_p_ds)

            #create the next set
            Qcurr = [q for q, d in zip(Q, Q_p_ds) if d <= d_p_Q + self.base**l]

        #find the minimum
        return self.arg_min(p, Qcurr)

    #
    # Overview: find an element given a particular level, recursive
    #
    # Input: point p to find, cover set Qi, current level i
    #
    # Output: True if p is found False otherwise and the level of p
    #
    def find_rec(self, p, Qi, i):
        #get the children of the current level
        Q, Q_p_ds = self.getChildren(p, Qi, i)
        Qi_next = [q for q, d in zip(Q, Q_p_ds) if d <= self.base**i]
        d_p_Qi = self.getDist(p, Qi)

        # TODO can be simplified 
        if(i < self.minlevel):
            print "Point not found"
            return False, None
        elif(d_p_Qi == 0):
            return True, i
        else:
            return self.find_rec(p, Qi_next, i-1)


    #
    # Overview: get the children of cover set Qi at level i
    #
    # Input: point p to compare the distance with Qi
    #
    # Output: the children of Qi and the distances of them with point p
    #
    def getChildren(self, p, Qi, i):
        Q = sum([j.getChildren(i) for j in Qi], [])
        Q_p_ds = [self.distance(p, q.data) for q in Q]
        return Q, Q_p_ds

    #
    # Overview: get the lowest distance of q and any Node of Qi
    #
    # Input: point p to get the distances from, Cover set Qi
    #
    # Output: the lowest distance of q and any Node of Qi
    #
    def getDist(self, p, Qi):
        return min([self.distance(p, q.data) for q in Qi])


    #
    #Overview:get the argument that has the minimum distance
    #
    #Input: Input node p, Cover set Q
    #Output: minimum distance Node in Q to p
    #
    def arg_min(self, p, Q):
        return min(Q, key = lambda q: self.distance(p, q.data))

    #
    #Overview:print to the terminal the dot representation
    #  of the stuff
    #
    #Input: None
    #Output: Dotty representation of the cover tree printed to the screen
    #
    def printDotty(self):
        print "digraph {"
        self.printHash = {}
        self.printTree([self.root], self.maxlevel)

        for i in self.printHash.keys():
            print i
        print "}"


    #
    #Overview:recursively print the tree (helper function for printDotty)
    #
    #Input: T ???
    #Output: Dotty representation of the cover tree printed to the screen
    #
    def printTree(self, T, level):
        if(level < self.minlevel):
            return

        thechildren = []
        for p in T:
            childs = deepcopy(p.getChildren(level))

            for i in p.getChildren(level):
                if(level < 0):
                    mylev = "_" + str(abs(level))
                else:
                    mylev = str(level)

                self.printHash["\"lev:" +str(level) + " " + str(p.data) + "\"->\"lev:" + str(level-1) + " " + str(i.data) + "\""] = 0

            thechildren.extend(childs)
        
        self.printTree(thechildren, level-1)

