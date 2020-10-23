import sys
import re
from bs4 import BeautifulSoup, Tag, NavigableString

with open(sys.argv[1]) as fp:
    soup = BeautifulSoup(fp, 'lxml-xml')

root = soup.find_all(value='ROOT')[0]


def find_leaf(tag, phrase):
    tmp_wd = []

    if(tag['value'] == 'CC'):
        cc_wd = tag.find_all('leaf')[0]['value']

        prev_sib = list(tag.previous_siblings)[1]
        prev_sib_depth = str(len(list(prev_sib.parents)))
        prev_sib1 = prev_sib['value']+prev_sib_depth

        next_sib = list(tag.next_siblings)[1]
        next_sib_depth = str(len(list(next_sib.parents)))
        next_sib1 = next_sib['value'] + next_sib_depth

        phrase.append([tag['value']+str(len(list(tag.parents))), prev_sib1, next_sib1, cc_wd])

    #elif (tag.name != 'leaf'):
    elif (re.match( r'^NP|WHNP|PP|WHPP|ADJP|WHADJP|ADVP|WHAVP|X|SBAR|NAC|NML|CONJP|FRAG|INTJ|LST|NAC|NX|QP|PRC|PRN|PRT|QP|RRC|UCP|ROOT|S|,$', tag['value']) and (tag.name != 'leaf')):
        for wd in tag.find_all('leaf'):
                tmp_wd.append(wd['value'])
        phrase.append([tag['value']+str(len(list(tag.parents))), tmp_wd])

def find_lwg(tag,tmp_lwg,flag):
    for tag1 in tag.contents:
        if (isinstance(tag1, Tag)):
            if (re.match(r'^VB|RB|TO|MD', tag1['value'])):
                tmp_lwg.append(tag1.find_all('leaf')[0]['value'])

            elif (re.match(r'^VP', tag1['value'])):
                find_lwg(tag1,tmp_lwg,1)
    if(flag == 0):
        phrase.append([tag['value']+'_LWG'+str(len(list(tag.parents))), tmp_lwg])


def process_tag(tag, phrase):
        if (isinstance(tag, Tag)):
            if (tag['value'] == 'VP') and (tag.parent['value'] != 'VP'):
                tmp_lwg = []
                #find_leaf(tag)
                find_lwg(tag,tmp_lwg,0)
                for tag1 in tag.contents:
                    if (isinstance(tag1, Tag)):
                        process_tag(tag1, phrase)


            elif(re.match(r'CC',tag['value'])):
                find_leaf(tag, phrase)

            else:
                find_leaf(tag, phrase)
                for tag1 in tag.contents:
                    if (isinstance(tag1, Tag)):
                        process_tag(tag1, phrase)

phrase = []
for ch in root.contents:
    if(isinstance(ch, Tag)):
        process_tag(ch,phrase)

for p in phrase:
    if(re.match(r'CC',p[0])):
        print(p[0], ':', p[1],'-', p[3], '-', p[2])
    else:
        print(p[0],':',' '.join(p[1]))