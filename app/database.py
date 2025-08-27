from sqlmodel import create_engine, SQLModel, Session as SQLModelSession
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=SQLModelSession
)

def init_db():
    SQLModel.metadata.create_all(engine)
