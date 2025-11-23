from __future__ import annotations

from typing import List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    articles: Mapped[List["ScientificArticle"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class ScientificArticle(Base):
    __tablename__ = "scientific_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(5000), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    arxiv_id: Mapped[str] = mapped_column(String(255), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    author: Mapped[Author] = relationship(back_populates="articles")
