<%_ if (postgresql){  _%>
from backend.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
<%_ } _%>

<%_ if (mongodb){  _%>
from pydantic import BaseModel

class Message(BaseModel):
    channel: str
    author: str
    text: str
<%_ } _%>