from http import HTTPStatus
from sqlalchemy import select
from spam.models import Models


def test_register(session, client):
    response = client.post(f'/auth/', 
                json={
                    'name': 'Test',
                    'category':'Flux'
                })
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()
    assert session.execute(select(Models)).scalar()
    
    


