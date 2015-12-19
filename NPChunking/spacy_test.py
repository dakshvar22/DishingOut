from spacy.en import English, LOCAL_DATA_DIR
import spacy.en
import os, time

data_dir = os.environ.get('SPACY_DATA', LOCAL_DATA_DIR)
nlp = English(parser=False, tagger=True, entity=False)

def print_fine_pos(token):
    return token.tag_

def pos_tags(sentence):
    # sentence = str(sentence, "utf-8")
    # sentence = sentence.decode("utf-8")
    tokens = nlp(sentence)
    tags = []
    for tok in tokens:
        tags.append((tok,print_fine_pos(tok)))

    words = []
    for (pos,tag) in tags:
        words.append(pos.text)
    print(words)

    return tags

start = time.time()
a = "The dosa was brilliant and so was the samosa"
print(pos_tags(a))
print(time.time()-start)


