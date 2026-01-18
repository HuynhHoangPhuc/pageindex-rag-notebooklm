from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    pageindex_file_id: str  # ID returned by PageIndex
    user_id: int = Field(foreign_key="user.id")
    upload_status: str = Field(default="pending") # pending, processed, failed

sqlite_file_name = "pagelindex_rag.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
