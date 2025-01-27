from pydantic import BaseModel
from datetime import datetime
from typing import List, Tuple

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
    
    # Quantidade de epocas
    epoch: int
    
    # Tamanho do bach
    
    bach_size: int
    
    # 1

class ModelAuth(BaseModel):
    
    # nome
    name: str
    
    # category
    category: str
    
    # 

class ImageMetadata(BaseModel):
    #Tensão de tração
    sigma:float
    
    # Cisalhamento
    tau:float
    
    #Viga
    section:str


class ModelsName(BaseModel):
    Name: List[Tuple[str, int]]
