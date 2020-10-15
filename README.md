## Finding Largest NP|PP|SBAR|S from a sentence

```
sh run-find-chunks.sh file
```
Please set the path to your stanford parser file in run-find-chunks.sh
The file should be one sentence per line


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

