import sqlite3
import os

def main():
    db_path = os.path.join(os.path.dirname(__file__), "ahmed.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Authors:")
    cursor.execute("SELECT id, full_name, title FROM authors")
    authors = cursor.fetchall()
    for a in authors:
        print(a)

    print("\nArticles:")
    cursor.execute("""
        SELECT articles.id, articles.title, articles.summary, articles.arxiv_id, authors.full_name
        FROM articles
        JOIN authors ON articles.author_id = authors.id
    """)
    articles = cursor.fetchall()
    for ar in articles:
        print(ar)

    conn.close()

if __name__ == "__main__":
    main()
