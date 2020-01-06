import sys
import copy
import operator
import pandas as pd
import argparse

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_colwidth', 8)


def return_index(lst, val):
    index = []
    for i in range(len(lst)):
        if val == lst[i]:
            index.append(i)
    return(index)        

"""Generate parenthesized contents in string as pairs (level, contents)."""
def constituency_to_conll(string,sen_len):
    stack = []
    stack_wd = []
    i = 0
    j = sen_len
    count = 0
    count_wd = 1
    sent_dic = {}
    re_index_const = []
    for wd_tmp in string:
        wd = wd_tmp.strip()
        if wd == '(':
            stack.append(i)
            re_index_const.append(' (')
        elif wd == ')' and len(stack_wd) > 1:

            re_index_const.append(')')


            wd2 = stack_wd[-2]
            wd1 = stack_wd[-1]

            if(re.search('[0-9]',wd2)):
                sent_dic[j]=wd1+'\t'+wd2
                j += 1
                wd1 = stack_wd.pop()


            #if only 2 items are there pop it empty the stack
            elif(len(stack_wd) == 2):
                wd1 = stack_wd.pop()
                wd2 = stack_wd.pop()
                sent_dic[j]=wd1+'\t'+wd2
                j += 1

            else:
                #for words (terminals)
                wd1 = stack_wd.pop()
                wd2 = stack_wd.pop()
                wd3 = stack_wd[-1]
                if(re.search('[0-9]',wd1)):
                    sent_dic[j]=wd2+'\t'+wd3
                    j += 1

                else:
                    sent_dic[count_wd]=wd2+'\t'+wd3
                    count_wd += 1
        else:
            if(re.match('NP|VP|PP|ADJP|ADVP|SBAR|ROOT|S',wd)):
                    stack_wd.append(wd+str(count))
                    re_index_const.append(wd+str(count))
                    count += 1
            else:
                stack_wd.append(wd)
                re_index_const.append(' '+wd)
        i += 1
    #return sent_dic
    return ''.join(re_index_const)


def add_children_info(lst, level,children,array):
    lst = []
    for each in children:
        val = []
        val.append(str(int(each)+1))
        val.append(level)
        array.append(val)



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


def calculate_top_value(tree):


    A_id = tree[0].tolist()
    H_id = tree[6].tolist()

    head_info_lst = []
    top_lst = []

    for l in H_id:
        head_info_lst.append(str(l))

    for l in A_id:
        top_lst.append(str(l))


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




def calculate_bottom_value(tree,top_value):


    A_id = tree[0].tolist()
    H_id = tree[6].tolist()

    T_V = top_value


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

def calculate_multi_bottom_value(tree,top_value):


    #T_label = top_value(head_info_lst,top_lst)
    #B_level  = calculate_bottom_level(A_id,H_id,T_label)

    T_level_org = calculate_top_value(tree)
    B_level_org = calculate_bottom_value(tree, T_level_org)

    A_id_org = tree[0].tolist()
    H_id_org = tree[6].tolist()

    A_id = tree[0].tolist()
    H_id = tree[6].tolist()



    multi_b_lev = {}
    multi_b_lev1 = {}

    tmp_A_id = A_id.copy()
    tmp_H_id = H_id.copy()

    count = 1
    map1 = {}
    while len(tmp_A_id) > 0:

        new_A_id = tmp_A_id.copy()
        new_H_id = tmp_H_id.copy()

        head_info_lst = []

        top_lst = []

        for l in new_H_id:
            head_info_lst.append(str(l))

        for l in new_A_id:
            top_lst.append(str(l))

        #T_label = top_value(head_info_lst,top_lst)
        #B_level  = calculate_bottom_level(new_A_id,new_H_id,T_label)

        # add head_info_lst, new_A_id to tree data frame


        new_tree = pd.DataFrame()
        tmp_filler = ['_' for x in range(0,len(new_A_id))]

        for i in range(0,10):
            if(i == 0):
                new_tree.insert(loc=i, column=i, value=new_A_id)
            elif(i == 6):
                new_tree.insert(loc=i, column=i, value=new_H_id)
            else:
                new_tree.insert(loc=i, column=i, value=tmp_filler)




        T_level = calculate_top_value(new_tree)
        B_level = calculate_bottom_value(new_tree, T_level)


        index_max = max(range(len(T_level)), key=T_level.__getitem__)




        for i in  range(0,len(A_id_org)):

            key = A_id_org[i]
            if key in multi_b_lev:
                multi_b_lev[key] = str(multi_b_lev[key])+','+str(B_level[i])
                multi_b_lev1[key].append(B_level[i])
            else:
                multi_b_lev[key] = str(B_level[i])
                multi_b_lev1[key] = [B_level[i]]

        del new_A_id[index_max]
        del new_H_id[index_max]

        del A_id_org[index_max]
        del H_id_org[index_max]

        map1 = {}
        re_new_A_id = []
        for k in range(1,len(new_A_id)+1):
            re_new_A_id.append(k)

        i = 1
        for k in new_A_id:
            map1[k] = i
            i += 1


        re_new_H_id = []
        for k in new_H_id:
            if k != 0:
                re_new_H_id.append(map1[k])
            else:
                re_new_H_id.append(0)


        tmp_A_id = re_new_A_id.copy()
        tmp_H_id = re_new_H_id.copy()

        count += 1



    multi_b_lev2 = {}
    for key in multi_b_lev1:

        if B_level_org[key-1] == 1:
            tmp_l = list(set(multi_b_lev1[key]))
            multi_b_lev2[key] = tmp_l

        else:

            tmp_l = list(set(multi_b_lev1[key]))
            del tmp_l[0]
            multi_b_lev2[key] = tmp_l


    return multi_b_lev2



