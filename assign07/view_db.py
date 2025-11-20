from storage.sqlite_storage import SessionLocal
from models.sql_models import Author, ScientificArticle

session = SessionLocal()

print("Authors:")
for a in session.query(Author).all():
    print(a.id, a.full_name, a.title)

print("\nArticles:")
for art in session.query(ScientificArticle).all():
    print(art.id, art.title, art.arxiv_id, art.text, art.author.full_name)

session.close()