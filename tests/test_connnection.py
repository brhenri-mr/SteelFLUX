from gerdau.connection import EndPLate
from gerdau.elements import Column, Conector, Beam, Plate


chapa = Plate(t_ch=6.3,
              c= 200,
              f_uc=400,
              f_yc=250)

parafuso = Conector(d_b=15.875,
                    f_ub=825)

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

conexao = EndPLate(Conector=parafuso,
                   Plate=chapa,
                   Viga=viga,
                   Coluna=coluna,
                   n_ps=6,
                   s=60,
                   g_ch=120)


def test_blockShear():
    '''
    Função para test do blockshear na conexão
    '''
    
    assert conexao.blockShear().magnitude == 11231, 'Valor de BlockShear está errado'
    


def test_plateShear():
    '''
    Função para test do plateShear
    '''
    
    assert conexao.plateShear().magnitude == 11231, 'Valor de plateShear está errado'
    


def test_plateBearing():
    '''
    Função para test do plateBearing
    '''
    
    assert conexao.plateBearing().magnitude == 11231, 'Valor de plateBearing está errado'


def test_plateCrush():
    '''
    Função para test do plateCrush
    '''
    
    assert conexao.plateCrush().magnitude == 11231, 'Valor de plateCrush está errado'


def test_boltShear():
    '''
    Função para test do boltShear
    '''
    
    assert conexao.boltShear().magnitude == 11231, 'Valor de boltShear está errado'


def test_beamWebShear():
    '''
    Função para test do beamWebShear
    '''
    
    assert conexao.beamWebShear().magnitude == 11231, 'Valor de beamWebShear está errado'
