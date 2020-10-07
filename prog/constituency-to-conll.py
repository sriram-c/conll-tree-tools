import re
import sys
def parenthetic_contents(string,sen_len):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    stack_wd = []
    i = 0
    j = sen_len+1
    count = 0
    count_wd = 1
    sent_dic = {}
    for wd_tmp in string:
        wd = wd_tmp.strip()
        if wd == '(':
            stack.append(i)
        elif wd == ')' and len(stack_wd) > 1:

            #print(stack_wd)

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
                    #sent_dic[j]=wd2+'\t'+wd3
                    sent_dic[j]=wd1+'_'+wd2+'\t'+wd3
                    j += 1

                else:
                    sent_dic[count_wd]=wd1+'_'+wd2+'\t'+wd3
                    count_wd += 1
        else:
            #http://www.surdeanu.info/mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html
            if(re.match(r'^NP|WHNP|VP|PP|WHPP|ADJP|WHADJP|ADVP|WHAVP|X|SBAR|NAC|CONJP|FRAG|INTJ|LST|NAC|NX|QP|PRC|PRN|PRT|QP|RRC|UCP|ROOT|S$',wd)):
                    stack_wd.append(wd+str(count))
                    count += 1
            else:
                stack_wd.append(wd)
        i += 1
    return sent_dic


with open(sys.argv[1]) as f:
    sents = f.readlines()



no_wds = 0
for sent in sents:

    for wd in sent.split():
        if(re.search('\)',wd)):
            no_wds += 1

    sent1 = re.sub('\(',' ( ',sent)
    sent2 = re.sub('\)',' ) ',sent1)
    sent_dic = parenthetic_contents(sent2.split(),no_wds)


    '''
    for key in sorted (sent_dic):
        print(key,'\t',sent_dic[key])
    '''


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

        if(len(pos_val.split('_')) > 1):
            word = pos_val.split('_')[0]
            pos = pos_val.split('_')[1]
        else:
            word = '_'
            pos = pos_val.split('_')[0]


        if(head_val != 'ROOT0'):
            print(idx,'\t',word,'\t',pos,'\t_','\t_','\t_','\t_\t',hd[head_val],'\tmother','\t',str(hd[head_val])+':mother','\t_')
        else:
            print(idx,'\t',word,'\t',pos,'\t_','\t_','\t_','\t_\t0','\tmother','\t','0:mother','\t_')

print('\n')
