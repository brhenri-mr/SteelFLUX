from pydantic import BaseModel
from datetime import datetime

class TrainingDate(BaseModel):
    # mensagem de treino
    msg: str
    
    # Modelo sendo treinado
    model: str
    
    # Tempo treinando
    time: str
    
    # Comeco do treinamento
    data: datetime

    # Quantidade ja concluida do treinamento
    percentage: str
    
    # Epoca atual
    epoch: int
    
    # Status do treinamento
    status: int

class Training(BaseModel):
    
    # Name
    name: str
    
    # Quantidade de epocas
    epoch: int
    
    # Tamanho do bach
    
    bach_size: int
    
    # 1
