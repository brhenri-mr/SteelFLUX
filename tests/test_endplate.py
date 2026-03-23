
# Eles todos tem a mesma taxa de erro de 0,8 % muito estranho --> Era a espessura da chapa eu considerei como sendo 6.3 nas contas a mão
# e no programa está como 6.35 e da examente essa difrerença em porcentagem
def test_blockShear(conexao):
    '''
    Função para test do blockshear na conexão
    '''
    tol = 10E-3
    assert abs(conexao.blockShear().magnitude - 309.50) < 10E-3, f'Valor de BlockShear está errado {conexao.blockShear().magnitude}'

    

def test_plateShear(conexao):
    '''
    Função para test do plateShear
    '''
    tol = 10E-3
    assert abs(conexao.plateShear().magnitude - 207.433)<tol, f'Valor de plateShear está errado {conexao.plateShear().magnitude}'
    

"""
def test_plateBearing():
    '''
    Função para test do plateBearing
    '''
    
    assert conexao.plateBearing().magnitude == 11231, 'Valor de plateBearing está errado'

"""
def test_plateCrush(conexao):
    '''
    Função para test do plateCrush
    '''
    tol = 10E-3
    assert abs(conexao.plateCrush()[0].magnitude - 171.87) < tol, f'Valor de plateCrush está errado {conexao.plateCrush()[0].magnitude}'


def test_boltShear(conexao):
    '''
    Função para test do boltShear
    '''
    tol = 10E-3
    assert abs(conexao.boltShear().magnitude - 290.30) < tol, f'Valor de boltShear está errado {conexao.boltShear().magnitude}'


def test_beamWebShear(conexao):
    '''
    Função para test do beamWebShear
    '''
    tol = 10E-3
    assert abs(conexao.beamWebShear().magnitude - 121.377)<tol, f'Valor de beamWebShear está errado {conexao.beamWebShear().magnitude}'

