from fastapi import APIRouter,HTTPException, Depends
from fastapi.responses import FileResponse

from http import HTTPStatus
from spam.database import get_session
from sqlalchemy import select
from spam.models import Modelos
from spam.schemas import TrainingDate
from datetime import datetime
import os
from settings import Settings


router = APIRouter(prefix='/status', tags=['Status'])


@router.get('/', response_model=TrainingDate)
async def models(session=Depends(get_session)):
    '''
    EndPoint com informação do modelo treinando
    '''
    try:
        # recuperando dados do modelo
        train_model = session.execute(select(Modelos.status).where(Modelos.status == 'Train')).scalars().first()
        if train_model:
            return TrainingDate(msg='Train',
                    model=train_model.name,
                    time=1,
                    data=datetime.now(),
                    percentage=1,
                    epoch=1,
                    status=200)
            
        else:
            raise HTTPException(HTTPStatus.NO_CONTENT, detail='Não há modelos treinando')
    
    except Exception as e :
        return HTTPException(status_code=HTTPStatus.BAD_GATEWAY, detail=str(e))

@router.get('/{model}/{name}/{version}', response_model=TrainingDate)
async def log(model:str, name:str, version:int, session=Depends(get_session)):
    '''
    Endpoint para recuperar loggs do sistema
    '''
    try:
        name_uuid = session.execute(select(Modelos.uuid).where(Modelos.category == model).where(Modelos.name == name).where(Modelos.versao == version)).scalars().first()
        if name_uuid:
            # Caminho para o log
            path = os.path.join(Settings().LOG, f'{name_uuid}.log')
            
            if os.path.isfile(path):
                return FileResponse(path=path,media_type="text/plain",filename=f"{name_uuid}.log")
            
            else:
                raise HTTPStatus.NOT_FOUND
        
        else:
            raise HTTPStatus.NOT_FOUND
    except Exception as e:
        return HTTPException(HTTPStatus.BAD_REQUEST, detail=str(e))




