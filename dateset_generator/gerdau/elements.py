from gerdau.unit import unit


class Beam:
    def __init__(self,
                 name:str,
                 h:float,
                 tw:float,
                 tf:float,
                 fy:float,
                 fu:float,
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
        '''
        self.name = name
        self.h = h*unit[Dimension_unit]
        self.tw = tw*unit[Dimension_unit]
        self.tf = tf*unit[Dimension_unit]
        self.fy = fy*unit[Resistence_unit]
        self.fu = fu*unit[Resistence_unit]


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


class Column:
    def __init__(self, 
                 name:str,
                 tf:float,
                 h:float,
                 Dimension_unit='millimeter'):
        '''
        Parameters
        ----------
        
        * tf: float
                Espessura do flange
        * h: float
                Altura da alma do perfil

        '''
        self.name = name   
        self.h = h*unit[Dimension_unit]
        self.tf = tf*unit[Dimension_unit]


if __name__ == '__main__':
    test = Conector(1,2)
    test1 = test.f_ub*test.d_b*test.d_b
    print(test1.to('newton'))