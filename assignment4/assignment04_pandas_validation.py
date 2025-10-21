import pandas as pd
import numpy as np
from functools import partial


data = {
    "user_id": [1, 2, 3, 3],
    "name": ["Ahmed", "Mouhamed", "Ali", "Ali"],
    "age": [23, 25, np.nan, 25],
    "city": ["Tunis", "Sfax", "Sousse", "Sousse"],
    "salary": ["2500", "3000", "invalid", "2800"],
    "birth_date": ["2001-07-11", "1999-03-21", None, "2000-01-15"]
}

df = pd.DataFrame(data)
df.to_csv("employees.csv", index=False)


s = pd.Series([100, 200, 300], index=["A", "B", "C"])
print(s)


print(df.dtypes)
print(df.head())
print(df.describe(include="all"))


print(df.iloc[:2])
print(df[["name", "city"]])


print(df[df["age"] > 23])

print(df.duplicated())
print(df["name"].nunique())
df = df.drop_duplicates()
print(df)


df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
print(df.dtypes)


def fill_age(x):
    return 24 if pd.isna(x) else x

df["age"] = df["age"].apply(fill_age)
print(df)


def convert_types(data):
    data["salary"] = pd.to_numeric(data["salary"], errors="coerce")
    data["birth_date"] = pd.to_datetime(data["birth_date"], errors="coerce")
    return data

df = df.pipe(convert_types)
print(df.dtypes)
print(df.isnull().sum())


def remove_low_salary(data, threshold):
    return data[data["salary"] > threshold]

df = df.pipe(partial(remove_low_salary, threshold=2600))
print(df)
