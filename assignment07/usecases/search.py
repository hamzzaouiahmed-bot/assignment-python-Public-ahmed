from __future__ import annotations

from typing import List

from models.document import ScientificArticleDoc
from storage.mongodb import init_mongo_connection


def search_articles(query: str) -> None:
    init_mongo_connection()

    results: List[ScientificArticleDoc] = list(
        ScientificArticleDoc.objects.search_text(query)
    )

    print(f"Search results for: '{query}'")
    if not results:
        print("No articles found.")
        return

    for doc in results:
        print("-" * 40)
        print(f"Title : {doc.title}")
        print(f"Arxiv : {doc.arxiv_id}")
        print(f"Author: {doc.author.full_name} ({doc.author.title})")
