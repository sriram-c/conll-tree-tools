import sys
import copy
import operator
import pandas as pd
import argparse
import re

'''
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_colwidth', 8)

'''

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


def largest_np_pp(const_tree):

    A_id = const_tree[0].tolist()

    w_id = const_tree[1].tolist()

    pos_id = const_tree[2].tolist()
    H_id = const_tree[7].tolist()

    #w_id = sen.split()

    np_pp_dic = {}
    for i in range(0, len(w_id)):
        if(w_id[i].strip() != '_'):
            head_list = get_ancestor1(A_id, H_id, i)

            for j in range(len(head_list),0, -1):
                c_pos = pos_id[head_list[j-1] - 1]
                if re.search(r'NP|PP', c_pos):
                    if(c_pos in np_pp_dic):
                        np_pp_dic[c_pos] = np_pp_dic[c_pos] + ' '+w_id[i].strip()
                    else:
                        np_pp_dic[c_pos] = w_id[i].strip()
                    break


    return np_pp_dic




if __name__ == "__main__":

    const_tree = pd.read_csv(sys.argv[1], sep='\t', header=None)

    '''
    with open(sys.argv[2],'r') as f:
        sen = f.readlines()

    np_pp = largest_np_pp(const_tree, sen[0].strip())
    '''
    np_pp = largest_np_pp(const_tree)
    for key in np_pp:
        print(key,np_pp[key])

