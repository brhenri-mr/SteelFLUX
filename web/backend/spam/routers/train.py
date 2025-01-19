from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy import select
from http import HTTPStatus
from spam.schemas import Training
from spam.database import get_session
from spam.models import Models
from uuid import uuid4
import logging.config
import logging
from settings import Settings
import os 

router = APIRouter(prefix='/train', tags=['Train'])


@router.post('/{model}/{version}')
def train(model:str, version:int, db: Training, session=Depends(get_session)):
    try:
        
        # Verificando se o modelo existe 
        path = session.execute(select(Models.path).where(Models.category == model).where(Models.version == version)).scalars().first()
        
        # Iniciando o identificador unico
        name_uuid = uuid4()
        
        # Caminho do log
        log_path = os.path.join(Settings().LOG,f'{name_uuid}.log')
        
        if path:
            # Configurando o log
            logging.basicConfig(
                filename=log_path,  # Salvar no arquivo com nome dinâmico
                level=logging.DEBUG,  # Nível de log
                format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
            )
            
            # Recuperando o caminho do modelo
            
            # Iniciando o treinamento
            
            # sistema de logs
            
            # Cadastrando novo modelo
            new_db = Models(uuid=name_uuid,
                            category=model,
                            name='1231',
                            status='',
                            versao=version+1,
                            )
            
            session.add(new_db)
            session.commit()
            session.refresh(new_db)
            
            return HTTPStatus.OK
        
        else:
            return HTTPStatus.NOT_FOUND
    
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.BAD_GATEWAY, detail=str(e))
