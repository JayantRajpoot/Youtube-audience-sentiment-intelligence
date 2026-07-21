import nltk

resources = [
    "stopwords",
    "punkt",
    "punkt_tab",
    "wordnet",
    "omw-1.4"
]

for resource in resources:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource)