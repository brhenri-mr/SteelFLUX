from generator.elements import Plate, Conector, Beam, Column
from generator.connection import EndPLate
import pandas as pd
from generator.db import load_data
from uuid import uuid4

solicitacao = 120 # KN


saida = pd.DataFrame(columns=['Perfil', 'Chapa', 'Bitola','Material', 's', 'Parafuso', 'Block', 
                              'ShearPlate', 'PlateCrush', 'boltShear', 'webShear', 'FS'])

bitolas = [16, 20, 22 ,24 , 27 , 30, 36]


material = {'A36': {'fy':250, 'fu':400}, 
            'A527_GR50':{'fy':345, 'fu':450},
            'A527_GR55':{'fy':380, 'fu':485}}

viga = Beam(name='W 250 x 44,8' ,
            tw=7.6,
            tf=13*0.8, # So visual, com o 13 dica mto desproporcional
            h=240,
            bf=148,
            fy=345,
            fu=400)

coluna = Column(
      name='HP 310 x 79,0 (H)',
      h=140,
      tf=11,
      tw=11,
      bf=306,
)

#parafuso = Conector(d_b=16,  f_ub=825)

#chapa = Plate(name='CH 1/4"',c= 200,f_uc=250, f_yc=400)

#conexao = EndPLate(Conector=parafuso, Plate=chapa,Viga=viga,Coluna=coluna,n_ps=4 ,s=60, g_ch=120, dev_mode=False, uuid=uuid4())

#conexao.analyze(solicitacao)

#conexao.plotConnection()
#conexao.mask()
i= 0


for chapa_tipo in ['CH 1/4"','CH 3/16"', 'CH 5/16"', 'CH 3/8"', 'CH 1/2"', 'CH 5/8"', 'CH 3/4"', 'CH 7/8"' ]:
      for nome, materia_chapa in material.items():
            for element in bitolas:
                  i = 0
                  while True:
                        i += 1
                        try:
                              uuid = uuid4()
                              chapa = Plate(    name=chapa_tipo,
                                                c= 200,
                                                f_uc=materia_chapa['fu'],
                                                f_yc=materia_chapa['fy'])
                              
                              
                              print(f'Teste com {element} para {i*2} parafusos com chapa {chapa_tipo} {nome}')
                              parafuso = Conector(d_b=element,
                                                f_ub=825)
                              
                              conexao = EndPLate(Conector=parafuso,
                                          Plate=chapa,
                                          Viga=viga,
                                          Coluna=coluna,
                                          n_ps=2*i,
                                          s=element*3.01, # Garantir mais que o espaçamento mínimo,
                                          g_ch=120,
                                          dev_mode=False,
                                          uuid=uuid)
                            
                              # Veificando o dimensionamento 
                              dimensionamento = conexao.analyze(solicitacao)
                              if dimensionamento:
                                block, Vrd, F_vRd, F, web_shear = dimensionamento['blockShear'], dimensionamento['platShear'], dimensionamento['blotShear'], dimensionamento['plateCrush'][0], dimensionamento['beamWebShear']
                                FS = solicitacao/min(block, Vrd, F_vRd, F).magnitude
                                
                                ret = load_data(nome_perfil = 'W150x13',
                                            name = 'EndPlate',
                                            nome_chapa = chapa_tipo,
                                            bitola_parafuso = element,
                                            material_chapa = nome,
                                            distancia_s = 3.01*element, # Garantir mais que o espaçamento mínimo,
                                            qntd_parafusos = i*2,
                                            fs = FS,
                                            bolt_shear=F_vRd,
                                            block = block,
                                            shear_plate = Vrd,
                                            plate_crush = F,
                                            web_shear = web_shear,
                                            uuid=uuid,
                                            solicitacao=solicitacao,)
        
                                conexao.plotConnection()
                                conexao.mask()
                              
                        except AssertionError as e:
                              print(f'Falha em {element} para o conjunto com {i*2} parafusos')
                              print(f'{e}')
                              break
