from sqlalchemy import create_engine
import pymysql

def get_engine():
   
    user = "root"
    password = "root123"
    host = "127.0.0.1"
    port = 3307
    database = "articles_db"

   
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    return engine
