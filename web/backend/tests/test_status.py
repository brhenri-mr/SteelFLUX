from http import HTTPStatus

def test_status_molde(client, model, session):
    response = client.get('/status')
    
    assert response.status_code == HTTPStatus.OK
    #assert response.json() == 1


def test_status_log(session, model, client):
    pass
    #models = '2'
    #name = '1'
    #versio = 1
    
    #response = client.get(f'/status/{models}/{name}/{versio}')
    #assert response.status_code == HTTPStatus.OK
    
