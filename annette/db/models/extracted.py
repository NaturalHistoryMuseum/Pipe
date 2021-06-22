from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.dialects import mysql

from ..session import Base
from . import decorators


@decorators.column_access
@decorators.logged
class ExtractedCitation(Base):
    __tablename__ = 'extractedcitations'

    id = Column(Integer, autoincrement=True, primary_key=True)
    email_id = Column(String(40))
    title = Column(mysql.MEDIUMTEXT)
    snippet = Column(mysql.MEDIUMTEXT)
    author = Column(mysql.MEDIUMTEXT)
    pub_title = Column(mysql.MEDIUMTEXT)
    pub_year = Column(Integer)
    sent_date = Column(Date)
    source = Column(String(2))
    id_status = Column(mysql.TINYINT)
    label = Column(mysql.MEDIUMTEXT)
    doi = Column(String(100), default=None)
    snippet_match = Column(Integer)
    highlight_length = Column(Integer)
    last_identify_run = Column(Date, default=None)
