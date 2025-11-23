import os
import sqlite3
from usecases.csv_to_sqlite import load_csv_to_sqlite
from pymongo import MongoClient
import pandas as pd  

def load_sqlite_to_mongo(sqlite_db_path):
    """Load data from SQLite to MongoDB."""
   
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

  
    client = MongoClient("mongodb://localhost:27017/")
    db = client['ahmed']

    
    db.authors.drop()
    db.scientific_articles.drop()

   
    cursor.execute("SELECT id, full_name, title FROM authors")
    authors = cursor.fetchall()
    authors_docs = [{"_id": a[0], "full_name": a[1], "title": a[2]} for a in authors]
    if authors_docs:
        db.authors.insert_many(authors_docs)

    
    cursor.execute("SELECT id, title, summary, arxiv_id, text, author_id FROM articles")
    articles = cursor.fetchall()
    articles_docs = [
        {
            "_id": ar[0],
            "title": ar[1],
            "summary": ar[2],
            "arxiv_id": ar[3],
            "text": ar[4],
            "author_id": ar[5]
        }
        for ar in articles
    ]
    if articles_docs:
        db.scientific_articles.insert_many(articles_docs)

    print("Data inserted into MongoDB successfully!")

    
    print("\nAuthors Table:")
    authors_df = pd.DataFrame(authors_docs)
    print(authors_df)

    print("\nArticles Table:")
    articles_df = pd.DataFrame(articles_docs)
    print(articles_df)

def main():
   
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "articles.csv")
    sqlite_db_path = os.path.join(base_dir, "ahmed.db")

  
    load_csv_to_sqlite(csv_path)
    print("CSV loaded into SQLite successfully!")

  
    load_sqlite_to_mongo(sqlite_db_path)

if __name__ == "__main__":
    main()
