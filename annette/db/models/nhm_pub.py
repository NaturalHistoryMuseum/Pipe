from sqlalchemy import Column, String
from sqlalchemy.dialects import mysql

from . import decorators
from ..session import Base


@decorators.column_access
class NHMPub(Base):
    __tablename__ = 'nhm_pubs'

    issn = Column(String(9), primary_key=True)
    pub_title = Column(mysql.TEXT)
