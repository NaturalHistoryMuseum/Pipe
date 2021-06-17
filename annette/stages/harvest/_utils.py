import itertools
import re
import unicodedata
import emoji
import nltk

from annette.utils.log import get_logger

logger = get_logger('annette.harvest')

nltk.download('punkt')


def clean_string(string):
    """
    Cleans string
    :param string: String to be cleaned
    :return: Clean string
    """
    return emoji.demojize(unicodedata.normalize("NFKD", string).replace("...", "").strip())


def minimum_word_distance(string):
    single_tokens = ["nhmuk", "nhml", "bmnh", "10.5519"]
    phrase_tokens = [('bm', 'nh'),
                     ('natural', 'history', 'museum', 'london')]

    tokens = [t.lower() for t in nltk.word_tokenize(string) if re.match('.*\w.*', t)]
    for label in single_tokens:
        if label in tokens:
            return 0
    min_distance = None
    for phrase in phrase_tokens:
        if not all([p in tokens for p in phrase]):
            continue
        indices = [[i for i, t in enumerate(tokens) if t == p] for p in phrase]
        phrase_min_distance = min([max(x) - min(x) for x in itertools.product(*indices)])
        # account for differences in phrase length
        phrase_min_distance -= len(phrase) - 1
        if min_distance is None:
            min_distance = phrase_min_distance
        else:
            min_distance = min(min_distance, phrase_min_distance)
    return min_distance
