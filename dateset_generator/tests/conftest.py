import pytest
from generator.elements import Column, Conector, Beam, Plate
from generator.connection import EndPLate
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
      h=80,
      tf=4.3
    )

    return coluna


@pytest.fixture()
def viga():
    viga = Beam(name='W150x13',
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
