import pandas as pd
import os 
from gerdau.unit import unit


def perfil_gerdau_W(name,path, Dimension_unit='millimeter', ):
    '''
    Função que retorna as caracteristicas geométrica de um perfil. As caracteristicas
    geométricas retornas são Massa linear, Altura da seção (d), largura do flange (bf),
    espessura da alma (tw), espessura do flange (tf), altura da alma (h)
    
    Parametrs
    ---------
    * name: str
        Nome do perfil conforme banco de dados
    * path: str
        Caminho para o local dos dados
    * Dimension_unit: str
        Unidade dimensionais das caracteristicas do perfil segundo o banco de dados
    
    Return
    ------
    Dicionário com os valores das características 
    '''
    
    dados = pd.read_excel(os.path.join(path, 'Perfis.xlsx'))
    features = dados[dados['BITOLA'] == name]
    features = features.to_dict()

    for chave in features.keys():
        for key, value in features[chave].items():
            if isinstance(value, str) or value == 'BITOLA':
                features[chave] = value
            else:
                features[chave] = value*unit[Dimension_unit]
    return features


if __name__ == '__main__':
    name = "W 150 x 13,0"
    
    PATH = os.path.join(os.getcwd(), 'gerdau', 'Dados')
    
    print(perfil_gerdau_W(name, path=PATH))
