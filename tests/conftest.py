import pytest
from generator.elements import Column, Conector, Beam, Plate, CornerFrame
from generator.connection import EndPLate, LCPP
from uuid import uuid4


@pytest.fixture()
def chapa():
    chapa = Plate(name='CH 1/4"',
              c= 200,
              f_uc=400,
              f_yc=345)
    return chapa


@pytest.fixture()
def parafuso():
    parafuso = Conector(d_b=15.875,
                    f_ub=825)
    return parafuso


@pytest.fixture()
def coluna():
    coluna = Column(
      name='w',
      tw=4.3,
      bf=200,
      h=80,
      tf=4.3
    )

    return coluna


@pytest.fixture()
def viga():
    viga = Beam(name='W150x13',
            bf=200,
            tw=4.3,
            tf=4.3,
            h=150,
            fy=345,
            fu=400)
    return viga


@pytest.fixture()
def conexao(parafuso, chapa, viga, coluna):
    conexao = EndPLate(Conector=parafuso,
                    Plate=chapa,
                    Viga=viga,
                    Coluna=coluna,
                    n_ps=6,
                    s=60,
                    g_ch=120,
                    uuid=uuid4())
    return conexao

1
def cantoneira():
    # Cadastrando um 2L 1/2"
    cantoneira = CornerFrame(t_ch=3.18,
                             f_yc=345,
                             f_uc=400,
                             lc=12.7)
    return cantoneira


def lcpp(cantoneira, coluna, viga, parafuso):
    
    lcpp = LCPP(
        Viga=viga,
        Coluna=coluna,
        Angle=cantoneira,
        n_ps=4,
        s=60,
        Conector=parafuso
    )
    
    return lcpp
