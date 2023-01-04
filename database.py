from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

MYSQL_DB_URL = "mysql+pymysql://root:1212amam@localhost/signupandlogin"

engine = create_engine(MYSQL_DB_URL)

sessionlocal = Session(bind=engine, autocommit=False, expire_on_commit=False)

Base = declarative_base()