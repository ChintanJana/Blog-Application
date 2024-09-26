from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

URL_DATABASE = "mysql+pymysql://blog_application:Admin#123@localhost:3306/BlogApplication"

engine = create_engine(URL_DATABASE, echo = True)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    autocommit = False, 
    autoflush = False,
    bind = engine
)