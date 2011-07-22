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

from random import choice
from heapq import nsmallest
from itertools import product
from collections import Counter

# method that returns true iff only one element of the container is True
def unique(container):
    return Counter(container).get(True, 0) == 1


# the Node representation of the data
class Node:
    # data is an array of values
    def __init__(self, data=None):
        self.data = data
        self.children = {}      # dict mapping level and children
        self.parent = None

    # addChild adds a child to a particular Node and a given level i
    def addChild(self, child, i):
        try:
            # in case i is not in self.children yet
            if(child not in self.children[i]):
                self.children[i].append(child)
        except(KeyError):
            self.children[i] = [child]
        child.parent = self

    # getChildren gets the children of a Node at a particular level
    def getChildren(self, level):
        retLst = [self]
        try:
            retLst.extend(self.children[level])
        except(KeyError):
            pass
        
        return retLst

    # like getChildren but does not return the parent
    def getOnlyChildren(self, level):
        try:
            return self.children[level]
        except(KeyError):
            pass
        
        return []


    def removeConnections(self, level):
        if(self.parent != None):
            self.parent.children[level+1].remove(self)
            self.parent = None

    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return str(self.data)

class CoverTree:
    
    #
    # Overview: initalization method
    #
    # Input: distance function, root, maxlevel, minlevel Here root is
    #  a point, maxlevel is the largest number that we care about
    #  (e.g. base^(maxlevel) should be our maximum number), just as
    #  base^(minlevel) should be the minimum distance between Nodes.
    # Output:
    #
    def __init__(self, distance, root = None, maxlevel = 10, base = 2):
        self.distance = distance
        self.root = root
        self.maxlevel = maxlevel
        self.minlevel = maxlevel # the minlevel will adjust automatically
        self.base = base
        # for printDotty
        self.__printHash__ = set()


    #
    # Overview: insert an element p into the tree
    #
    # Input: p
    # Output: nothing
    #
    def insert(self, p):
        if self.root == None:
            self.root = Node(p)
        else:
            self.insert_iter(p)

            
    #
    # Overview: behaves like knn(p, k) and insert(p). This method exists for efficiency reason
    #
    # Input: point p, and k the number of nearest neighbors to return
    #
    # Output: Nearest points with respect to the distance metric
    #          self.distance()
    #
    def knn_insert(self, p, k):
        return self.knn_insert_iter(p, k)
        
    #
    # Overview: get the k-nearest neighbors of an element
    #
    # Input: point p, and k the number of nearest neighbors to return
    #
    # Output: Nearest points with respect to the distance metric
    #          self.distance()
    #
    def knn(self, p, k):
        return self.knn_iter(p, k)

    #
    # Overview: find an element in the tree
    #
    # Input: Node p
    # Output: True if p is found False otherwise
    #
    def find(self, p):
        return self.distance(self.knn(p, 1)[0], p) == 0


    #
    # Overview:insert an element p in to the cover tree
    #
    # Input: point p
    #
    # Output: nothing
    #
    def insert_iter(self, p):
        Qi = [self.root]
        Qi_p_ds = [self.distance(p, self.root.data)]
        i = self.maxlevel
        while True:
            # get the children of the current level
            # and the distance of the all children
            Q, Q_p_ds = self.getChildrenDist(p, Qi, Qi_p_ds, i)
            d_p_Q = min(Q_p_ds)

            if d_p_Q == 0.0:    # already there, no need to insert
                return
            elif d_p_Q > self.base**i: # the found parent should be right
                break
            else: # d_p_Q <= self.base**i, keep iterating

                # find parent
                if min(Qi_p_ds) <= self.base**i:
                    parent = choice([q for q, d in zip(Qi, Qi_p_ds)
                                     if d <= self.base**i])
                    pi = i
                
                # construct Q_i-1
                zn = [(q, d) for q, d in zip(Q, Q_p_ds)
                      if d <= self.base**i]
                Qi = [q for q, _ in zn]
                Qi_p_ds = [d for _, d in zn]
                i -= 1

        # insert p
        parent.addChild(Node(p), pi)
        # update self.minlevel
        self.minlevel = min(self.minlevel, pi-1)

                

    #
    # Overview:get the nearest neighbor, iterative
    #
    # Input: query point p
    #
    # Output: the nearest Node 
    #
    def knn_iter(self, p, k):
        Qi = [self.root]
        Qi_p_ds = [self.distance(p, self.root.data)]
        for i in reversed(xrange(self.minlevel, self.maxlevel + 1)):
            #get the children of the current Q and
            #the best distance at the same time
            Q, Q_p_ds = self.getChildrenDist(p, Qi, Qi_p_ds, i)
            d_p_Q = nsmallest(k, Q_p_ds)[-1]

            #create the next set
            zn = [(q, d) for q, d in zip(Q, Q_p_ds)
                  if d <= d_p_Q + self.base**i]
            Qi = [q for q, _ in zn]
            Qi_p_ds = [d for _, d in zn]

        #find the minimum
        return self.args_min(Qi, Qi_p_ds, k)


    #
    # Overview: query the k-nearest points from p and then insert p in
    # to the cover tree (at no additional cost)
    #
    # Input: point p
    #
    # Output: nothing
    #
    def knn_insert_iter(self, p, k):
        Qi = [self.root]
        Qi_p_ds = [self.distance(p, self.root.data)]
        i = self.maxlevel
        found_parent = False
        already_there = False
        while (not already_there and not found_parent) or i >= self.minlevel:
            # get the children of the current level
            # and the distance of all children
            Q, Q_p_ds = self.getChildrenDist(p, Qi, Qi_p_ds, i)
            d_k = nsmallest(k, Q_p_ds)
            d_p_Q_h = d_k[-1]
            d_p_Q_l = d_k[0]

            if d_p_Q_l == 0.0:    # already there, no need to insert
                already_there = True
            elif not already_there and \
                    not found_parent and \
                    d_p_Q_l > self.base**(i-1):
                found_parent = True
                
            # remember potential parent
            if min(Qi_p_ds) <= self.base**i:
                parent = choice([q for q, d in zip(Qi, Qi_p_ds)
                                 if d <= self.base**i])
                pi = i

            # construct Q_i-1
            zn = [(q, d) for q, d in zip(Q, Q_p_ds)
                  if d <= d_p_Q_h + self.base**i]
            Qi = [q for q, _ in zn]
            Qi_p_ds = [d for _, d in zn]
            i -= 1

        # insert p
        if not already_there and found_parent:
            parent.addChild(Node(p), pi)
            # update self.minlevel
            self.minlevel = min(self.minlevel, pi - 1)
        
        # find the minimum
        return self.args_min(Qi, Qi_p_ds, k)


    #
    # Overview: get the children of cover set Qi at level i and the
    # distances of them with point p
    #
    # Input: point p to compare the distance with Qi's children, and
    # Qi_p_ds the distances of all points in Qi with p
    #
    # Output: the children of Qi and the distances of them with point
    # p
    #
    def getChildrenDist(self, p, Qi, Qi_p_ds, i):
        Q = sum([n.getOnlyChildren(i) for n in Qi], [])
        Q_p_ds = [self.distance(p, q.data) for q in Q]
        return Qi + Q, Qi_p_ds + Q_p_ds



    #
    # Overview:get the argument that has the minimum distance
    #
    # Input: Input cover set Q, distances of all nodes of Q to some point
    # Output: minimum distance points in Q to that point
    #
    def args_min(self, Q, Q_p_ds, k):
        z = nsmallest(k, zip(Q, Q_p_ds), lambda x: x[1])
        return [q.data for q, _ in z]

    #
    # Overview: write to a file the dot representation
    #
    # Input: None
    # Output: 
    #
    def writeDotty(self, outputFile):
        outputFile.write("digraph {\n")
        self.writeDotty_rec(outputFile, [self.root], self.maxlevel)
        outputFile.write("}")


    #
    # Overview:recursively build printHash (helper function for writeDotty)
    #
    # Input: C, i is the level
    #
    def writeDotty_rec(self, outputFile, C, i):
        if(i == self.minlevel):
            return

        children = []
        for p in C:
            childs = p.getChildren(i)

            for q in childs:
                outputFile.write("\"lev:" +str(i) + " "
                                 + str(p.data) + "\"->\"lev:"
                                 + str(i-1) + " "
                                 + str(q.data) + "\"\n")

            children.extend(childs)
        
        self.writeDotty_rec(outputFile, children, i-1)


    # check if the tree satisfies all invariants
    def check_invariants(self):
        return self.check_nesting() and \
            self.check_covering_tree() and \
            self.check_seperation()


    # check if my_invariant is satisfied:
    # C_i denotes the set of nodes at level i
    # for all i, my_invariant(C_i, C_{i-1})
    def check_my_invariant(self, my_invariant):
        C = [self.root]
        for i in reversed(xrange(self.minlevel, self.maxlevel + 1)):        
            C_next = sum([p.getChildren(i) for p in C], [])
            if not my_invariant(C, C_next, i):
                print "At level", i, "the invariant", my_invariant, "is false"
                return False
            C = C_next
        return True
        
    
    # check if the invariant nesting is satisfied:
    # C_i is a subset of C_{i-1}
    def nesting(self, C, C_next, _):
        return set(C) <= set(C_next)

    def check_nesting(self):
        return self.check_my_invariant(self.nesting)
        
    
    # check if the invariant covering tree is satisfied
    # for all p in C_{i-1} there exists a q in C_i so that
    # d(p, q) <= base^i and exactly one such q is a parent of p
    def covering_tree(self, C, C_next, i):
        return all(unique(self.distance(p.data, q.data) <= self.base**i
                          and p in q.getChildren(i)
                          for q in C)
                   for p in C_next)

    def check_covering_tree(self):
        return self.check_my_invariant(self.covering_tree)

    # check if the invariant seperation is satisfied
    # for all p, q in C_i, d(p, q) > base^i
    def seperation(self, C, _, i):
        return all(self.distance(p.data, q.data) > self.base**i
                   for p, q in product(C, C) if p != q)

    def check_seperation(self):
        return self.check_my_invariant(self.seperation)
