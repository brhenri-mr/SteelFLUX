import os
from sqlalchemy import create_engine
import pandas as pd


class CustomeDataSet():
    def __init__(self, traindata_url, tipo_dados='EndPlate', transform=None, size=(768, 768), criterio='Image'):
        # Recuperando dados com dataframe --> Pelo visto é a melhor forma ...
        self.df = pd.read_sql(f"SELECT * FROM dados_table WHERE name='{tipo_dados}'", con=create_engine(f'sqlite:///{traindata_url}/database.db') )
        self.traindata_url = traindata_url # path da pasta com os dados
        self.nome_perfil = self.df['nome_perfil'] # Serie com os nome dos perfis
        self.solicitacao = self.df['solicitacao'] # Serie com as solicitacoes utilizadas
        self.img_uuid = self.df['uuid'] # Identificador unico da aplicação
        self.viga = self.df['nome_perfil']
        self.coluna = self.df['nome_perfil']
        self.chapa = self.df['nome_chapa']
        self.material = self.df['material_chapa']
        self.fs = self.df['fs']
        self.qntd_parafusos = self.df['qntd_parafusos']
        self.carregamento = self.df['solicitacao']
        self.bitola = self.df['bitola_parafuso']
        self.size = size # Tamanho padrão da imagem
        self.transform = transform # Transformações a serem aplicadas nas imagens
        self.criterio = criterio


    def __len__(self):
        return len(self.df)


    def __getitem__(self, index:int):
        
        if self.criterio == 'Image':
            # Recuperando uuid do elemento
            uuid_str = self.img_uuid[index]
            img_uuid = f"{uuid_str[:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:20]}-{uuid_str[20:]}"

            # Escrevendo o propmt da imagem
            
            caption = f'Complete the masked region on the left with the cross-sectional view, and the masked region on the right with the plan detail of a steel structural connection between an I-beam and an I-column, designed for a vertical load of {self.carregamento[index]} kN.Use the following information: seção viga: {self.viga[index]}, Bitola do parafuso: {self.bitola[index]}, quantidade de parafusos: {self.qntd_parafusos[index]}, FS: {self.fs[index]}. Use technical representation according to structural drawing standards, including visible profiles, bolts, and connection plates.'


            return caption, img_uuid
        else:
            
            espessuras_chapas = {
    'CH 1/4"': 6.35,
    'CH 3/16"': 4.76,
    'CH 5/16"': 7.94,
    'CH 3/8"': 9.52,
    'CH 1/2"': 12.70,
    'CH 5/8"': 15.88,
    'CH 3/4"': 19.05,
    'CH 7/8"': 22.23
            }
            
            name_corretion = {'A36':'A36',
                              'A527_GR55':'A572_GR55',
                              'A527_GR50':'A572_GR50'}
            
            return (name_corretion[self.material[index]],
                    espessuras_chapas[self.chapa[index]],
                    self.qntd_parafusos[index],
                    self.bitola[index],
                    self.fs[index])