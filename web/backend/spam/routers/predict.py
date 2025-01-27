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
async def predict(model: str, 
                  name: str, 
                  version: int, 
                  session = Depends(get_session), 
                  file: UploadFile = File(...)):
    '''
    Endpoint para predizer uma imagem
    '''
    try:
        # Verificando se o modelo existe
        db_uuid = session.execute(select(Models.uuid).where(Models.name == name)).scalars().first()
        
        # Fazendo as verificações
        if db_uuid:
            # Exemplo de chamada de função dependendo do nome
            match name:
                case 'FLUXControlnetInpainting':
                    ret, path = fluxInpaintinRun(image_path=1, mask_path=1, prompt=1, uuid=db_uuid)
                    # Aqui você pode retornar o que for relevante, por exemplo, o resultado da predição
                    return {"status": "success", "result": ret, "path": path}
                
            # Caso o nome não seja reconhecido
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Modelo não reconhecido")
         
        else:
            # Se o modelo não for encontrado no banco de dados
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Modelo não encontrado")
        
    except Exception as e:
        # Captura qualquer exceção e retorna uma resposta de erro
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    