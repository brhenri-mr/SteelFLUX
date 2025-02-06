from http import HTTPStatus
from sqlalchemy import select
from spam.models import Modelos


def test_category_recive(session, client, model):
    
    models_category = session.execute(select(Modelos.category)).scalar()
    
    response = client.get(f'/model/{models_category}')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()

    
    