if __name__ == "__main__":


    parser = argparse.ArgumentParser(prog="CONLL Tools.", description="A set of tools to do basic operation on CONLL Parse Tree")


    parser.add_argument('--value',  choices=['top','bottom'], help='Values to calculate [top|bottom]')
    parser.add_argument('--tree_transform', choices=['obl','yaxi_wo'], help='Type of tree  transformation [case|yaxi_wo]')
    parser.add_argument('--input-file', dest='infile', help='Input conll File')
    parser.add_argument('--output-file', dest='outfile', default='out.conll', help='Output File')




    args = parser.parse_args()
    #print(args)

    if(args.value):


        tree = pd.read_csv(args.infile,sep='\t',header=None)
        if(args.value == 'top'):
            lst = calculate_top_value(tree)
            print(lst)
        elif(args.value == 'bottom'):
            t_v = calculate_top_value(tree)
            dic_b_val  = calculate_multi_bottom_value(tree,t_v)
            list_b_val = []
            for keys in sorted(dic_b_val):
               list_b_val.append(dic_b_val[keys])

            tree.insert(loc=10, column=10, value=list_b_val)
            tree.to_csv('out',sep='\t',header=False,index=False)


    if(args.tree_transform):
        print('yes')




'''
print(new_A_id)
print(new_H_id)
print('------')
print(re_new_A_id)
print(re_new_H_id)
'''
'''

#print(T_label)
print(B_level)

print('###########################################')

tmp_A_id = re_new_A_id.copy()
tmp_H_id = re_new_H_id.copy()

count += 1

'''
'''

#print(calculate_bottom_level(re_new_A_id,re_new_H_id,new_T_V))
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


'''
with open(sys.argv[1]) as f:
    sents = f.readlines()



no_wds = 1



'''

'''
for sent in sents:

    for wd in sent.split():
        if(re.search('\)',wd)):
            no_wds += 1

    sent1 = re.sub('\(',' ( ',sent)
    sent2 = re.sub('\)',' ) ',sent1)
    re_index_const = parenthetic_contents(sent2.split(),no_wds)
    print(re_index_const)

    for key in sent_dic:
        print(key,sent_dic[key])

    for key in sorted (sent_dic):
        print(key,'\t',sent_dic[key])


    #for creating conll type format

    hd = {}
    for key in sorted (sent_dic):
        idx = key
        all_val = sent_dic[key]
        pos_val = sent_dic[key].split('\t')[0].strip()
        head_val = sent_dic[key].split('\t')[1].strip()
        hd[pos_val] = idx

    for key in sorted (sent_dic):
        
        idx = key
        all_val = sent_dic[key]
        pos_val = sent_dic[key].split('\t')[0]
        head_val = sent_dic[key].split('\t')[1].strip()

        if(head_val != 'ROOT0'):
            print(idx,'\t',pos_val,'\t_','\t_','\t_','\t_\t',hd[head_val],'\tmother','\t',str(hd[head_val])+':mother','\t_')
        else:
            print(idx,'\t',pos_val,'\t_','\t_','\t_','\t_\t0','\tmother','\t','0:mother','\t_')

'''



'''
#T_label =  top_lst #coming from roja prog

A_id = []
H_id = []
R_id = []
Wds = []

data = pd.read_csv(sys.argv[1],sep='\t',header=None)

A_id = data[0].tolist()
Wds = data[1].tolist()
H_id = data[6].tolist()
R_id = data[7].tolist()

#B_level = calculate_bottom_level(A_id,H_id,T_label)

#new_tree = tree_tran(data,[A_id,H_id,R_id,Wds],'obl_replacement')
new_data = tree_tran(data,[A_id,H_id,R_id,Wds],'yaxi_wo')
pdf = new_data[['new_id',1,2,3,4,5,'new_hid','new_rid','new_comb_rel',9]]
pdf.to_csv('out',sep='\t',header=False,index=False)



'''

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
    
    
    
'''





