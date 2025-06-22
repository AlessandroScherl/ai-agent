import os

import sqlmodel
from sqlmodel import Session, SQLModel

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL == "":
    raise NotImplementedError("The `DATABASE_URL` needs to be set")


engine = sqlmodel.create_engine(DATABASE_URL)  #connect to DB itself

# database models
def init_db():
    print("creating databased tables . . .")
    SQLModel.metadata.create_all(engine)

# api routes
def get_session():
    with Session(engine) as session:
        yield session