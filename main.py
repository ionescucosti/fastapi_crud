import crud
import models
import schemas
from database import SessionLocal, engine

import json
from fastapi import FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')

    if user:
        name = user['given_name']
        html = (
            f'<pre>Welcome {name}!</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/docs">Swagger</a></h2></br>'
                        '<a href="/login">login</a>')


@app.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    print('redirect_uri >>>', redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@app.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@app.get("/accounts/")
async def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = crud.get_accounts(db, skip=skip, limit=limit)
    return accounts


@app.get("/account/{name}")
def get_account(name: str, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, name)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.post("/account/", response_model=schemas.AccountBase, status_code=status.HTTP_201_CREATED)
def create_user(account: schemas.AccountBase, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, name=account.name)
    if db_account:
        raise HTTPException(status_code=400, detail="Account already registered")
    return crud.create_account(db, account)


@app.put("/account/{name}", response_model=schemas.AccountBase)
def create_user(name: str, account: schemas.AccountBase, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, name=name)
    if db_account is None:
        raise HTTPException(status_code=400, detail="Account not registered")
    return crud.update_account(db, name, account)


@app.delete("/account/{name}")
def create_user(name: str, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, name=name)
    if db_account is None:
        raise HTTPException(status_code=400, detail="Account not registered")
    return crud.delete_account(db, name)
