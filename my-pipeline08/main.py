from utils import (
    connect_mariadb,
    check_create_table_mariadb,
    insert_article_mariadb,
    connect_mongodb,
    insert_article_mongodb,
    load_csv,
    fetch_arxiv
)


df = load_csv("articles.csv")


mariadb_conn = connect_mariadb(user="root", password="root", host="localhost", port=3307, database="articles_db")
check_create_table_mariadb(mariadb_conn)
df.apply(lambda row: insert_article_mariadb(mariadb_conn, row.to_dict()), axis=1)


mongo_db = connect_mongodb()
df.apply(lambda row: insert_article_mongodb(mongo_db, row.to_dict()), axis=1)


arxiv_df = fetch_arxiv(query="machine learning", max_results=5)

arxiv_df['id'] = range(len(df)+1, len(df)+1+len(arxiv_df))


arxiv_df.apply(lambda row: insert_article_mariadb(mariadb_conn, row.to_dict()), axis=1)
arxiv_df.apply(lambda row: insert_article_mongodb(mongo_db, row.to_dict()), axis=1)

print(" Data pipeline completed successfully!")
