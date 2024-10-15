import matplotlib.pyplot as plt


def breakline(start,cota,length=100):
    '''
    Função para geração dos valores de pontos de uma 
    break-line

    Parameters
    ----------
    start : float
        Ponto de incio da breakLine.
    cota : float
        Altura da linha de breakline.
    length : float, optional
        Comprimento da linha. The default is 100.

    Returns
    -------
    coord : list
        Coordenadas da breakline.

    '''

    coord = [[start, cota], 
             [length/2 - 2, cota], 
             [length/2, cota - 1.5], 
             [length/2, cota + 1.5], 
             [length/2 + 2, cota], 
             [length, cota]]
    
    return coord





