#File: quicksort.py
#Author: Thomas Kollar
#email: tkollar@csail.mit.edu
#Date: 11/20/08
#All Rights Reserved. Copyright Thomas Kollar 2007
#
#
#  This is a function that implements the quicksort algorithm

from random import sample

def quicksort(q, cmpfunc=None):
    return quicksort_ind(q, range(len(q)), cmpfunc)

def quicksort_ind(q, index_list, cmpfunc=None):
     less, pivotList, greater, less_index, pivotList_index, greater_index = [],[],[],[],[],[]
     if len(q) <= 1:
         return q, index_list
     
     pivot_val, = sample(range(len(q)),1)
     pivot = q[pivot_val]

     iteration = 0
     pivot_indices = []
     for x in q:
         if(not x == pivot):
             if(not cmpfunc==None):
                 if cmpfunc(x, pivot)<=0:
                     less.append(x)
                     less_index.append(index_list[iteration])
                 elif cmpfunc(x, pivot)>0:
                     greater.append(x)
                     greater_index.append(index_list[iteration])
             else:
                 if cmp(x, pivot)<=0:
                     less.append(x)
                     less_index.append(index_list[iteration])
                 elif cmp(x, pivot)>0:
                     greater.append(x)
                     greater_index.append(index_list[iteration])
         else:
             pivot_indices.append(index_list[iteration])

         iteration += 1

     #need to put in the pivot the number of times it appears
     for index in pivot_indices:
         pivotList.append(pivot)
         pivotList_index.append(index)

     ret_list = []
     ret_list_index = []

     val1, ind1 = quicksort_ind(less,less_index,cmpfunc)
     ret_list.extend(val1)
     ret_list_index.extend(ind1)
     
     
     ret_list.extend(pivotList)
     ret_list_index.extend(pivotList_index)

     val2, ind2 = quicksort_ind(greater, greater_index,cmpfunc)
     ret_list.extend(val2)
     ret_list_index.extend(ind2)
     
     return ret_list, ret_list_index


if(__name__ == "__main__"):
    a = range(10)+[0]
    a.reverse()
    print "start", a
    retval = quicksort(a)
    print "sorted:", retval
