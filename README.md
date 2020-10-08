## Finding Largest NP|PP|SBAR|S from a sentence

```
sh run-find-chunks.sh file
```
The file should be the penn tree parse in one line as given in the below example.

```
ROOT (S (S (NP (DT The) (JJ key) (NN difference)) (VP (VBZ is) (SBAR (IN that) (S (NP (DT an) (JJ explicit) (NN query)) (VP (VBZ is) (ADJP (JJ missing))))))) (CC and) (S (ADVP (RB instead)) (NP (PRP we)) (VP (MD can) (ADVP (RB only)) (VP (VB use) (NP (NP (JJ past) (NML (NN purchase) (CC and) (NN viewing)) (NNS decisions)) (PP (IN of) (NP (DT the) (NN user)))) (S (VP (TO to) (VP (VB predict) (NP (JJ future) (NML (NN viewing) (CC and) (NN purchase)) (NNS habits)))))))) (. .)))

```

# conll-tree-tools

Following are the different conll tree transformation tools.


'and' construction:
-------------------

```
python tree-and.py  and-ex1
```
Transformed tree is written to a file 'out'


'obl' construction:
-------------------
```
python tree-obl.py eng-obl-ex
python tree-obl.py hnd-obl-ex
```
output is written to stdout

output is  given in the form of a list [[Index],[Head_id],[Relations],[Words]]



Top value and Bottom Value calculation:
-------------------
```
python top_bottom_value.py tb-val-ex
```
output is written to stdout



To convert constituency  to conll format
-------------------
```
python constituency-to-conll.py const-conll-ex  > jnk
../conllu-viewer-master/bin/conllu2svg jnk > jnk.html 
```


To convert constituency original to indexed oneline format
-------------------
```
sh constituency-index.sh const-conll-ex
```

