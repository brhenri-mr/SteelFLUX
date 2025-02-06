from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from sqlalchemy import select
from spam.schemas import ModelAuth
from spam.models import Modelos
from uuid import uuid4
from spam.database import get_session

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/')
async def cadastro(db: ModelAuth, session=Depends(get_session)):
    try:
        new_db = Modelos(uuid=str(uuid4()),
                        name=db.name,
                        category=db.category,
                        version=db.version,
                        status=db.status,
                        storage_path=db.storage_path,
                        extension=db.extension,
                        description=db.description,
                        )
        
        session.add(new_db)
        session.commit()
        session.refresh(new_db)
        
        return new_db
    
    except Exception as e:
        session.rollback()
        return HTTPException(status_code=HTTPStatus.BAD_GATEWAY, detail=str(e))
