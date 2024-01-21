from pydantic import BaseModel


class AccountBase(BaseModel):
    name: str
