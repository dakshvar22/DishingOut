__author__ = 'daksh'

from dishingOut.NPChunking.NPChunker import NPChunker

chunker = NPChunker()
chunker.train()
# tree,terms = chunker.extractChunk("Dosa was good")
# text = 'An institution in south indian offerings with Benne Masala Dosa at its best along with rava upma,kesari bath and mangalore bhajji with same level of excellence.Masala Dosa- You cant eat just one,will crave for more for sure.It tastes heavenly with the chutney CTR offers,its own kind.'
# text = 'Biryani was aromatic and superb'
# text = "Brilliant Idli Vada but Kara Bhath is not good!"
# text = "Amritsari fish were my favorites of the day"
# text = "Rasgulla and jamun were good"

# text = "Idli Vada and Kara Bhath are good!"
# text= "We had a crispy dosa and the coffee was not hot but the paneer was pathetic"
# text = "crispy dosa and coffee not hot"
# text = "Double masala chicken biryani served here is the best biryani I have tried till date"
# text = "Other starters that I have ordered like lemon chicken chicken kebab paneer Manchurian are okayish but the taste of biryani covers it all for me"
# text = "paneer was tasty"
# text = "I did not expect palak paneer to be so good but to my wonder it was excellent."
text = "Paneer tikka - Soft and tasty."

tree,terms = chunker.extractChunk(text)
tree.draw()
# tree.draw()
print(terms)
# sentences = chunker.getSentences(text)
# print(type(sentences[0]))
#for sent in sentences:
 #   print(chunker.getAdjetives(sent))