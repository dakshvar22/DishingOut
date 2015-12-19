__author__ = 'daksh'

import nltk
from nltk.corpus import stopwords
from os.path import expanduser
home = expanduser("~/PycharmProjects/untitled")
nltk.data.path.append("/home/daksh/Documents/Softwares/nltk_data")
from nltk.tag import stanford
from nltk.tokenize import RegexpTokenizer
nltk.internals.config_java(options='-xmx2G')
from textblob import TextBlob
import os
java_path = "/usr/bin/java"
os.environ['JAVAHOME'] = java_path
from spacy.en import English, LOCAL_DATA_DIR
import os, time
import string

data_dir = os.environ.get('SPACY_DATA', LOCAL_DATA_DIR)



class NPChunker():
    def __init__(self):
        self.pattern = """

                NP2: {<JJ.?>+ <RB>? <JJ.?>* <NN.?|FW>+ <VB.?>* <JJ.?>*}
                NP1: {<JJ.?>? <NN.?|FW>+ <CC>? <NN.?|FW>* <VB.?>? <RB.?>* <JJ.?>+ (<CC><JJ.?>)?}

            """
        self.st = None
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = RegexpTokenizer(r'\w+')
        self.nlp = English(parser=False, tagger=True, entity=False)
        self.exclude = set(string.punctuation)

    def leaves(self,tree):
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP1' or t.label()=='NP2'):
            yield subtree.leaves()

    def get_terms(self,tree):
        for leaf in self.leaves(tree):
            term = [ w for w,t in leaf ]
            yield term

    def train(self):
        # _path_to_model = home + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
        _path_to_model = home + '../../stanford-postagger/models/english-left3words-distsim.tagger'
        _path_to_jar = home + '../../stanford-postagger/stanford-postagger.jar'

        self.st = stanford.StanfordPOSTagger(_path_to_model,_path_to_jar)

    ''' Extract Dish with its adjectives from a sentence
    Uses Stanford POS Tagger with NLTK library'''

    def print_fine_pos(self,token):
        return token.tag_

    def extractChunk(self,sentence):
        sentence = sentence.lower()

        stop_words = set(stopwords.words('english'))
        stop_words.remove('not')
        stop_words.remove('and')
        stop_words.remove('but')
        stop_words.remove('or')
        # stop_words.add('yet')
        stop_words.remove('it')


        sentence = ''.join(ch for ch in sentence if ch not in self.exclude)
        sentence = ' '.join(sentence.split())
        # print(sentence)
        chunker = nltk.RegexpParser(self.pattern,loop=3)

        ######
        ''' Using nltk pos tagger '''
        # tokens = self.nltk_tokenizer.tokenize(sentence)
        # postokens = self.st.tag(tokens)
        # postokens = [(pos,tag) for (pos,tag) in postokens if pos not in stop_words]

        ######

        ######
        ''' Using spacy(cython) POS tagger'''
        tokens = self.nlp(sentence)
        # print(tokens)
        postokens = []
        for tok in tokens:
            postokens.append((tok,self.print_fine_pos(tok)))
        postokens = [(pos.text,tag) for (pos,tag) in postokens if pos.text not in stop_words]
        ######

        tree = chunker.parse(postokens)
        #tree.draw()

        terms = self.get_terms(tree)

        # for term in terms:
        #     print(term)

        return tree,list(terms)


    ''' Returns Adjectives in a sentence using TExtBlob POS tagging
    Advantage : JUst fast!
    '''
    def getAdjectives(self,sentence):
        try:
            sentence = sentence.lower()
            tokens =self.getWords(sentence)
            text = " ".join(tokens)
            # print(text)
            # postokens = self.st.tag(tokens)
            # print(sentence)
            wiki = TextBlob(text)
            postokens = wiki.tags
            tags = ['JJ','JJR','JJS']

            postokens = [(pos,tag) for (pos,tag) in postokens if tag in tags]

        except:
            print(sentence)
            postokens = []
        return postokens

    def getNouns(self,sentence):
        sentence = sentence.lower()
        tokens = self.getWords(sentence)
        postokens = self.st.tag(tokens)
        tags = ['NN','NNS','NNP','NNPS','FW']

        postokens = [(pos,tag) for (pos,tag) in postokens if tag in tags]

        return postokens

    def getSentences(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        print(sentences)
        #tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        words = list()
        # for sentence in tokenized_sentences:
        #     words = [word for word in sentence if word not in ]

        return sentences

    def getWords(self,text):
        words = list()
        try:
            words = self.nltk_tokenizer.tokenize(text)
        except:
            pass
        return words


if __name__ == '__main__':
    chunker = NPChunker()
    chunker.train()

    # adj = chunker.getAdjectives("The samosa was soft but soggy")
    # print(adj)
    tree,terms = chunker.extractChunk("Dosa was - good")
    tree.draw()
    print(terms)