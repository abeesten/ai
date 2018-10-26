from starter_code import BernoulliNaiveBayes, PreProcess
import sys

filePath = sys.argv[1]
bnb = BernoulliNaiveBayes(filePath, "stopwords.txt")
bnb.doEverything()
