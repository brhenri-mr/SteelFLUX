from .models import Dados
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from settings import Settings


def load_data(nome_perfil:str,
              nome_chapa:str,
              bitola_parafuso:int,
              material_chapa:str,
              distancia_s:float,
              qntd_parafusos:int,
              fs:float):
    '''
    Função que carrega os dados para o banco de dados SQL
    
    Return:
    ------
     - True - Tudo certo
     - False - Deu errado
    '''
    try:
        # Novo banco de dados
        new_db = Dados(nome_perfil=nome_perfil,
                    nome_chapa=nome_chapa,
                    bitola_parafuso=bitola_parafuso,
                    material_chapa=material_chapa,
                    distancia_s=distancia_s,
                    qntd_parafusos=qntd_parafusos,
                    fs=fs)
        
        with Session(create_engine(Settings().DATABASE_URL)) as session:
            session.add(new_db)
            session.commit()
            session.refresh(new_db)
    
        return True
    
    except: 
        return False
