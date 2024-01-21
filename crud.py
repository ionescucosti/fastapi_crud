import datetime

import models
import schemas

from sqlalchemy.orm import Session


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Accounts).offset(skip).limit(limit).all()


def get_account(db: Session, name: str):
    return db.query(models.Accounts).filter(models.Accounts.name == name).first()


def create_account(db: Session, account: schemas.AccountBase):
    db_account = models.Accounts(name=account.name, created=datetime.datetime.now(),
                                 login=datetime.datetime.now())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def update_account(db: Session, name: str, account: schemas.AccountBase):
    db_account = db.query(models.Accounts).filter(models.Accounts.name == name).first()
    db_account.name = account.name
    db.commit()
    db.refresh(db_account)
    return db_account


def delete_account(db: Session, name: str):
    db_account = db.query(models.Accounts).filter(models.Accounts.name == name).first()
    db.delete(db_account)
    db.commit()
    return db_account
