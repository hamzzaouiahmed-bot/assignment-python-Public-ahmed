from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///ahmed.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
