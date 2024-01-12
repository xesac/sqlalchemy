from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    age: Mapped[int]

db = Session(autoflush=False, bind=engine)
