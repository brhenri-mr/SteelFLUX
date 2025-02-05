from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from sqlalchemy import select
from spam.schemas import ModelAuth
from spam.models import Models
from uuid import uuid4
from spam.database import get_session

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/')
async def cadastro(db: ModelAuth, session=Depends(get_session)):
    try:
        new_db = Models(uuid=uuid4(),
                        name=db.name,
                        category=db.category,
                        versao=0,
                        status='idle'
                        )
        
        session.add(new_db)
        session.commit()
        session.refresh(new_db)
        
        return new_db
    
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.BAD_GATEWAY, detail=str(e))
