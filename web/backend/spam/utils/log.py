from datetime import datetime
from uuid import UUID, uuid4
from settings import Settings
import os 

def log_init(version:int, category:str, nome:str, hip:dict, uuid:UUID, path:str):
    '''
    Função para inicialização do arquivo arquivo padrão de log com cabeaçalho
    
    Parameters
    ----------
    * version: versão do modelo
    
    * category: categoria do modelo 
    
    * nome: nome do modelo

    * hip: hiperparâmetros do modelo
    
    * uuid: identificador unico do modelo
    
    * path: caminho para salvamento do log
    
    '''
    
    # Criar o cabeçalho padrão
    header = "=== INÍCIO DO LOG ===\n"
    header += f"Model: {category} {nome}.v0{version}\n"
    header += f'id: {uuid}\n'
    header += "Data: {:%Y-%m-%d %H:%M:%S}\n".format(datetime.now())
    header += "Hipeparâmteros:\n"
    
    for chave, valor in dict(hip).items():
        header += f'{chave}: {valor}\n'
    
    header += "=" * 40 + "\n"
        
    with open(path, 'w') as arquivo:
        arquivo.write(header)
    
    return 1

if __name__ == '__main__':
    log_init(version=1,
             category='Gan',
             nome='Test',
             hip={'epoch':100},
             uuid=uuid4(),
             path='')  
