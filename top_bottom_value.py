import sys
import copy
import operator
from all_indices import return_index

import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_colwidth', 8)

import sys

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



#For top level info    
array = []
level  = 0

def add_children_info(lst, level):
    lst = []
    for each in children:
        val = []
        val.append(str(int(each)+1))
        val.append(level)
        array.append(val)

root = return_index(head_info_lst, '0')

val = []
val.append(str(int(root[0]+1)))
val.append(level+1)
array.append(val)
index = 0

for i in range(index, len(f)-1):
    head = array[i][0]
    level = array[i][1]
    level += 1
    children = return_index(head_info_lst, head)
    if children != None:
        add_children_info(children, level)

array.sort()
#print('Top level info, id and level', array)


for each in array:
    index = int(each[0])-1
    level = each[1]
    top_lst[index] = level
#print('Only top level info', top_lst)
########################### Coding for top level ended.

#Bottom level info
max_val = max(top_lst)

#To get id info::
main_id_lst = []
for i in range(0, len(f)-1):
    lst = f[i].strip().split('\t')
    main_id_lst.append(lst[0])


def remove_list(list1, list2):
  for  l in list2:
    while l in list1:
        list1.remove(l)
  return list1


def find_id_with_max_top_level(lst1, lst2):
    new_lst = []
    for each in lst1:
        new_lst.append(lst2[int(each)-1])
    max_val = max(new_lst)
    for i in range(0, len(lst2)):
        if lst2[i] == max_val:
            return i

def get_ancestor_list(index):
    lst = []
    while index != 0:
        mother = head_info_lst[index-1]
        lst.append(mother)
        index = int(mother)
    return lst

bottom_list = []
bottom_level_info = main_id_lst
max_ind = 0  


#To get 1st level info of Bottom to top approach
for i in range(0, len(f)-1):
    lst = f[i].strip().split('\t')
    if lst[0] not in head_info_lst:
        bottom_list.append(lst[0])
        bottom_level_info[int(lst[0])-1] = 1


#print(bottom_level_info)
main_id_lst = remove_list(main_id_lst, bottom_list)
max_ind = find_id_with_max_top_level(bottom_list, top_lst)

#print(max_ind)

#while max_ind != 0:
    #To get ancestor info highest bottom 
out = get_ancestor_list(max_ind)

    #To assign level info for ancesstors
for each in out :
    for i in range(0, len(main_id_lst)):
        if each == main_id_lst[i]:
             main_id_lst[i] = max_val-1

max_ind = find_id_with_max_top_level(bottom_list, top_lst)


#print(len(main_id_lst),main_id_lst)
#print(len(main_id_lst),main_id_lst)


#print(head_info_lst)
#print(top_lst)
#print(bottom_list)
#print(len(bottom_list),bottom_list)



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


