from nltk import RegexpParser
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


def tokenise_authors(author_string):
    if author_string == '' or author_string is None:
        return []
    split_authors = []
    for a in author_string.split(';'):
        family_name, given_names = a.strip().split(',', 1)
        given_names = ' '.join([n[0] for n in given_names.split(' ') if len(n) > 0])
        rearranged = ' '.join([given_names.strip(), family_name.strip()]).strip()
        if rearranged != '':
            split_authors.append(rearranged)
    return split_authors


def tokenise_subjects(subject):
    if subject == '' or subject is None:
        return []
    split_subjects = []
    phrase_pattern = 'CHUNK:{<JJ>*<NN.?>*<VBG>*}'
    phrase_chunker = RegexpParser(phrase_pattern)
    for s in subject.split(','):
        tokens = word_tokenize(s.strip().lower())
        tags = pos_tag(tokens)
        phrases = [' '.join([leaf[0] for leaf in c.leaves()]) for c in phrase_chunker.parse(tags) if hasattr(c, 'label') and c.label() == 'CHUNK']
        for phrase in phrases:
            phrase_tokens = word_tokenize(phrase)
            phrase_tags = pos_tag(phrase_tokens)
            lemmatised_phrase = []
            for pto, pta in phrase_tags:
                wn_tag = {
                    'n': wn.NOUN,
                    'j': wn.ADJ,
                    'v': wn.VERB,
                    'r': wn.ADV
                    }.get(pta[0].lower(), None)
                if wn_tag is None:
                    continue
                lemmatised = WordNetLemmatizer().lemmatize(pto, wn_tag)
                lemmatised_phrase.append(lemmatised)
            if len(lemmatised_phrase) > 0:
                lemmatised_phrase = ' '.join(lemmatised_phrase)
                split_subjects.append(lemmatised_phrase)
    return list(set(split_subjects))
