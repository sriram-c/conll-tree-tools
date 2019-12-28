import sys
import copy
import operator
from all_indices import return_index

import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_colwidth', 8)

import sys


def add_children_info(lst, level,children,array):
    lst = []
    for each in children:
        val = []
        val.append(str(int(each)+1))
        val.append(level)
        array.append(val)





#########################################
#sriram work starts
#########################################
# Calculating node values from Bottom level.
#########################################

def get_ancestor1(A_id,H_id,index):

    lst = []
    mother = H_id[index]
    lst.append(mother)

    while mother != 0:
        if(mother in A_id):
            l = A_id.index(mother)
            mother = H_id[l]
            lst.append(mother)
        else:
            return  lst
    return lst



def remove_list1(list1, list2):
    tmp = list1.copy()
    for  l in list2:
      while l in tmp:
          tmp.remove(l)
    return tmp




def calculate_bottom_level(A_id,H_id,T_V):

    A_id_org = A_id.copy()
    H_id_org = H_id.copy()

    B_level = []
    for l in range(0,len(A_id_org)):
        B_level.append(0)

    tmp = remove_list1(A_id,H_id)
    for l in tmp:
        B_level[l-1] = 1

    new_A_id = remove_list1(A_id,tmp)


    m = 2
    while len(new_A_id) != 0:

        new_H_id = []
        for l in new_A_id:
            new_H_id.append(H_id[l-1])

        new_T_V = []
        for l in new_A_id:
            new_T_V.append(T_V[l-1])

        index_max = max(range(len(new_T_V)), key=new_T_V.__getitem__)

        B_level[new_A_id[index_max]-1] = m
        al = get_ancestor1(new_A_id, new_H_id,index_max)


        if(len(al) == 1):
            if(B_level[al[0]-1] != 0):
                del new_A_id[index_max]

        k = m+1

        for j in al:
            if j in new_A_id:
                B_level[j-1] = k
                new_A_id.remove(j)
                k += 1

    return B_level


def top_value(head_info_lst,top_lst):

    #For top level info
    array = []
    level  = 0

    root = return_index(head_info_lst, '0')

    val = []
    val.append(str(int(root[0]+1)))
    val.append(level+1)
    array.append(val)
    index = 0

    for i in range(index, len(head_info_lst)-1):
        head = array[i][0]
        level = array[i][1]
        level += 1
        children = return_index(head_info_lst, head)
        if children != None:
            add_children_info(children, level,children,array)

    array.sort()
    #print('Top level info, id and level', array)


    for each in array:
        index = int(each[0])-1
        level = each[1]
        top_lst[index] = level


    return top_lst



'''
f = open(sys.argv[1], 'r').readlines()

#Declarations:
head_info_lst = []
top_lst = []
###########################################
for line in f:
    if line != '\n':
        lst = line.strip().split('\t')
        head_info_lst.append(lst[6])
        top_lst.append(lst[0])

###########################################

print(head_info_lst)
print(top_lst)

'''

A_id = []
H_id = []
R_id = []
Wds = []

data = pd.read_csv(sys.argv[1],sep='\t',header=None)

A_id = data[0].tolist()
Wds = data[1].tolist()
H_id = data[6].tolist()
R_id = data[7].tolist()


head_info_lst = []
top_lst = []

for l in H_id:
    head_info_lst.append(str(l))

for l in A_id:
    top_lst.append(str(l))

T_label = top_value(head_info_lst,top_lst)
B_level  = calculate_bottom_level(A_id,H_id,T_label)

print(A_id)
print(H_id)


print('###########################################')

tmp_A_id = A_id.copy()
tmp_H_id = H_id.copy()

count = 1
while len(tmp_A_id) > 0:

    print(count)
    new_A_id = tmp_A_id.copy()
    new_H_id = tmp_H_id.copy()

    head_info_lst = []

    top_lst = []

    for l in new_H_id:
        head_info_lst.append(str(l))

    for l in new_A_id:
        top_lst.append(str(l))

    T_label = top_value(head_info_lst,top_lst)
    B_level  = calculate_bottom_level(new_A_id,new_H_id,T_label)

    index_max = max(range(len(T_label)), key=T_label.__getitem__)



    del new_A_id[index_max]
    del new_H_id[index_max]

    map = {}
    re_new_A_id = []
    for k in range(1,len(new_A_id)+1):
        re_new_A_id.append(k)

    i = 1
    for k in new_A_id:
        map[k] = i
        i += 1


    re_new_H_id = []
    for k in new_H_id:
        if k != 0:
            re_new_H_id.append(map[k])
        else:
            re_new_H_id.append(0)



    '''
    print(new_A_id)
    print(new_H_id)
    print('------')
    print(re_new_A_id)
    print(re_new_H_id)
    '''
    #print(T_label)
    print(B_level)

    print('###########################################')

    tmp_A_id = re_new_A_id.copy()
    tmp_H_id = re_new_H_id.copy()

    count += 1

#print(calculate_bottom_level(re_new_A_id,re_new_H_id,new_T_V))
'''

index_max = max(range(len(T_label)), key=T_label.__getitem__)

tmp = A_id.remove(index_max)
print(tmp)
B_level,index_max  = calculate_bottom_level(tmp,H_id,T_label)
print(B_level)

#new_tree = tree_tran(data,[A_id,H_id,R_id,Wds],'obl_replacement')
#new_data = tree_tran(data,[A_id,H_id,R_id,Wds],'yaxi_wo')
#pdf = new_data[['new_id',1,2,3,4,5,'new_hid','new_rid','new_comb_rel',9]]
#pdf.to_csv('out',sep='\t',header=False,index=False)

'''

