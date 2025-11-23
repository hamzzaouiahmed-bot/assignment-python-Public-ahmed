from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Tuple

from sqlalchemy.orm import Session

from models.relational import Author, ScientificArticle
from storage.mariadb import get_session, create_database_schema


DATA_PATH = Path("data") / "articles.csv"


def _get_or_create_author(
    session: Session, full_name: str, title: str
) -> Author:
    author = (
        session.query(Author)
        .filter(Author.full_name == full_name, Author.title == title)
        .one_or_none()
    )
    if author is None:
        author = Author(full_name=full_name, title=title)
        session.add(author)
        session.flush()  # للحصول على id مباشرة
    return author


def load_csv_to_mariadb(csv_path: Path | None = None) -> None:
    create_database_schema()
    if csv_path is None:
        csv_path = DATA_PATH

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    session: Session = get_session()
    try:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                author = _get_or_create_author(
                    session=session,
                    full_name=row["author_full_name"],
                    title=row["author_title"],
                )
                article = ScientificArticle(
                    title=row["title"],
                    summary=row["summary"],
                    file_path=row["file_path"],
                    arxiv_id=row["arxiv_id"],
                    author=author,
                )
                session.add(article)

        session.commit()
        print(" Data loaded from CSV to MariaDB successfully.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
