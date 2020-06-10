# Import standard libraries
import pandas as pd
import re

# NLTK libraries
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from todoist.api import TodoistAPI

# pandas settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# dummy / synthetic data
test_task = [{"id": 1, "content": "[test description](http://link.com)"},
             {"id": 2, "content": "unrelated"},
             {"id": 3, "content": "some other test"},
             {"id": 4, "content": "old macdonald had a farm"},
             {"id": 5, "content": "keep it secret. keep it safe."}]

# Functions
def gen_text(words):
    tokens = word_tokenize(words)
    no_sw = [w for w in tokens if not w in stopwords.words('english')]
    ps = nltk.wordnet.WordNetLemmatizer()
    stemmed = [ps.lemmatize(word) for word in no_sw]
    return stemmed

def parse_task(tasks, level = "content", k = 2):
    knnmap = pd.DataFrame([(tt["id"], tt[level]) for tt in tasks],
                           columns = ["ID", level])

    # extract all words between brackets from links
    ptrn = '\[(.*?)\]|[\w\s]+'

    # Prioritize the column that will be cleaned
    # Note: currently, I only analyze the direct text that is provided.
    #       Eventually, I will focus on parsing the enriched text of the actual
    #       posts / comments.
    content_focus = knnmap.content.tolist()
    knnmap["delinked"] = [re.search(ptrn, cc).group(0) for cc in content_focus]
    knnmap["cleaned"] = [gen_text(dlk) for dlk in knnmap["delinked"].tolist()]

    # return the pandas dataframe with the categorizations
    return knnmap

# Documentation
parse_task.__doc__ = \
    """parse tasks to determine their categorical closeness
       relative to the `k` number of groups specified

       The default `k` groups is set to 10, and is determined based off
       of a k-nearest neighbors algorithm."""

gen_text.__doc__ = \
    """Strip text of hyperlinks, lemmatize text into the singular form, and
       all other operations related to simplifying task text.

       'Generalize' text into a consumable format so that tasks can be compared
       and categorized against one another."""

print(parse_task(test_task))
