import pandas as pd
from database import get_engine

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def save_to_db(df, table_name):
    engine = get_engine()
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    print(f"Data inserted into table '{table_name}' successfully.")

if __name__ == "__main__":
    file_path = "articles.csv"
    table_name = "articles"
    
    df = load_csv(file_path)
    print("CSV loaded successfully:")
    print(df.head())

    save_to_db(df, table_name)
