from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from spam.models import Models
from sqlalchemy import select
from spam.database import get_session
import os 


router = APIRouter(prefix='/predict', tags=['predict'])

@router.get('/{model}')
def predict(model:str, session=Depends(get_session)):
    '''
    Endpoint para predizer uma imagem
    '''
    
    
    
    
    