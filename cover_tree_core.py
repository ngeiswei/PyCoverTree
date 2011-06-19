#File: cover_tree_core.py
#Author: Thomas Kollar
#email: tkollar@csail.mit.edu
#Date: 05/04/07
#All Rights Reserved. Copyright Thomas Kollar 2007
#
#
#
#  This is a class for the cover tree nearest
#  neighbor algorithm.  For more information
#  please refer to the technical report entitled
#  "Fast Nearest Neighbors" by Thomas Kollar
#  or to "Cover Trees for Nearest Neighbor" by
#  John Langford, Sham Kakade and Alina Beygelzimer
#  
#  If you use this code in your research, kindly refer to the 
#  technical report.

from scipy import *
from copy import *
from random import *
import sys

class cover_tree_core:

    #
    #Overview: initalization method
    #
    #Input: root vector, maxlevel, minlevel
    #  Here initpt is a Node, maxlevel is the largest number that we care
    #  about (e.g. 2^(maxlevel) should be our maximum number), just as 2^(minlevel)
    #  should be the minimum distance between Nodes.
    #Output:
    #
    def __init__(self, initpt, maxlevel, minlevel=None):
        self.root = initpt
        self.maxLevel = maxlevel
        if(not minlevel == None):
            self.minlevel = minlevel
        else:
            self.minlevel = -10
            
    #
    #Overview: insert an element p into the tree
    #
    #Input: Node p
    #Output: None
    #
    def insert(self, p):
        return self.insert_rec(p, [self.root], self.maxLevel)

    #
    #Overview: get the nearest neighbor of an element
    #
    #Input: Node p
    #Output: Nearest Node with respect to the distance metric d(),
    #          defined in Node
    #
    def nearest_neighbor(self, p):
        return self.nearest_neighbor_iter(self.root, p)

    #
    #Overview: find an element in the tree
    #
    #Input: Node p
    #Output: The Node if it exists as well as the level on
    #          which it was found
    #
    def find(self, p):
        return self.find_rec(p, [self.root], self.maxLevel)


    #
    #Overview:insert an element p in to the cover tree
    #             based on the current level, recursive
    #
    #Input: Node p, Cover Qi(list of nodes?), integer level i
    #Output: boolean, Whether the node was inserted or not
    #
    def insert_rec(self, p, Qi, i):
        #get the children of the current level
        Q, d_p_Q = self.getChildren(p, Qi, i)

        if(d_p_Q == 0.0):
            print "already an element", p
            return True

        if(d_p_Q > 2**i):
            return True
        else:
            #construct Q_i-1
            Qi_next = []
            for q in Q:
                if(p.d(q) <= 2**i): #and q not in Qi_next):
                    Qi_next.append(q)
            d_p_Qi,elt = self.getDist(p, Qi)
            
            myIns = self.insert_rec(p, Qi_next, i-1)
            if(myIns and  d_p_Qi <= 2**i):
                possParents = []
                for q in Qi:
                    if(p.d(q) <= 2**i):
                        possParents.append(q)
                        
                myInst = randint(0, len(possParents)-1)
                possParents[myInst].addChild(p, i)

                return False
            else:
                return myIns
            
    #
    #Overview:get the nearest neighbor, iterative
    #
    #Input: root node T, query Node p
    #Output: the nearest Node 
    #
    def nearest_neighbor_iter(self, T, p):
        Qcurr = [self.root]
        done = False

        level = self.maxLevel
        Q = []
        while(not done):

            #get the children of the current Q and
            #the best distance at the same time
            Q, d_p_Q = self.getChildren(p, Qcurr, level)

            #if there are no children to examine, then
            #we are done and we return
            if(level<=self.minlevel):
                done = True
            
            #create the next set
            Qnext = []
            for q in Q:
                if(p.d(q) <= d_p_Q + 2**level):
                    Qnext.append(q)
            Qcurr = Qnext

            #go to the next level
            level = level -1;


        #find the minimum
        return self.arg_min(p, Qcurr)

    #
    #Overview:find an element given a particular level, recursive
    #
    #Input: Node to find p, Cover set Qi, current integer level i
    #Output: the Node node and the level
    #
    def find_rec(self, p, Qi, i):
        #get the children of the current level
        Q, d_p_Q = self.getChildren(p, Qi, i)
        Qi_next = []
        for q in Q:
            if(p.d(q) <= 2**i): #and q not in Qi_next):
                Qi_next.append(q)
        d_p_Qi,elt = self.getDist(p, Qi)

        if(i < self.minlevel):
            print "Elt. not found"
            return None
        elif(d_p_Qi == 0):
            return [elt, i]
        else:
            return self.find_rec(p, Qi_next, i-1)


    #
    #Overview:get the children of the current level
    #
    #Input: Node p to get the children of, Cover set Qi, current integer level i
    #Output: the children of Node p
    #
    def getChildren(self, p, Qi, level):
        Q = []
        
        #get all the children
        d_p_Q = sys.maxint
        
        for j in Qi:
            Q.extend(j.getChildren(level))
            
            #find the minimum distance
            for q in j.getChildren(level):
                if(p.d(q) <= d_p_Q):
                    d_p_Q = p.d(q)

        return Q, d_p_Q

    #
    #Overview:get the distances at the current level
    #
    #Input: Node p to get the distances from, Cover set Qi, list of Nodes to exclude
    #Output: the distances to all nodes below and the cover set
    #
    def getDist(self, p, Qi, excludeList=[]):
        #get all the children
        d_p_Q = sys.maxint
        retQ = None
        for q in Qi:

            if(p.d(q) <= d_p_Q and not q.data in excludeList):
                d_p_Q = p.d(q)
                retQ = q 

        return [d_p_Q,retQ]

    #
    #Overview:get the argument that has the minimum distance
    #
    #Input: Input node p, Cover set Q
    #Output: minimum distance Node in Q to p
    #
    def arg_min(self, p, Q):
        if(len(Q)>0):
            min_q = Q[0]
            
        for q in Q:
            if(p.d(q) <= p.d(min_q)):
                min_q = q

        return min_q 

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
        self.printTree([self.root], self.maxLevel)

        for i in self.printHash.keys():
            print i
        print "}"


    #
    #Overview:recursively print the tree (helper function for printDotty)
    #
    #Input: None
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


#the Node representation of the data
class Node:
    #data is an array of values
    def __init__(self, data=None):
        self.data = array(data)
        self.children = {}
        self.parent = None

    #addChild adds a child to a particular Node and a given level
    def addChild(self, child, level):
        try:
            if(not child in self.children[level]):
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
        if(not self.parent == None):
            #print self.parent.children
            self.parent.children[level+1].remove(self)
            self.parent = None

    #returns the array representation of the Node
    def toarray(self):
        return self.data

    #get the current form of distance between
    #  nodes (can be overridden if necessary)
    def d(self, q):
        x = self.data-q.data
        return sqrt(dot(x, x)) 

    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return str(self.data)
    
