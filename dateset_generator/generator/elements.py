from generator.unit import unit


class Beam:
    def __init__(self,
                 name:str,
                 h:float,
                 tw:float,
                 tf:float,
                 fy:float,
                 fu:float,
                 bf:float,
                 Resistence_unit='megapascal',
                 Dimension_unit='millimeter') -> None:
        '''
        Parameters
        ----------
        
        * tw: float
                Espessura da chapa
        * tf: float
                Espessura do flange
        * h: float
                Altura da alma do perfil
        * fy: float
                Resistência a escoamento da chapa
        * fu: float
                Resistência a ruptura da chapa
        * bf: float
                Comprimento do flange
        '''
        self.name = name
        self.h = h*unit[Dimension_unit]
        self.tw = tw*unit[Dimension_unit]
        self.tf = tf*unit[Dimension_unit]
        self.fy = fy*unit[Resistence_unit]
        self.fu = fu*unit[Resistence_unit]
        self.bf = bf*unit[Dimension_unit]


class Plate:
    
    def __init__(self, 
                 name:str, 
                 f_uc:float,
                 f_yc:float,
                 c:float,
                 Resistence_unit='megapascal',
                 Dimension_unit='millimeter') -> None:
        '''
        Parameters
        ----------
        
        * name: str
                Espessura da chapa
        * f_uc: float
                Resistência a ruptura da chapa
        * f_yc: float
                Resistência ao escoamento
        * c: float
                Comprimento
        '''
        
        chapas = {'CH 3/16"':4.75*unit['millimeter'],
                  'CH 1/4"':6.35*unit['millimeter'],
                  'CH 5/16"':7.94*unit['millimeter'],
                  'CH 3/8"':9.53*unit['millimeter'],
                  'CH 1/2"':12.7*unit['millimeter'],
                  'CH 5/8"':15.88*unit['millimeter'],
                  'CH 3/4"':19.05*unit['millimeter'],
                  'CH 7/8"':22.23*unit['millimeter'],
                  }
        
        
        self.t_ch = chapas[name].to(Dimension_unit)
        self.c = c*unit[Dimension_unit]
        self.f_uc = f_uc*unit[Resistence_unit]
        self.f_yc = f_yc*unit[Resistence_unit]


class Conector:
    
    def __init__(self, 
                 d_b:float, 
                 f_ub:float,
                 Resistence_unit='megapascal',
                 Dimension_unit='millimeter') -> None:
        
        '''
        Parameters
        ----------
        
        * d_b:
                Diâmetro de parafuso
        * f_ub: 
                Resistência a ruptura do parafusos
        '''
        self.d_b = d_b*unit[Dimension_unit]
        self.f_ub = f_ub*unit[Resistence_unit]
        self.name = f'ASTM {f_ub} d={d_b}'

class Column:
    def __init__(self, 
                 name:str,
                 tf:float,
                 tw:float,
                 h:float,
                 bf:float,
                 Dimension_unit='millimeter'):
        '''
        Parameters
        ----------
        
        * tf: float
                Espessura do flange
        * h: float
                Altura da alma do perfil
        * bf: float
                Comprimento do flange
        * tw:float
                Espessura da alma do perfil

        '''
        self.name = name   
        self.h = h*unit[Dimension_unit]
        self.tf = tf*unit[Dimension_unit]
        self.tw = tw*unit[Dimension_unit]
        self.bf = bf*unit[Dimension_unit]


class CornerFrame:
    def __init__(self, 
                     t_ch:float, 
                     f_yc:float,
                     f_uc:float,
                     lc:float,
                     Resistence_unit='megapascal',
                     Dimension_unit='millimeter'):
        '''
        Parameters:
        ----------
        * t_ch: float
                Espessura da chama
        * f_yc: float
                Resistência caracteristica do aço a escoamento 
        * f_uc: float
                Resistência caracterisitca do aço a ruptura
        * lc: float
                Comprimento da ligação
        
        '''
        self.name = f'2L {lc}x{t_ch}'
        self.t_ch = t_ch*unit[Dimension_unit]
        self.lc = lc*unit[Dimension_unit] # Comprimento da ligação
        self.c = lc*unit[Dimension_unit] # Comprimento da ligação
        self.f_yc = f_yc*unit[Resistence_unit]
        self.f_uc = f_uc*unit[Resistence_unit]

        

if __name__ == '__main__':
    test = Conector(1,2)
    test1 = test.f_ub*test.d_b*test.d_b
    print(test1.to('newton'))