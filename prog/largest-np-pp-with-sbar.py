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
    sbar_dic = {}
    sbar_dic_id = {}
    s_dic = {}
    s_dic_id = {}
    vp_dic = {}
    vp_dic_id = {}

    for i in range(0, len(w_id)):
        if(w_id[i].strip() != '_'):
            found_sbar = 0
            head_list = get_ancestor1(A_id, H_id, i)
            pos_list = []

            #for finding 's'(sentences) inside the main S1
            for j in range(len(head_list), 0, -1):
            #for j in range(0,len(head_list)):
                c_pos = pos_id[head_list[j-1] - 1].strip()
                pos_list.append(c_pos)
                if re.search(r'S', c_pos) and c_pos != 'S1':
                    found_sbar = 1
                    if (c_pos in s_dic):
                        s_dic[c_pos] = s_dic[c_pos] + ' ' + w_id[i].strip()
                        s_dic_id[c_pos] = s_dic_id[c_pos] + ',' + str(i)
                    else:
                        s_dic[c_pos] = w_id[i].strip()
                        s_dic_id[c_pos] = str(head_list[j-1]) + ',' + str(i)
                    break

            #for finding 'sbar'(sbar sentences) inside the main S1
            for j in range(len(head_list), 0, -1):
            #for j in range(0,len(head_list)):
                c_pos = pos_id[head_list[j-1] - 1].strip()
                pos_list.append(c_pos)
                if re.search(r'SBAR', c_pos) and c_pos != 'S1':
                    found_sbar = 1
                    if (c_pos in sbar_dic):
                        sbar_dic[c_pos] = sbar_dic[c_pos] + ' ' + w_id[i].strip()
                        sbar_dic_id[c_pos] = sbar_dic_id[c_pos] + ',' + str(i)
                    else:
                        sbar_dic[c_pos] = w_id[i].strip()
                        sbar_dic_id[c_pos] = str(head_list[j-1]) + ',' + str(i)
                    break


            #for finding 'VP' and 'VB*' grouping.
            # to check if the next vp phrase is present then take the larger 
            for j in range(0,len(head_list)):
                c_pos = pos_id[head_list[j-1] - 1].strip()
                c_pos_next = pos_id[head_list[j] - 1].strip()

                pos_list.append(c_pos)
                if re.search(r'VP', c_pos) and re.search(r'VB|MD|RB', pos_id[i]) and re.search(r'VP', c_pos_next) == None :
                    found_sbar = 1
                    if (c_pos in vp_dic):
                        vp_dic[c_pos] = vp_dic[c_pos] + ' ' + w_id[i].strip()
                        vp_dic_id[c_pos] = vp_dic_id[c_pos] + ',' + str(i)
                    else:
                        vp_dic[c_pos] = w_id[i].strip()
                        vp_dic_id[c_pos] = str(head_list[j-1]) + ',' + str(i)
                    break



            if(found_sbar == 0):
                for j in range(len(head_list),0, -1):
                    c_pos = pos_id[head_list[j-1] - 1]
                    pos_list.append(c_pos)
                    if re.search(r'NP|PP', c_pos):
                        if(c_pos in np_pp_dic):
                            np_pp_dic[c_pos] = np_pp_dic[c_pos] + ' '+w_id[i].strip()
                        else:
                            np_pp_dic[c_pos] = w_id[i].strip()
                        break

    if(len(sbar_dic_id) > 0):
       for key in sbar_dic_id:
           ids = sbar_dic_id[key].split(',')[1:]
           sbar_id = sbar_dic_id[key].split(',')[0]

           #print(key, sbar_dic[key])

           for i in range(0, len(ids)):
               if (w_id[int(ids[i])].strip() != '_'):
                   head_list = get_ancestor1(A_id, H_id, int(ids[i]))
                   for j in range(len(head_list), 0, -1):
                       c_pos = pos_id[head_list[j - 1] - 1]
                       if re.search(r'NP|PP', c_pos) and head_list[j-1] < int(sbar_id):
                           if (c_pos in np_pp_dic):
                               np_pp_dic[c_pos] = np_pp_dic[c_pos] + ' ' + w_id[int(ids[i])].strip()
                           else:
                               np_pp_dic[c_pos] = w_id[int(ids[i])].strip()
                           break

    if(len(s_dic_id) > 0):
       for key in s_dic_id:
           ids = s_dic_id[key].split(',')[1:]
           s_id = s_dic_id[key].split(',')[0]

           #print(key, s_dic[key])

           for i in range(0, len(ids)):
               if (w_id[int(ids[i])].strip() != '_'):
                   head_list = get_ancestor1(A_id, H_id, int(ids[i]))
                   for j in range(len(head_list), 0, -1):
                       c_pos = pos_id[head_list[j - 1] - 1]
                       if re.search(r'NP|PP', c_pos) and head_list[j-1] < int(s_id):
                           if (c_pos in np_pp_dic):
                               np_pp_dic[c_pos] = np_pp_dic[c_pos] + ' ' + w_id[int(ids[i])].strip()
                           else:
                               np_pp_dic[c_pos] = w_id[int(ids[i])].strip()
                           break

    total_chunks = {}
    for key in sbar_dic:
        num = re.match(r'[^\d]+(\d+)',key)[1]
        total_chunks[num] = key.strip()+':'+sbar_dic[key]
    for key in s_dic:
        num = re.match(r'[^\d]+(\d+)',key)[1]
        total_chunks[num] = key.strip()+':'+s_dic[key]
    for key in np_pp_dic:
        num = re.match(r'[^\d]+(\d+)',key)[1]
        total_chunks[num] = key.strip()+':'+np_pp_dic[key]
    for key in vp_dic:
        num = re.match(r'[^\d]+(\d+)',key)[1]
        total_chunks[num] = key.strip()+'(Verbal_part_only)'+':'+vp_dic[key]






    return (total_chunks)




if __name__ == "__main__":

    const_tree = pd.read_csv(sys.argv[1], sep='\t', header=None)
    total_chunks = largest_np_pp(const_tree)
    int_total_chunks = {int(k) : v for k, v in total_chunks.items()}
    for key in sorted(int_total_chunks):
        print(key,int_total_chunks[key])
