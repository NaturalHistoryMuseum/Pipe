from abc import abstractmethod
from pymysql.err import InternalError

class BaseHarvester(object):
    """
    Load, parse, and store basic citation data from a source.
    """

    def __init__(self, session_manager):
        self.session_manager = session_manager

    @abstractmethod
    def get_data(self):
        """
        Load the input data.
        :return:
        """
        pass

    @abstractmethod
    def parse_data(self, data):
        """
        Parse the input data to retrieve basic citation data.
        :return: list of ExtractedCitation instances
        """
        pass

    def store_citations(self, extracted_citations):
        """
        Store the extracted citation data.
        :return:
        """
        self.session_manager.session.add_all(extracted_citations)
        try:
            self.session_manager.session.flush()
        except InternalError as e:
            extracted_citations = [c for c in extracted_citations if c.email_id != e.params['email_id']]
            self.store_citations(extracted_citations)

