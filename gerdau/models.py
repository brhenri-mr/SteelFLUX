from sqlalchemy.orm import registry, Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey
from datetime import datetime
from uuid import UUID

table_registry = registry()

@table_registry.mapped_as_dataclass
class Dados():
        
    __tablename__ = 'dados_table'
    __table_args__ = {'quote': True}  # Indica que o nome da tabela deve ser tratado com aspas duplas
    
    # id
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    
    # Identificador unico
    uuid: Mapped[UUID]
    
    # Nome do perfil
    nome_perfil: Mapped[str]
    
    # Nome da chapa
    nome_chapa: Mapped[str]
    
    # Diametro ou bitola do parafuso mm
    bitola_parafuso: Mapped[int]
    
    # Material
    material_chapa: Mapped[str]
    
    # Distância entre parafusos
    distancia_s: Mapped[float]
    
    # Quantidade de parafusos
    qntd_parafusos: Mapped[int]
    
    # Solicitacao
    solicitacao:Mapped[float]
    
    # Fator de segurança
    fs: Mapped[float]
    
    stress: Mapped['Stress'] = relationship() 


@table_registry.mapped_as_dataclass
class Stress():
    
    __tablename__ = 'stress_table'
    __table_args__ = {'quote': True}  # Indica que o nome da tabela deve ser tratado com aspas duplas
    
    id:Mapped[int] = mapped_column(init=False, primary_key=True)
    
    uuid: Mapped[UUID] = mapped_column(ForeignKey('dados_table.uuid'))
    
    block:Mapped[float] = mapped_column(nullable=True)
    
    shear_plate:Mapped[float] = mapped_column(nullable=True)
    
    plate_crush:Mapped[float] = mapped_column(nullable=True)
    
    bolt_shear:Mapped[float] = mapped_column(nullable=True)
    
    web_shear:Mapped[float] = mapped_column(nullable=True)
