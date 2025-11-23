from __future__ import annotations

from pathlib import Path

from usecases.load_csv_to_mariadb import load_csv_to_mariadb
from usecases.transfer_to_mongodb import transfer_to_mongodb
from usecases.search import search_articles


def main() -> None:
   
    load_csv_to_mariadb()

    
    project_root = Path(".")
    transfer_to_mongodb(root_path=project_root)

    
    search_query = "neural networks" 
    search_articles(search_query)


if __name__ == "__main__":
    main()
