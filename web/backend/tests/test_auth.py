from http import HTTPStatus
from sqlalchemy import select
from spam.models import Modelos
from uuid import uuid4

def test_register(session, client):
    
    response = client.post(f'/auth/', 
                json={
                    'name': 'Test',
                    'category':'Flux',
                    'status':'Idle',
                    'storage_path':'1231',
                    'extension':'.pk',
                    'description':'Sou um test',
                    'version':'v.01'
                })
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()
    assert session.execute(select(Modelos)).scalar()
    
    


