from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from storage.sqlite_storage import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255))
    title = Column(String(128))

class ScientificArticle(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    summary = Column(Text)
    file_path = Column(String(1024))
    arxiv_id = Column(String(128))
    text = Column(Text)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author")
