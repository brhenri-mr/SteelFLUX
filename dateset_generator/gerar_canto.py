from generator.elements import Plate, Conector, Beam, Column, CornerFrame
from generator.connection import EndPLate, LCPP
import pandas as pd
from generator.db import load_data
from uuid import uuid4

solicitacao = 50 # KN


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

cantoneira = CornerFrame(t_ch=3.18,
                             f_yc=345,
                             f_uc=400,
                             lc=120.8)


"""lcpp = LCPP(
        Viga=viga,
        Coluna=coluna,
        Angle=cantoneira,
        n_ps=6,
        uuid=uuid4(),
        s=48,
        Conector=parafuso,
        dev_mode=True
    )
    
lcpp.analyze(solicitacao)"""
#lcpp.plotConnection(show=True)
#lcpp.mask()

"""
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
"""