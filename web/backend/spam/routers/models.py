from fastapi import APIRouter, HTTPException,Depends
from http import HTTPStatus
from spam.database import get_session
from spam.models import Modelos
from sqlalchemy import select
from spam.schemas import ModelsName

router = APIRouter(prefix='/model', tags=['Model'])


@router.get('/{model_category}')
async def allModelsCategory(model_category: str, session=Depends(get_session)):
    '''
    EndPoint para recupear os nome dos modelos por categoria
    '''
    try:
    
        db = session.execute(select(Modelos.name, Modelos.versao).where(Modelos.category == model_category)).all()

        # Verificando se existe o tipo de modelo
        if db:

            return db
        
        else:
            return HTTPStatus.BAD_REQUEST
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    

