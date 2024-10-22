from gerdau.connection import EndPLate
from gerdau.elements import Column, Conector, Beam, Plate

chapa = Plate(t_ch=6.3,
              c= 200,
              f_uc=400,
              f_yc=345)

parafuso = Conector(d_b=15.875,
                    f_ub=825)

viga = Beam(name='W150x13',
            tw=4.3,
            tf=4.3,
            h=150,
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
    tol = 10E-3
    assert conexao.blockShear
    ().magnitude - 307.0667 < 10E-3, 'Valor de BlockShear está errado'

    

def test_plateShear():
    '''
    Função para test do plateShear
    '''
    assert conexao.plateShear().magnitude == 205.8, 'Valor de plateShear está errado'
    

"""
def test_plateBearing():
    '''
    Função para test do plateBearing
    '''
    
    assert conexao.plateBearing().magnitude == 11231, 'Valor de plateBearing está errado'

"""
def test_plateCrush():
    '''
    Função para test do plateCrush
    '''
    tol = 10E-3
    assert abs(conexao.plateCrush()[0].magnitude - 170.52) < tol, 'Valor de plateCrush está errado'

test_plateCrush()
def test_boltShear():
    '''
    Função para test do boltShear
    '''
    tol = 10E-3
    assert abs(conexao.boltShear().magnitude - 290.30) < tol, f'Valor de boltShear está errado {conexao.boltShear().magnitude}'


def test_beamWebShear():
    '''
    Função para test do beamWebShear
    '''
    tol = 10E-3
    assert abs(conexao.beamWebShear().magnitude - 121.377)<tol, 'Valor de beamWebShear está errado'

