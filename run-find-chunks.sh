pres_path=`pwd`
parser_path=`echo $HOME_anu_test/Parsers/stanford-parser/stanford-parser-4.0.0`

java -mx200m -cp $parser_path/*:  edu.stanford.nlp.parser.lexparser.LexicalizedParser -retainTMPSubcategories -outputFormat "oneline"   $parser_path/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $* 1> $1-parsed.out 2>$1-parse.log


cd $pres_path
python prog/constituency-to-conll.py $1-parsed.out > $1.conll
python prog/largest-np-pp-with-sbar.py  $1.conll
