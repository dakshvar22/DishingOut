# DishingOut
DishingOut is a dish based rating system developed using Python's NLP tools. 
### Requirements
Following are the required Python modules:
* nltk - Python's natural language processing toolkit
* spaCy - Industrial strength NLP tasks in Python//Cython
* requests - HTTP library for Python
* BeautifulSoup - HTML parser

### Preprocessing
* The modify_reviews.py file works on the original dataset. It filters the reviews by removing the sentences from each review text which do not contain any dish names in them. 
* The clean_data.py file consequently replaces unicode special characters with their Python string equivalents.

### Running instructions
* Install all dependencies.
* Run mainAlgo.py in the DishingOut folder.

