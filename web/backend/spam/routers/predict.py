from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from http import HTTPStatus
from spam.models import Models
from sqlalchemy import select
from spam.database import get_session
import os 
from settings import Settings
from spam.schemas import ImageMetadata

# importando modelos
from spam.iamodels.FLUXControlnetInpainting.main import fluxInpaintinRun


router = APIRouter(prefix='/predict', tags=['predict'])

@router.post('/{model}/{name}/{version}')
async def predict(model:str, 
                  name:str, 
                  version:int, 

                  session=Depends(get_session),
                  file:UploadFile = File(...)):
    '''
    Endpoint para predizer uma imagem
    '''
    try:
        
        # Contexto para LLM
        #context = f'''sigma={metadados.sigma}, tau={metadados.tau}, perfil={metadados.section}'''
        
        # Verificando se o modelos existe
        date = session.execute(select(Models).where(Models.name == name)).scalars().first()
        
        
        # Fazendo as verificações
        if date:
            # Retornar a msg
            match name:
                case 'FLUXControlnetInpainting':
                    pass
                    
            return 1
        
        else:
            return HTTPException(HTTPStatus.NOT_FOUND)
        
    except:
        return HTTPException(HTTPStatus.BAD_REQUEST)
    
    