import csv
from models.sql_models import Author, ScientificArticle, Base
from storage.sqlite_storage import SessionLocal, engine

def load_csv_to_sqlite(csv_path):
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            author = Author(full_name=row["author_full_name"], title=row["author_title"])
            session.add(author)
            session.flush()  
            article = ScientificArticle(
                title=row["title"],
                summary=row["summary"],
                file_path=row["file_path"],
                arxiv_id=row["arxiv_id"],
                text=row.get("text", ""),
                author_id=author.id
            )
            session.add(article)
    session.commit()
    session.close()
