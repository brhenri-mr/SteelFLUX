from datetime import datetime
from sqlalchemy.orm import registry, Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey
from datetime import datetime
from typing import List


table_registry = registry() 


@table_registry.mapped_as_dataclass
class Modelos():
    __tablename__ = 'modelos_table'
    __table_args__ = {'quote': True}


    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # name
    name: Mapped[str]
    
    # Status
    status: Mapped[str]

    #Category
    category: Mapped[str]
    
    # Versão desse modelo
    version: Mapped[str]

    # Path do modelo no minIO
    storage_path: Mapped[str]

    # Tipo do arquivo de salvamento
    extension: Mapped[str]

    # Descrição
    description: Mapped[str]

    training_id: Mapped[int] = mapped_column(ForeignKey('experimentos_table.id'), init=False, nullable=True)

    uuid: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class MetadadosExperimentos():
    __tablename__ = 'experimentos_table'
    __table_args__ = {'quote': True}


    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Status do treinamento do modelo
    status:Mapped[str]

    model: Mapped['Modelos'] = relationship(init=False)

    hiperparmetro: Mapped[List['Hiperparametros']] = relationship(init=False)


@table_registry.mapped_as_dataclass
class Hiperparametros():
    __tablename__ = 'hiperparametros_table'
    __table_args__ = {'quote': True}
    
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_metadados = mapped_column(ForeignKey('experimentos_table.id'), init=False)
    nome: Mapped[str]
    valor: Mapped[float]

