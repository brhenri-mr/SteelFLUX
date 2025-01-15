from .models import Dados, Stress
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from settings import Settings
from uuid import UUID

def load_data(nome_perfil:str,
              nome_chapa:str,
              bitola_parafuso:int,
              material_chapa:str,
              distancia_s:float,
              qntd_parafusos:int,
              fs:float,
              block:float,
              shear_plate:float,
              plate_crush:float,
              bolt_shear:float,
              web_shear:float,
              uuid:UUID,
              solicitacao:float):
    '''
    Função que carrega os dados para o banco de dados SQL
    
    Return:
    ------
     - True - Tudo certo
     - False - Deu errado
    '''
    
    try:
        # Dados de tensão
        new_stress = Stress(block=block.magnitude,
                            shear_plate = shear_plate.magnitude,
                            plate_crush = plate_crush.magnitude,
                            bolt_shear=bolt_shear.magnitude,
                            web_shear=web_shear,
                            uuid=uuid
                            )
        
        # Novo banco de dados
        new_db = Dados(nome_perfil=nome_perfil,
                    nome_chapa=nome_chapa,
                    bitola_parafuso=bitola_parafuso,
                    material_chapa=material_chapa,
                    distancia_s=distancia_s,
                    qntd_parafusos=qntd_parafusos,
                    fs=fs,
                    uuid=uuid,
                    stress=new_stress,
                    solicitacao=solicitacao
                    )
        
        with Session(create_engine(Settings().DATABASE_URL)) as session:
            session.add(new_db)
            session.commit()
            session.refresh(new_db)
    
        return True
    
    except Exception as e: 
        return e
