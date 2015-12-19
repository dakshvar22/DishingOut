__author__ = 'daksh'

import csv
vocab = None
with open('vocabulary.csv', 'r') as csvfile:
    spamwriter = csv.reader(csvfile)
    vocab = list(spamwriter)

vocab = [word for [word] in vocab]
print(len(vocab))

vocab = list(set(vocab))
print(len(vocab))
# with open('vocabCleaned.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter='\n',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(vocab)

# print(vocab.index('impressing'))
print(vocab)