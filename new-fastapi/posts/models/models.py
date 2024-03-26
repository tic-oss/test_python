from core.database import Base
from sqlalchemy import Column, Integer, String


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer,primary_key=True,nullable=False)
    subject = Column(String,nullable=False)
    description = Column(String,nullable=False)
