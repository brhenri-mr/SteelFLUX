from sqlalchemy.orm import registry, Mapped, mapped_column, relationship
from sqlalchemy import func, Table, Column, ForeignKey, Enum
from datetime import datetime
from typing import List
from uuid import UUID

table_registry = registry()


@table_registry.mapped_as_dataclass
class Models():
    '''
    Tabela com as informações do usuário
    '''
    __tablename__ = 'models_table'
    __table_args__ = {'quote': True}  # Indica que o nome da tabela deve ser tratado com aspas duplas
    
    # id
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    
    # Identificador de imagem
    uuid: Mapped[UUID]
    
    # Nome 
    name: Mapped[str]
    
    # Classe do modelo  
    category: Mapped[str] 
    
    # Status
    status: Mapped[str]
    
    # Versão
    versao: Mapped[int]
    
    # Caminho do arquivo
    path: Mapped[str]


