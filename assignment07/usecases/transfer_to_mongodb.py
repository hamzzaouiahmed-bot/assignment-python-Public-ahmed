from __future__ import annotations

from pathlib import Path
from typing import List

from PyPDF2 import PdfReader
from sqlalchemy.orm import Session

from models.document import AuthorDoc, ScientificArticleDoc
from models.relational import ScientificArticle
from storage.mariadb import get_session
from storage.mongodb import init_mongo_connection


def pdf_to_markdown(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    reader = PdfReader(str(file_path))
    texts: List[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        texts.append(page_text)

   
    markdown_text = "\n\n".join(texts)
    return markdown_text


def transfer_to_mongodb(root_path: Path | None = None) -> None:
   
    if root_path is None:
        root_path = Path(".")

    init_mongo_connection()

    session: Session = get_session()
    try:
        articles: List[ScientificArticle] = session.query(ScientificArticle).all()

        for art in articles:
            pdf_path = root_path / art.file_path
            markdown_text = pdf_to_markdown(pdf_path)

            author_doc = AuthorDoc(
                full_name=art.author.full_name,
                title=art.author.title,
            )

            doc = ScientificArticleDoc(
                title=art.title,
                summary=art.summary,
                text=markdown_text,
                arxiv_id=art.arxiv_id,
                author=author_doc,
            )
            doc.save()

        print(" Data transferred from MariaDB to MongoDB successfully.")
    finally:
        session.close()
