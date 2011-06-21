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
        Q, d_p_Q = self.getChildren(p, Qi, i)

        if(d_p_Q == 0.0):
            print "already an element", p
            return True

        if(d_p_Q > self.base**i):
            return False
        else:
            #construct Q_i-1
            Qi_next = [q for q in Q if self.distance(p, q.data) <= self.base**i]
            d_p_Qi,_ = self.getDist(p, Qi)
            
            myIns = self.insert_rec(p, Qi_next, i-1)
            if(not myIns and d_p_Qi <= self.base**i):
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
            Q, d_p_Q = self.getChildren(p, Qcurr, l)

            #create the next set
            Qcurr = [q for q in Q
                     if self.distance(p, q.data) <= d_p_Q + self.base**l]

        #find the minimum
        return self.arg_min(p, Qcurr)

    #
    #Overview:find an element given a particular level, recursive
    #
    #Input: Node to find p, Cover set Qi, current integer level i
    #Output: the Node node and the level
    #
    # TODO: it's strange to return the Node found, perhaps it should
    # return a boolean and the level
    def find_rec(self, p, Qi, i):
        #get the children of the current level
        Q, _ = self.getChildren(p, Qi, i)
        Qi_next = [q for q in Q if self.distance(p.data, q.data) <= self.base**i]
        d_p_Qi, elt = self.getDist(p, Qi)

        if(i < self.minlevel):
            print "Elt. not found"
            return None
        elif(d_p_Qi == 0):
            return elt, i
        else:
            return self.find_rec(p, Qi_next, i-1)


    #
    #Overview:get the children of the current level
    #
    #Input: Node p to get the children of, Cover set Qi, current integer level i
    #Output: the children of Node p
    #
    def getChildren(self, p, Qi, level):
        Q = sum([j.getChildren(level) for j in Qi], [])
        d_p_Q = min([self.distance(p, q.data) for q in Q])
        return Q, d_p_Q

    #
    #Overview:get the distance at the current level
    #
    #Input: point p to get the distances from, Cover set Qi, list of Nodes to exclude
    #Output: the distances to all nodes below and the cover set
    #
    def getDist(self, p, Qi):
        # TODO perhaps can be sped-up by splitting defining another function that returns only the distance and use min instead of that loop
        #get all the children
        d_p_Q = sys.float_info.max
        retQ = None
        for q in Qi:
            d = self.distance(p, q.data)
            if(d <= d_p_Q):
                d_p_Q = d
                retQ = q 
        return [d_p_Q,retQ]

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

