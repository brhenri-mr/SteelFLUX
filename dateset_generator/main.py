from gerdau.elements import Plate, Conector, Beam, Column
from gerdau.connection import EndPLate
import pandas as pd
from gerdau.db import load_data
from uuid import uuid4

solicitacao = 80 # KN


saida = pd.DataFrame(columns=['Perfil', 'Chapa', 'Bitola','Material', 's', 'Parafuso', 'Block', 
                              'ShearPlate', 'PlateCrush', 'boltShear', 'webShear', 'FS'])

bitolas = [16, 20, 22 ,24 , 27 , 30, 36]
material = {'A36': {'fy':250, 'fu':400}, 
            'A527_GR50':{'fy':345, 'fu':450},
            'A527_GR55':{'fy':380, 'fu':485}}

viga = Beam(name='W150x13',
            tw=4.3,
            tf=4.3,
            h=138,
            fy=345,
            fu=400)

coluna = Column(
      name='w',
      h=80,
      tf=4.3
)

parafuso = Conector(d_b=16,  f_ub=825)

chapa = Plate(name='CH 1/4"',c= 200,f_uc=250, f_yc=400)

#conexao = EndPLate(Conector=parafuso, Plate=chapa,Viga=viga,Coluna=coluna, n_ps=4 ,s=60, g_ch=120, dev_mode=False, uuid=uuid4())
#conexao.plotConnection(show=False)
#conexao.mask()

for chapa_tipo in ['CH 3/16"','CH 1/4"', 'CH 5/16"', 'CH 3/8"', 'CH 1/2"', 'CH 5/8"', 'CH 3/4"', 'CH 7/8"' ]:
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
                                          s=element*3.2,
                                          g_ch=120,
                                          dev_mode=False,
                                          uuid=uuid)
                                    
                              block = conexao.blockShear()
                              
                              Vrd = conexao.plateShear()

                              F, indv = conexao.plateCrush()

                              F_vRd = conexao.boltShear()

                              #web = conexao.beamWebShear()

                              FS = solicitacao/min(block, Vrd, F_vRd, F).magnitude
                              
                              ret = load_data(nome_perfil = 'W150x13',
                                          nome_chapa = chapa_tipo,
                                          bitola_parafuso = element,
                                          material_chapa = nome,
                                          distancia_s = 3.2*element,
                                          qntd_parafusos = i*2,
                                          fs = FS,
                                          bolt_shear=F_vRd,
                                          block = block,
                                          shear_plate = Vrd,
                                          plate_crush = F,
                                          web_shear = 0,
                                          uuid=uuid,
                                          solicitacao=solicitacao,)
      
                              conexao.plotConnection(show=False)
                              conexao.mask()
                              
                        except AssertionError as e:
                              print(f'Falha em {element} para o conjunto com {i*2} parafusos')
                              print(f'{e}')
                              break
