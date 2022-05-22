import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine(os.environ['DATABASE_URL'])
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
