from generator.elements import Plate, Conector, Beam, Column, CornerFrame
from generator.connection import EndPLate, LCPP
import pandas as pd
from generator.db import load_data
from uuid import uuid4
from generator.unit import unit

solicitacao = 50 # KN


saida = pd.DataFrame(columns=['Perfil', 'Chapa', 'Bitola','Material', 's', 'Parafuso', 'Block', 
                              'ShearPlate', 'PlateCrush', 'boltShear', 'webShear', 'FS'])

bitolas = [16, 20, 22 ,24 , 27 , 30]
material = {'A36': {'fy':250, 'fu':400}, 
            'A527_GR50':{'fy':345, 'fu':450},
            'A527_GR55':{'fy':380, 'fu':485}}

cantoneira_dados = {
    "8”": [
        {"b_mm": 203.2, "peso_kg_m": 48.7, "t_pol": "5/8”", "t_mm": 15.88},
        {"b_mm": 203.2, "peso_kg_m": 57.9, "t_pol": "3/4”", "t_mm": 19.05},
    ],
    "3”": [
        {"b_mm": 76.2, "peso_kg_m": 5.52, "t_pol": "3/16”", "t_mm": 4.76},
        {"b_mm": 76.2, "peso_kg_m": 7.29, "t_pol": "1/4”", "t_mm": 6.35},
        {"b_mm": 76.2, "peso_kg_m": 9.07, "t_pol": "5/16”", "t_mm": 7.94},
        {"b_mm": 76.2, "peso_kg_m": 10.71, "t_pol": "3/8”", "t_mm": 9.52},
        {"b_mm": 76.2, "peso_kg_m": 14.0, "t_pol": "1/2”", "t_mm": 2.7},
    ],
    "3.1/2”": [
        {"b_mm": 88.9, "peso_kg_m": 8.56, "t_pol": "1/4”", "t_mm": 6.35},
        {"b_mm": 88.9, "peso_kg_m": 10.59, "t_pol": "5/16”", "t_mm": 7.94},
        {"b_mm": 88.9, "peso_kg_m": 12.58, "t_pol": "3/8”", "t_mm": 9.52},
    ],
    "4”": [
        {"b_mm": 101.6, "peso_kg_m": 9.81, "t_pol": "1/4”", "t_mm": 6.35},
        {"b_mm": 101.6, "peso_kg_m": 12.19, "t_pol": "5/16”", "t_mm": 7.94},
        {"b_mm": 101.6, "peso_kg_m": 14.57, "t_pol": "3/8”", "t_mm": 9.52},
        {"b_mm": 101.6, "peso_kg_m": 16.8, "t_pol": "7/16”", "t_mm": 11.11},
        {"b_mm": 101.6, "peso_kg_m": 19.03, "t_pol": "1/2”", "t_mm": 12.7},
    ],
    "5”": [
        {"b_mm": 127, "peso_kg_m": 12.34, "t_pol": "1/4”", "t_mm": 6.35},
        {"b_mm": 127, "peso_kg_m": 15.31, "t_pol": "5/16”", "t_mm": 7.94},
        {"b_mm": 127, "peso_kg_m": 18.3, "t_pol": "3/8”", "t_mm": 9.52},
        {"b_mm": 127, "peso_kg_m": 24.1, "t_pol": "1/2”", "t_mm": 1.27},
        {"b_mm": 127, "peso_kg_m": 29.8, "t_pol": "5/8”", "t_mm": 15.88},
        {"b_mm": 127, "peso_kg_m": 23.52, "t_pol": "7/16”", "t_mm": 11.11},
    ],
    "6”": [
        {"b_mm": 152.4, "peso_kg_m": 22.2, "t_pol": "3/8”", "t_mm": 9.52},
        {"b_mm": 152.4, "peso_kg_m": 29.2, "t_pol": "1/2”", "t_mm": 12.7},
        {"b_mm": 152.4, "peso_kg_m": 36.0, "t_pol": "5/8”", "t_mm": 15.88},
        {"b_mm": 152.4, "peso_kg_m": 42.7, "t_pol": "3/4”", "t_mm": 19.05},
    ]
}



viga = Beam(name='W150x13',
            tw=4.3,
            tf=4.3,
            h=138,
            bf=80,
            fy=345,
            fu=400)

coluna = Column(
      name='w',
      h=80,
      tf=4.3,
      tw=4.3,
      bf=250,
)

parafuso = Conector(d_b=16,  f_ub=825)

"""
cantoneira = CornerFrame(t_ch=6.13,
                                                        f_yc=345,
                                                        f_uc=400,
                                                        lc=120)


lcpp = LCPP(
        Viga=viga,
        Coluna=coluna,
        Angle=cantoneira,
        n_ps=6,
        uuid=uuid4(),
        s=48,
        Conector=parafuso,
        dev_mode=True
    )
    
lcpp.analyze(solicitacao)
lcpp.plotConnection(show=True)
lcpp.mask()
"""

for el in cantoneira_dados.keys():
    for el_coner in cantoneira_dados[el]:
      for nome, materia_chapa in material.items():
            for element in bitolas:
                  i = 0
                  while True:
                        i += 1
                        try:
                              uuid = uuid4()
                              cantoneira = CornerFrame(t_ch=el_coner['t_mm'],
                                                        f_yc=345,
                                                        f_uc=400,
                                                        lc=el_coner['b_mm'])

                              print(f'Teste com ø={element}mm para {i} parafusos com cantoneira 2xL{el}x{el_coner['t_mm']} {nome}')
                              parafuso = Conector(d_b=element,
                                                f_ub=825)
                              
                              conexao = LCPP(
                                                    Viga=viga,
                                                    Coluna=coluna,
                                                    Angle=cantoneira,
                                                    n_ps=2*i, # O valor 2 multiplicado é uma correção, o código foi feito para a chapa de fundo que é simétrica. Então quando eu coloc n_ps*2 o código divide por 2. Então fica um
                                                    uuid=uuid,
                                                    s=element*3.01,
                                                    dev_mode=False,
                                                    Conector=parafuso,
                                                )
                              
                              dimensionamento = conexao.analyze(solicitacao)
                              
                              if dimensionamento:
                                Vrd, F_vRd, F, web_shear = dimensionamento['platShear'], dimensionamento['blotShear'], dimensionamento['plateCrush'][0], dimensionamento['beamWebShear']
                                FS = solicitacao/min(Vrd, F_vRd, F).magnitude
                                ret = load_data(nome_perfil = 'W150x13',
                                            name='LLCP',
                                            nome_chapa = f'2xL{el}x{el_coner['t_mm']} {nome}',
                                            bitola_parafuso = element,
                                            material_chapa = nome,
                                            distancia_s = 3.01*element,
                                            qntd_parafusos = i,
                                            fs = FS,
                                            bolt_shear=F_vRd,
                                            block = 0*unit['millimeter'],
                                            shear_plate = Vrd,
                                            plate_crush = F,
                                            web_shear = web_shear,
                                            uuid=uuid,
                                            solicitacao=solicitacao,)
                                conexao.plotConnection()
                                conexao.mask()
                              
                        except AssertionError as e:
                            print('*'*20)
                            #print(f'Falha em {element} para o conjunto com {i*2} parafusos')
                            #print(f'{e}')
                            break
