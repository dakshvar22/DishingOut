import nltk
from nltk.corpus import stopwords
from os.path import expanduser
home = expanduser("~/PycharmProjects/untitled")
nltk.data.path.append("/home/daksh/Documents/Softwares/nltk_data")
from textblob import TextBlob

from nltk.tag import stanford 
from nltk.tag.stanford import StanfordPOSTagger


_path_to_model = home + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
_path_to_jar = home + '/stanford-postagger/stanford-postagger.jar'


pattern = """ 
                NP2: {<JJ.?>+ <RB>? <JJ.?>* <NN.?|FW>+ <VB.?>* <JJ.?>*}
                NP1: {<JJ.?>? <NN.?|FW>+ <CC>? <NN.?|FW>* <VB.?>? <RB.?>* <JJ.?>+}

                NP3: {<NP1><IN><NP2>}
                NP4: {<NP2><IN><NP1>}

            """
def leaves(tree):
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def get_terms(tree):
    for leaf in leaves(tree):
        term = [ w for w,t in leaf ]
        yield term


#~ a = "Dosa was good"
# a = "We had a crispy dosa and the coffee was not hot but the paneer was pathetic"
#~ a = "You should try the Soft yet Crispy Dosa of CTR"
a = "Idli Vada and Kara Bhath are good!"
#~ a = "crispy dosa and coffee not hot"
# a = "Double masala chicken biryani served here is the best biryani I have tried till date"
a = "Other starters that I have ordered like lemon chicken chicken kebab paneer Manchurian are okayish but the taste of biryani covers it all for me"
#~ a = "Recently opened here and as usual Biriyani is good here"

#~ a = "I did not expect palak paneer to be so good but to my wonder it was excellent."
a=a.lower()
stop_words = set(stopwords.words('english'))
#~ print stop_words
stop_words.remove('not')
stop_words.remove('and')
stop_words.remove('but')
stop_words.remove('or')
#~ stop_words.add('yet')
stop_words.remove('it')

chunker = nltk.RegexpParser(pattern,loop=3)
st = stanford.StanfordPOSTagger(_path_to_model,_path_to_jar)

tokens = nltk.word_tokenize(a)
postokens = st.tag(tokens)
# postokens = TextBlob(a).tags
print(postokens)

postokens = [(pos,tag) for (pos,tag) in postokens if pos not in stop_words]
print(postokens)

tree = chunker.parse(postokens)
tree.draw()

terms = get_terms(tree)

for term in terms:
    print(term)
