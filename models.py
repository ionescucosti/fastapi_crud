from sqlalchemy import Column, Integer, String
from database import Base


class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    created = Column(String)
    login = Column(String)
