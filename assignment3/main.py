from typing import TypedDict
from collections import namedtuple
from dataclasses import dataclass
from pydantic import BaseModel
import numpy as np
import pandas as pd
import time


class UserTD(TypedDict):
    id: int
    name: str
    age: int
    email: str

UserNT = namedtuple("UserNT", ["id", "name", "age", "email"])

@dataclass
class UserDC:
    id: int
    name: str
    age: int
    email: str

class UserPD(BaseModel):
    id: int
    name: str
    age: int
    email: str


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper


@timer
def multiply_list(lst, scalar):
    return [x * scalar for x in lst]

@timer
def multiply_numpy(arr, scalar):
    return arr * scalar


num_array = np.array([1, 2, 3, 4, 5])
num_list = [1, 2, 3, 4, 5]


multiply_list(num_list, 10)
multiply_numpy(num_array, 10)



df = pd.read_csv("users.csv")
print(df)


big_list = list(range(1_000_000))
big_array = np.array(big_list)

multiply_list(big_list, 10)
multiply_numpy(big_array, 10)
