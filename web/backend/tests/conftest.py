import pytest
from fastapi.testclient import TestClient
from spam.app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from spam.models import table_registry
from spam.database import get_session
from spam.models import Modelos
from uuid import uuid4


@pytest.fixture()
def client(session):
    def get_session_override():
        return session
    
    # Reescrevendo o sql em tempo de injeção -> ele altera para poder usar o banco de dados de teste
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    # Criando o banco de dados em memoria
    engine = create_engine('sqlite:///:memory:',
                           connect_args={'check_same_thread':False}, # nao verifica se tudo esta em uma thread,
                           poolclass=StaticPool)

    # Criando o banco de dados em memoria
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session 

    # Deletando os dados em memoria -> tear down
    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def model(session):

    model = Modelos(status='Train',
                    name='Test',
                    category='Flux',
                    version='v0',
                    storage_path='hhtp',
                    extension='.pkl',
                    description='Opa sou um test',
                    uuid=str(uuid4()))

    session.add(model)
    session.commit()
    session.refresh(model)

    return model
