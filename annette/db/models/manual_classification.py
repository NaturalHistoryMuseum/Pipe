from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects import mysql

from . import decorators
from ..session import Base


@decorators.column_access
class ManualClassification(Base):
    __tablename__ = 'manual_classification'

    doi = Column(String(100), primary_key=True)
    classification_id = Column(Boolean)
    label_name = Column(mysql.MEDIUMTEXT)
