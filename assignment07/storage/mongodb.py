from __future__ import annotations

from mongoengine import connect


def init_mongo_connection() -> None:
   
    connect(
        db="articles_mongo",
        host="localhost",
        port=27017,
        alias="default",
    )
