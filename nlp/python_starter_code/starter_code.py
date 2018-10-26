import glob, math, os, re, string, sys

class PreProcess:

    def __init__(self): pass

    ## Function to print the confusion matrix.
    ## Argument 1: "actual" is a list of integer class labels, one for each test example.
    ## Argument 2: "predicted" is a list of integer class labels, one for each test example.
    ## "actual" is the list of actual (ground truth) labels.
    ## "predicted" is the list of labels predicted by your classifier.
    ## "actual" and "predicted" MUST be in one-to-one correspondence.
    ## That is, actual[i] and predicted[i] stand for testfile[i].
    def printConfMat(self, actual, predicted):
        all_labels = sorted(set(actual + predicted))
        assert(len(actual) == len(predicted))
        confmat = {}  ## Confusion Matrix
        for i,a in enumerate(actual): confmat[(a, predicted[i])] = confmat.get((a, predicted[i]), 0) + 1
        print
        print
        print "0",  ## Actual labels column (aka first column)
        for label2 in all_labels:
            print label2,
        print
        for label in all_labels:
            print label,
            for label2 in all_labels:
                print confmat.get((label, label2), 0),
            print

    ## Function to remove leading, trailing, and extra space from a string.
    ## Inputs a string with extra spaces.
    ## Outputs a string with no extra spaces.
    def remove_extra_space(self, input_string):
        return re.sub("\s+", " ", input_string.strip())

    ## Tokenizer.
    ## Input: string
    ## Output: list of lowercased words from the string
    def word_tokenize(self, input_string):
        extra_space_removed = self.remove_extra_space(input_string)
        punctuation_removed = "".join([x for x in extra_space_removed if x not in string.punctuation])
        lowercased = punctuation_removed.lower()
        return lowercased.split()


class BernoulliNaiveBayes:
    def __init__(self, train_test_dir, vocab):
        self.numAuthors = 0
        self.featureFrequency = None
        self.train_test_dir = train_test_dir
        self.vocab = vocab
        self.p = PreProcess()
        self.authors = []
        self.features = []
        self.featRank = []
        self.wordsPerAuthor = []
        self.traindict = {}
        self.prior = {}
        self.cond = {}
        self.xplot = []
        self.yplot = []

    def get_author(self):
        for i in range(500):
            num = str(i).zfill(2)
            authors = glob.glob(self.train_test_dir + "/*train" + num + "*")
            self.numAuthors += len(authors)
            if len(authors) > 0:
                self.authors.append(i)
                self.traindict[i] = authors

    def get_features(self):
        with open(self.vocab) as f:
            for line in f.readlines():
                self.features.append(self.p.remove_extra_space(line))

    def featureFreq(self):
        words = {}
        feats = []
        for i in self.authors:
            for file in self.traindict[i]:
                with open(file, 'r') as file:
                    for line in file:
                        for word in self.p.word_tokenize(line):
                            words[word] = words.get(word, 0) + 1
        for feature in self.features:
            words[feature] = words.get(feature, 0)
            feats.append((feature,words[feature]))
        self.featureFrequency = sorted(feats, key=lambda item:item[1])[::-1]

    # return y values
    def curve(self):
        self.featureFreq()
        x = 10
        while x <= 420:
            if x > len(self.featureFrequency):
                x = len(self.featureFrequency)
            self.features = []
            for i in range(x):
                self.features.append(self.featureFrequency[i][0])
            self.xplot.append(len(self.features))
            # print('x = ' + str(len(self.features)))

            testFiles = glob.glob(self.train_test_dir + '/*sample*')
            testFiles.sort()

            test = []
            actual = []
            for testFile in testFiles:
                test.append(self.test(testFile))

            letter = self.train_test_dir[-1]
            true_directory = os.path.join(sys.path[0], 'test_ground_truth.txt')
            with open(true_directory, 'r') as f:
                for line in f.readlines():
                    if line.strip() and line[7] == letter:
                        actual.append(int(line[-3 : -1]))
            accuracy = 0
            for i in range(len(test)):
                if actual[i] == test[i]:
                    accuracy += 1
            acc = float(accuracy) / len(test)
            # acc * 100 is just to get percentage
            self.yplot.append(acc * 100)
            x += 10
        print(self.xplot)
        print(self.yplot)

    ## Define Train function
    def train(self):
        for i in self.authors:
            self.wordsPerAuthor = []
            # p(C)
            self.prior[i] = float(len(self.traindict[i])) / self.numAuthors

            countPerAuthor = {}
            for feature in self.features:
                countPerAuthor[feature] = 0

            for file in self.traindict[i]:
                essay = set()
                with open(file, 'r') as f:
                    for line in f:
                        for word in self.p.word_tokenize(line):
                            essay.add(word)
                    self.wordsPerAuthor.append(essay)

            for wordset in self.wordsPerAuthor:
                for feature in self.features:
                    if feature in wordset:
                        countPerAuthor[feature] += 1

            for feature in self.features:
                # p(fi | C)
                self.cond[(i, feature)] = (float(countPerAuthor[feature]) + 1) / (len(self.traindict[i]) + 2)

    ## Define Test function
    def test(self, testfilename):
        localProb = float("-Inf")
        index = 0

        essay = set()
        with open(testfilename, 'r') as file:
            for line in file:
                for word in self.p.word_tokenize(line):
                    essay.add(word)

        for i in self.authors:
            prob = math.log(self.prior[i], 2)
            for feature in self.features:
                if feature in essay:
                    prob += math.log(self.cond[(i, feature)], 2)
                else:
                    prob += math.log(1 - self.cond[(i, feature)], 2)
            if prob > localProb:
                index = i
                localProb = prob
        return index

    def autoTest(self):
        testFiles = glob.glob(self.train_test_dir + "/*sample*")
        testFiles.sort()
        test = []
        actual = []
        for testFile in testFiles:
            test.append(self.test(testFile))

        letter = self.train_test_dir[-1]
        true_directory = os.path.join(sys.path[0], 'test_ground_truth.txt')
        with open(true_directory, 'r') as f:
            for line in f.readlines():
                if line.strip() and line[7] == letter:
                    actual.append(int(line[-3 : -1]))

        # print accuracy
        accuracy = 0
        for i in range(len(test)):
            if actual[i] == test[i]:
                accuracy += 1
        acc = float(accuracy) / len(test)
        print(acc)

        self.p.printConfMat(actual, test)

        # rank features
        for feature in self.features:
            ent = 0
            for i in self.authors:
                ent -= self.prior[i] * self.cond[(i,feature)] * \
                    math.log(self.cond[(i,feature)], 2)
            self.featRank.append((feature, ent))
        fRank = sorted(self.featRank, key = lambda item:item[1])[::-1]

        # print top 20
        for i in range(20):
            word = fRank[i][0]
            featP = fRank[i][1]
            print(word + ": " + str(featP))

        #get accuracies with different amounts of features
        self.curve()

    def doEverything(self):
        self.get_author()
        self.get_features()
        self.train()
        self.autoTest()
