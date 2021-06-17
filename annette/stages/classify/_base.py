from abc import abstractmethod
from annette.db.models import Citation


class BaseClassifier(object):
    """
    Classify citations.
    """

    def __init__(self, session_manager):
        self.session_manager = session_manager

    def get_data(self):
        """
        Load the input data.
        :return:
        """
        return self.session_manager.session.query(Citation).filter(
            Citation.classification_id.is_(None)).all()

    @abstractmethod
    def process_data(self, citations):
        """
        Process/classify the citations.
        :param citations:
        :return: list of citations
        """
        pass

    def store_data(self, citations):
        """
        Store the classification results.
        :return:
        """
        self.session_manager.session.add_all(citations)
        self.session_manager.session.flush()
