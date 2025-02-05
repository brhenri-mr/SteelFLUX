from http import HTTPStatus
from sqlalchemy import select
from spam.models import Models


def test_register(session, client, model):
    
    models_name = session.execute(select(Models.category)).scalar()
    
    response = client.get(f'/model/{models_name}')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()

    
    


