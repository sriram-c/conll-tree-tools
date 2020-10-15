pres_path=`pwd`
parser_path='/home/sriram/alignment/anusaaraka/Parsers/stanford-parser/stanford-parser-4.0.0'
cp $1 $parser_path/.
cd $parser_path

java -mx200m -cp ./*:  edu.stanford.nlp.parser.lexparser.LexicalizedParser -retainTMPSubcategories -outputFormat "oneline"   edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $* 1> $1-parsed.out 2>$1-parse.log

cd $pres_path
python prog/constituency-to-conll.py $1-parsed.out > $1.conll
python prog/largest-np-pp-with-sbar.py  $1.conll
