from fastapi import FastAPI, HTTPException, Depends
from http import HTTPStatus
from sqlalchemy import select
from spam.models import Models
from spam.routers import status, train, predict, auth, models
import os
from spam.database import get_session

app = FastAPI()
app.include_router(status.router)
app.include_router(train.router)
app.include_router(predict.router)
app.include_router(auth.router)
app.include_router(models.router)


@app.get('/')
def existModels(session=Depends(get_session)):
    '''
    Modelos disponiveis para treinamento
    '''
    try:
        return session.execute(select(Models.name)).scalars().all()
    
    except:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND)


@app.get('/{model}')
def avaibleModelsSpefic(model:str, session=Depends(get_session)):
    '''
    Modelos disponiveis para treinamento
    '''
    try:
        return session.execute(select(Models.name).where(Models.category == model)).scalars().all()
    
    except:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND)
