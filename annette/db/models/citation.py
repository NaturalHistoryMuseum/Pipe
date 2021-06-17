from sqlalchemy import Column, Date, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql

from . import decorators
from ..session import Base
from .extracted import ExtractedCitation


@decorators.column_access
@decorators.logged
class Citation(Base):
    __tablename__ = 'citations'

    doi = Column(String(100), primary_key=True)
    author = Column(mysql.MEDIUMTEXT)
    title = Column(mysql.MEDIUMTEXT)
    type = Column(mysql.MEDIUMTEXT)
    issued_date = Column(Date)
    subject = Column(mysql.MEDIUMTEXT)
    pub_title = Column(mysql.MEDIUMTEXT)
    pub_publisher = Column(mysql.MEDIUMTEXT)
    issn = Column(String(9))
    isbn = Column(String(14))
    issue = Column(mysql.MEDIUMTEXT)
    volume = Column(mysql.MEDIUMTEXT)
    page = Column(mysql.MEDIUMTEXT)
    classification_id = Column(Integer)
    ecid = Column(ForeignKey(ExtractedCitation.id))
    raw = relationship('ExtractedCitation', backref='citation')
