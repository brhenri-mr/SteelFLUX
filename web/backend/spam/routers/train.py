from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy import select
from http import HTTPStatus
from spam.schemas import Training
from spam.database import get_session
from spam.models import Modelos
from uuid import uuid4
import logging.config
import logging
from settings import Settings
import os 
from spam.utils.log import log_init

router = APIRouter(prefix='/train', tags=['Train'])


@router.post('/{model}/{name}/{version}')
async def train(model:str,name:str, version:int, db: Training, session=Depends(get_session)):
    try:
        
        # Verificando se o modelo existe 
        modelo = session.execute(select(Modelos).where(Modelos.category == model).where(Modelos.name == name).where(Modelos.versao == version)).scalars().first()
        
        # Iniciando o identificador unico
        name_uuid = uuid4()
        
        # Caminho do log
        log_path = os.path.join(Settings().LOG,f'{name_uuid}.log')
        
        log_init(version = version+1,
                 category=model,
                 nome=name,
                 hip=db,
                 uuid=name_uuid,
                 path=log_path)
        
        if modelo:
            # Configurando o log
            logging.basicConfig(
                filename=log_path,  # Salvar no arquivo com nome dinâmico
                level=logging.DEBUG,  # Nível de log
                format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
            )
            
            # Recuperando o caminho do modelo
            
            # Iniciando o treinamento
            logging.info("O treinamento foi iniciado.")
            
            logging.info("Registrando novo modelo")
            # Cadastrando novo modelo
            new_db = Modelos(uuid=name_uuid,
                            category=model,
                            name=name,
                            status='idle',
                            storage_path='hhtp',
                            extension='.pkg',
                            description='Gerador de imagens',
                            versao=f'v.{version+1}',
                            )
            
            session.add(new_db)
            session.commit()
            session.refresh(new_db)
            
            logging.info("Treinamento finalizado com sucesso")
            return HTTPStatus.OK
        
        else:
            return HTTPStatus.NOT_FOUND
    
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.BAD_GATEWAY, detail=str(e))
