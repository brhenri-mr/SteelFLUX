from fastapi import APIRouter,HTTPException, Depends
from fastapi.responses import FileResponse

from http import HTTPStatus
from spam.database import get_session
from sqlalchemy import select
from spam.models import Models
from spam.schemas import TrainingDate
from datetime import datetime
import os
from settings import Settings


router = APIRouter(prefix='/status', tags=['Status'])


@router.get('/', response_model=TrainingDate)
def models(session=Depends(get_session)):
    try:
        # recuperando dados do modelo
        train_model = session.execute(select(Models.status).where(Models.status == 'Train')).scalars().all()
        
        return TrainingDate(msg='Train',
                 model=train_model.name,
                 time=1,
                 data=datetime.now(),
                 percentage=1,
                 epoch=1,
                 status=200)
        
    
    except:
        return HTTPException(status_code=HTTPStatus.BAD_GATEWAY)

@router.get('/{model}/{version}', response_model=TrainingDate)
def log(model:str, version:int, session=Depends(get_session)):
    '''
    Endpoint para recuperar loggs do sistema
    '''
    
    name = session.execute(select(Models.uuid).where(Models.category == model).where(Models.version == version)).scalars().first()
    if name:
        # Caminho para o log
        path = os.path.join(Settings().LOG, f'{name}.log')
        
        if os.path.isfile(path):
             return FileResponse(path=path,media_type="text/plain",filename=f"{name}.log")
        
        else:
            return HTTPStatus.NOT_FOUND
    
    else:
        return HTTPStatus.NOT_FOUND




