from database import get_engine
import pandas as pd

def test_connection():
    engine = get_engine()
    try:
        
        df = pd.read_sql("SELECT * FROM articles", con=engine)
        print("Database connection successful! Here is the data:")
        print(df)
    except Exception as e:
        print("Error connecting to the database:", e)

if __name__ == "__main__":
    test_connection()
