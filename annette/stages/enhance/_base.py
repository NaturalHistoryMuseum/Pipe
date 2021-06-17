from abc import abstractmethod

from annette.db.models import Citation


class BaseEnhancer(object):
    """
    Get extra metadata for citations.
    """

    def __init__(self, session_manager):
        self.session_manager = session_manager

    def get_data(self):
        """
        Load the input data.
        :return:
        """
        return self.session_manager.session.query(Citation).filter(Citation.classification_id is not None).all()

    @abstractmethod
    def get_metadata(self, citation):
        """
        Get extra metadata about the citation.
        :return: list of enhancer/metadata instances
        """
        pass

    def store_metadata(self, metadata):
        """
        Store the extracted citation data.
        :return:
        """
        self.session_manager.session.add_all(metadata)
        self.session_manager.session.flush()

    @property
    def run_now(self):
        """
        A true/false value indicating whether the enhancer should be run at this time; for making
        sure an enhancer only runs e.g. once a month.
        :return: boolean
        """
        return True
