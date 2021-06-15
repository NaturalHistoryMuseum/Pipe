from nltk import RegexpParser, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from ._base import BaseAttributeCluster


class SubjectAttributeCluster(BaseAttributeCluster):
    attribute_name = 'subject'

    @staticmethod
    def tokenise(input_string):
        if input_string == '' or input_string is None:
            return []
        split_subjects = []
        phrase_pattern = 'CHUNK:{<JJ>*<NN.?>*<VBG>*}'
        phrase_chunker = RegexpParser(phrase_pattern)
        for s in input_string.split(','):
            tokens = word_tokenize(s.strip().lower())
            tags = pos_tag(tokens)
            phrases = [' '.join([leaf[0] for leaf in c.leaves()]) for c in
                       phrase_chunker.parse(tags) if hasattr(c, 'label') and c.label() == 'CHUNK']
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
