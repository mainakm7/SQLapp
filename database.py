from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL_sqlite = "sqlite:///./sqltodosapp.db"

# SQLALCHEMY_DATABASE_URL_PG = "postgresql://user:pass@localhost/sqltodosapp"
SQLALCHEMY_DATABASE_URL_MYSQL = "mysql+pymysql://root:test1234@localhost:8080/sqltodosapp"

# engine = create_engine(SQLALCHEMY_DATABASE_URL_sqlite, connect_args = {"check_same_thread":False})
engine = create_engine(SQLALCHEMY_DATABASE_URL_MYSQL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()