from torch.utils.data import Dataset
import os 
from sqlalchemy import create_engine
import pandas as pd
from diffusers.utils import load_image

class CustomeDataSet(Dataset):
    def __init__(self, traindata_url:str, transform=None, size=(768, 768)):
        # Recuperando dados com dataframe --> Pelo visto é a melhor forma ...
        self.df = pd.read_sql("SELECT * FROM dados_table", con=create_engine('sqlite:///database.db') )
        self.traindata_url = traindata_url # path da pasta com os dados
        self.nome_perfil = self.df['nome_perfil'] # Serie com os nome dos perfis
        self.solicitacao = self.df['solicitacao'] # Serie com as solicitacoes utilizadas
        self.img_uuid = self.df['uuid'] # Identificador unico da aplicação
        self.size = size # Tamanho padrão da imagem
        
        
    def __len__(self):
        return len(self.df)
    
    
    def __getitem__(self, index):
        
        # Recuperando uuid do elemento
        img_uuid = self.img_uuid[index]
        
        # Carregando as imagens 
        img_root_url = os.path.join(self.traindata_url, 'img', f'{img_uuid}.png')
        img_mask_root = os.path.join(self.traindata_url, 'mask', f'{img_uuid}.png')
        img_raw_root = os.path.join(self.traindata_url, 'raw', f'{img_uuid}.png')

        # Padronização das imagens
        img_root = load_image(img_root_url).convert("RGB").resize(self.size)
        img_mask = load_image(img_mask_root).convert("RGB").resize(self.size)
        img_raw = load_image(img_raw_root).convert("RGB").resize(self.size)
    
        # Escrevendo o propmt da imagem
        caption = f'flexible steel connection between a steel column and a steel beam {self.nome_perfil[index]} with a load of {self.solicitacao[index]} kN'
        
        # Aplicando alguma transformação as imagens
        if self.transform:
            img_root = self.transform(img_root)
            img_mask = self.transform(img_mask)
            img_raw = self.transform(img_raw)
            
        return caption, img_root, img_mask, img_raw
