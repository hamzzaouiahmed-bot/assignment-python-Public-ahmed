import mariadb
from pymongo import MongoClient
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET


def connect_mariadb(user="root", password="root", host="localhost", port=3306, database="articles_db"):
    conn = mariadb.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )
    print(" Connected to MariaDB successfully")
    return conn

def check_create_table_mariadb(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INT PRIMARY KEY,
            title VARCHAR(255),
            authors VARCHAR(255),
            published DATE,
            abstract TEXT
        )
    """)
    conn.commit()
    print("Table 'articles' checked/created successfully.")

def insert_article_mariadb(conn, article):
    cursor = conn.cursor()
    
    published = article.get("published")
    if published:
        if "T" in published:
            published = published.split("T")[0]
    try:
        cursor.execute("""
            INSERT INTO articles (id, title, authors, published, abstract)
            VALUES (?, ?, ?, ?, ?)
        """, (article.get("id"), article.get("title"), article.get("authors"), published, article.get("abstract")))
        conn.commit()
    except mariadb.IntegrityError:
        print(f"Duplicate entry {article.get('id')} ignored.")
    return article.get("id")


def connect_mongodb(host="localhost", port=27017, db_name="articles_db"):
    client = MongoClient(host, port)
    db = client[db_name]
    print("Connected to MongoDB successfully")
    return db

def insert_article_mongodb(db, article):
    collection = db.articles
    collection.update_one({"id": article.get("id")}, {"$set": article}, upsert=True)


def load_csv(filepath="articles.csv"):
    df = pd.read_csv(filepath, dtype=str)
    print(" CSV loaded successfully")
    return df


def fetch_arxiv(query="machine learning", max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    articles = []
    for entry in root.findall('atom:entry', ns):
        articles.append({
            "id": None,
            "title": entry.find('atom:title', ns).text.strip(),
            "authors": ", ".join([author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]),
            "published": entry.find('atom:published', ns).text,
            "abstract": entry.find('atom:summary', ns).text.strip()
        })
    df = pd.DataFrame(articles)
    print(f"{len(df)} articles fetched from ArXiv")
    return df


def fetch_html_content(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.get_text()
    except:
        return ""