def tree_tran(tree,T,transformation):

    if(transformation == 'obl_replacement'):


        A_id = T[0]
        H_id = T[1]
        R_id = T[2]
        Wds = T[3]

        A_id_org = A_id.copy()
        H_id_org = H_id.copy()
        R_id_org = R_id.copy()
        Wds_org = Wds.copy()


        obl_markers = ['nmod','obl']
        pp = ['mark','case']

        rem_node = []
        for l in obl_markers:
            l = return_index(R_id,l)
            for k in l:
                rem_node.append(k)

        count = 0
        for n in rem_node:
            for i,j,k,l in zip(A_id_org,H_id_org,R_id_org,Wds):
                if(n+1 == j):
                    for m in pp:
                        if (k == m):
                            new_rel = Wds[i-(count+1)]

                            if(count > 0):
                                R_id[n] = R_id[n]+'_'+new_rel
                            else:
                                R_id[n] = new_rel


                            del A_id[i-(count+1)]
                            del H_id[i-(count+1)]
                            del R_id[i-(count+1)]
                            del Wds[i-(count+1)]
                            count += 1

        #reindex the new  tree

        new_A_id = []
        for i in range(1,len(A_id)+1):
            new_A_id.append(i)
        map1 = {}
        for i in range(len(A_id)):
            if(i+1 != A_id[i]):
                map1[A_id[i]] = i+1

        for i in H_id:
            if i in  map1:
                index = H_id.index(i)
                H_id[index] = map1[i]

        return [new_A_id,H_id,R_id,Wds]

    elif(transformation == 'yaxi_wo'):

        #remove yaxi and wo node in Hindi
        # remove 'if' node in English

        #################
        #pandas example:
        # match either 'Tokyo' or 'Paris'
        #result = sr.str.match(pat='(Tokyo)|(Paris)')
        #df = df[~df['your column'].isin(['list of strings'])]
        #new_data = data[~data[1].isin(['yaxi','wo','and'])]
        #yaxi_list = data[1].str.match('yaxi')
        #data1 = data.drop([0],axis=0)
        #data1.reset_index()
        # pd.concat([pd.DataFrame([i], columns=['A']) for i in range(5)],
        #df.insert(loc=idx, column='A', value=new_col)
        #################


        k= data[1].isin(['yaxi','wo','and'])
        occur  = k[k].index

        new_rid = data[7].tolist()
        for l in occur:
            a_id = data[0].tolist()
            h_id = data[6].tolist()
            al = get_ancestor1(a_id,h_id,int(l))

            for k in al:
                if(k != 0):
                    pos = data.loc[k-1][3]
                    if(pos == 'VERB'):
                        new_rid[k-1] = 'and'

            data.insert(loc=7, column='new_rid', value=new_rid)
            head = data.loc[l][6]
            head_pos = data.loc[head-1][3]
            if(head_pos == 'VERB'):
                data1 = data.drop([l],axis=0)



        tmp_df = pd.DataFrame([['x','vAkya_sambanXa',0,0,0,0,0,'root','0:root','_']])
        new_data = tmp_df.append(data1,ignore_index=False)

        new_id = [i for i in range(1,len(new_data[0])+1)]
        new_data.insert(loc=1, column='new_id', value=new_id)
        new_data = new_data.rename(columns ={0:'old_id',6:'old_hid'})


        o_n_map = {}
        i = 0
        for l in new_data['old_id'].tolist():
            o_n_map[l] = new_data['new_id'].tolist()[i]
            i += 1

        new_h_id = new_data['old_hid'].tolist()
        for i in range(0,len(new_h_id)):
            if new_h_id[i] in o_n_map:
                new_h_id[i] = o_n_map[new_h_id[i]]

        new_rid = new_data['new_rid'].tolist()
        for i in range(0,len(new_rid)):
            if(new_rid[i] == 'and'):
                new_h_id[i] = 1


        new_data.insert(loc=7, column='new_hid', value=new_h_id)

        new_data = new_data.fillna('root')
        new_rid = new_data['new_rid'].tolist()
        new_hid = new_data['new_hid'].tolist()
        new_comb_rel = []
        for i,j in zip(new_h_id,new_rid):
            new_comb_rel.append(str(i)+':'+j)

        new_data.insert(loc=7, column='new_comb_rel', value=new_comb_rel)
        return new_data



T_label =  top_lst #coming from roja prog

A_id = []
H_id = []
R_id = []
Wds = []

data = pd.read_csv(sys.argv[1],sep='\t',header=None)

A_id = data[0].tolist()
Wds = data[1].tolist()
H_id = data[6].tolist()
R_id = data[7].tolist()

B_level = calculate_bottom_level(A_id,H_id,T_label)
print(B_level)

#new_tree = tree_tran(data,[A_id,H_id,R_id,Wds],'obl_replacement')
#new_data = tree_tran(data,[A_id,H_id,R_id,Wds],'yaxi_wo')
#pdf = new_data[['new_id',1,2,3,4,5,'new_hid','new_rid','new_comb_rel',9]]
#pdf.to_csv('out',sep='\t',header=False,index=False)


