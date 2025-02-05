from fastapi import APIRouter, HTTPException,Depends
from http import HTTPStatus
from spam.database import get_session
from spam.models import Models
from sqlalchemy import select
from spam.schemas import ModelsName

router = APIRouter(prefix='/model', tags=['Model'])


@router.get('/{model_category}',response_model=ModelsName)
async def allModelsCategory(model_category: str, session=Depends(get_session)):
    '''
    EndPoint para recupear os nome dos modelos por categoria
    '''
    try:
    
        db = session.execute(select(Models.name, Models.versao).where(Models.category == model_category)).all()
        print(db)
        
        # Verificando se existe o tipo de modelo
        if db:

            return ModelsName(Name=db)
        else:
            return HTTPStatus.BAD_REQUEST
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    

