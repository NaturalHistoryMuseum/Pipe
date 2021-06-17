from ._base import BaseClassifier
from ._utils import logger
from .forest import RandomForestClassifier
import logging


class ClassifyCore:
    classifiers = [RandomForestClassifier]

    @classmethod
    def run(cls, session_manager):
        logger.debug('Beginning classify stage')
        citations = BaseClassifier(session_manager).get_data()
        for classifier_type in cls.classifiers:
            classifier = classifier_type(session_manager)
            citations = classifier.process_data(citations)
        session_manager.log(citations)
        if logger.isEnabledFor(logging.DEBUG):
            # classification_id only evaluates properly (i.e. 1 == 1 == True) once you look at it,
            # so the classification_ids variable is just to inspect the ids before getting the
            # number of 'relevant' citations
            # it's purely for logging so if it's found to be too slow then it can be disabled
            classification_ids = [c.classification_id for c in citations]
            classified_true = len([c for c in classification_ids if c == '1'])
            logger.debug(
                f'Finished classifying. {len(citations)} citations processed; {classified_true} '
                f'classified as relevant.')
        return citations

    @classmethod
    def store(cls, session_manager, citations):
        BaseClassifier(session_manager).store_data(citations)
        logger.debug(f'{len(citations)} citations updated.')
