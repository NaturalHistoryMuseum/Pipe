from abc import abstractmethod


class BaseHarvester(object):
    """
    Load, parse, and store basic citation data from a source.
    """

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

    @classmethod
    def store_citations(cls, extracted_citations, session):
        """
        Store the extracted citation data.
        :return:
        """
        session.add_all(extracted_citations)
        session.flush()