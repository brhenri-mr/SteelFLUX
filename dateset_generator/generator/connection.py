import numpy as np
from generator.unit import unit
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from generator.plot import breakline
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from settings import Settings
import os
from uuid import UUID


class BoltChecker:
    '''
    Classe para verificação dos parafusos, independente do conjunto
    '''
    def __init__(self, 
                 Conector, 
                 n_ps:int,
                 coef=1.35,
                 Result_unit='kilonewton'):
            
        self.Parafuso = Conector
        self.coef = coef
        self.n_ps = n_ps
        self.Result_unit = Result_unit
        
        
    def boltShear(self, Corte='Rosca') -> float:
        '''
        Status Verificado
        -----------------
        
        Cálculo da Cortante no grupo de parafusos segundo NBR 8800:2008 item 6.3.3.2
        
        Parameters
        ----------
        
        * d_b: float
                Diâmetro do parafuso
        * F_ub: float
                Resistência última do parafuso
        * n_ps: int
                Número de parafusos na chapa de extremidade
        * coef: float
                coeficiente de ponderação
        
        Return
        ------
        Resistência de cáluclo a cortante do parafuso
        '''
        # Área do parafuso
        a_b = 0.25*np.pi*self.Parafuso.d_b**2
        
        # Determinação do local de corte do parafuso
        match Corte:
            case 'Conservador':
                return (0.4*a_b*self.Parafuso.f_ub*self.n_ps/self.coef).to(self.Result_unit)
            case 'Rosca':
                return (0.4*a_b*self.Parafuso.f_ub*self.n_ps/self.coef).to(self.Result_unit)
            case 'Fuste':
                return (0.5*a_b*self.Parafuso.f_ub*self.n_ps/self.coef).to(self.Result_unit)


class BasicConnection:
    def __init__(self, 
                 n_ps:float,
                 Conector,
                 Coluna,
                 Viga,
                 uuid:UUID,
                 s:float, 
                 Conectante,
                 Dimension_unit='millimeter',
                 Result_unit='kilonewton',
                 dev_mode=True,
                 coef=1.35,
                 ):
       
       
        self.uuid = uuid
        self.dev_mode = dev_mode
        self.settings = Settings()
        self.d_h = Conector.d_b + 1.5*unit['millimeter'] # Diametro de furo
        self.Coluna = Coluna
        self.Viga = Viga
        self.s = s*unit[Dimension_unit] # Distancia entre centroide de furo interno
        
        # Tentando verificar a distância da borda com uma valor de tamanho de Conectante
        try:
            self.lc = Conectante.lc
            self.e = (Conectante.lc - (n_ps/2 -1)*self.s)/2 # Distancia entre centro do furo e borda vertical

    
        except:
            self.lc = 0*unit[Dimension_unit]
            self.e = (Viga.h - (n_ps/2 -1)*self.s)/2 # Distancia entre centro do furo e borda vertical
            
        assert self.e.magnitude>0, 'Distância entre furos (s) está superando o comprimento da chapa'
        
        assert s>= 3*Conector.d_b.magnitude, 'Distância entre furos insuficiente' # Distância mínima entre furos Iterm 6.3.9
            
        self.Result_unit = Result_unit
        self.coef = coef
        self.Conectante = Conectante
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig_frontal, self.ax_frontal = plt.subplots(figsize=(8, 6))
        self.fig_top, self.ax_top = plt.subplots(figsize=(8, 6))
        self.TAMANHO = Settings().TAMANHO_IMG
        
        # Inicializando as pastas do dataset
        self.initialize()
        
        # Inicializando o desenho padrão
        self.plotBasic()
        self.plotBasicFrontal()
        self.plotBasicTop()
        
    
    def initialize(self):
        '''
        Método para criar as pastas do dataset
        '''
        # Verificando se já não existe as pastas
        if not os.path.isdir(self.settings.DATASET_URL):
            for pasta in ['img', 'base', 'mask']:
                for subpasta in ['frontal', 'lateral', 'top']:
                    os.makedirs(os.path.join(self.settings.DATASET_URL, pasta, subpasta), exist_ok=True)
            
    
    def plotBasic(self, SHOW=False):
        '''
        Plot da vista básica lateral da conexão
        '''
        unit.setup_matplotlib()
        self.ax.set_ylim(0, self.TAMANHO*1.17) 
        self.ax.set_xlim(0, self.TAMANHO*1.17)
        
        
        # -------------------------------Coluna Definição das Breakline-------------------------------
        for altura in [1, self.TAMANHO]:
                coord = list(zip(*breakline(-1, altura, 
                                            length=self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + self.lc.magnitude)))
                self.ax.plot(coord[0],coord[1], color='black', linewidth=0.8)
        
        # -------------------------------Coluna Definição das mesas-------------------------------
        for offset in [0, self.Coluna.h.magnitude + self.Coluna.tf.magnitude + self.lc.magnitude]:
                
                mesa2 = patches.Rectangle((1 + offset ,1), 
                                 self.Coluna.tf.magnitude, self.TAMANHO-1, edgecolor='black', facecolor='gray')
                self.ax.add_patch(mesa2)

        coluna = patches.Rectangle((1 + self.Coluna.tf.magnitude,1), 
                                 self.Coluna.h.magnitude+ self.lc.magnitude, self.TAMANHO-1, edgecolor='black', facecolor='gray')
        self.ax.add_patch(coluna)
        
        # ---------------------------------VIGA-----------------------------------------------------
        mesa1 = patches.Rectangle((self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Conectante.t_ch.magnitude + self.lc.magnitude, 
                                  self.TAMANHO/2 + self.Viga.h.magnitude/2 ), 
                                 100+self.lc.magnitude, self.Viga.tf.magnitude*1.6, edgecolor='black', facecolor='gray')
        self.ax.add_patch(mesa1)
        
        mesa2 = patches.Rectangle((self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Conectante.t_ch.magnitude + self.lc.magnitude, 
                                  self.TAMANHO/2 - self.Viga.h.magnitude/2 - self.Viga.tf.magnitude*1.6 ), 
                                 100+self.lc.magnitude, self.Viga.tf.magnitude*1.6, edgecolor='black', facecolor='gray')
        self.ax.add_patch(mesa2)
        
        alma = patches.Rectangle((self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Conectante.t_ch.magnitude + self.lc.magnitude, 
                                  self.TAMANHO/2 - self.Viga.h.magnitude/2), 
                                 100+self.lc.magnitude, self.Viga.h.magnitude, edgecolor='black', facecolor='gray')
        self.ax.add_patch(alma)
        self.ax.axis('off')

        if SHOW:
            plt.show()
        
        if not self.dev_mode:
            self.fig.savefig(os.path.join(self.settings.DATASET_URL,'base','lateral',f'{self.uuid}.png'))
        
        
    def plotBasicFrontal(self, SHOW=False):
        unit.setup_matplotlib()

        # Tamanho da imagem - dos eixos 
        width = self.Conectante.c.magnitude*1.2
        height = self.Viga.h.magnitude*1.2
        
        # Defindo os limites dos eixos
        self.ax_frontal.set_xlim(0, width)  
        self.ax_frontal.set_ylim(0, height)  
        
        tamanho_retangulo = self.Coluna.bf.magnitude
        
        centro_x = (self.Conectante.c.magnitude*0.1 + self.Conectante.c.magnitude)/2
        centro_y = (self.Viga.h.magnitude*0.1 + self.Viga.h.magnitude)/2
        
        off_set = self.Conectante.c.magnitude*0.05 # preciso desse valor para que as coisas se encaixem
        
        off_set_y = self.Viga.h.magnitude*0.05

        
        # -------------------------------Coluna Definição das mesas-------------------------------

        coluna = patches.Rectangle((centro_x - self.Coluna.bf.magnitude/2 + off_set , -self.TAMANHO/2), 
                                 tamanho_retangulo, self.TAMANHO*2, edgecolor='black', facecolor='gray')
        self.ax_frontal.add_patch(coluna)
        
        # ---------------------------------VIGA-----------------------------------------------------
        points = [
                (centro_x - self.Viga.bf.magnitude/2 + off_set, centro_y - self.Viga.h.magnitude/2 - self.Viga.tf.magnitude + off_set_y),
                (centro_x - self.Viga.bf.magnitude/2 + off_set, centro_y - self.Viga.h.magnitude/2 + off_set_y),
                (centro_x - self.Viga.tw.magnitude/2 + off_set, centro_y - self.Viga.h.magnitude/2 + off_set_y),
                (centro_x - self.Viga.tw.magnitude/2 + off_set, centro_y + self.Viga.h.magnitude/2 + off_set_y),
                (centro_x - self.Viga.bf.magnitude/2 + off_set, centro_y + self.Viga.h.magnitude/2 + off_set_y),
                (centro_x - self.Viga.bf.magnitude/2 + off_set, centro_y + self.Viga.h.magnitude/2 + self.Viga.tf.magnitude + off_set_y),
                (centro_x + self.Viga.bf.magnitude/2 + off_set, centro_y + self.Viga.h.magnitude/2 + self.Viga.tf.magnitude + off_set_y),
                (centro_x + self.Viga.bf.magnitude/2 + off_set, centro_y + self.Viga.h.magnitude/2 + off_set_y),
                (centro_x + self.Viga.tw.magnitude/2 + off_set, centro_y + self.Viga.h.magnitude/2 + off_set_y),
                (centro_x + self.Viga.tw.magnitude/2 + off_set, centro_y - self.Viga.h.magnitude/2 + off_set_y),
                (centro_x + self.Viga.bf.magnitude/2 + off_set, centro_y - self.Viga.h.magnitude/2 + off_set_y),
                (centro_x + self.Viga.bf.magnitude/2 + off_set, centro_y - self.Viga.h.magnitude/2 - self.Viga.tf.magnitude + off_set_y),
        ]
        
        # Adicionado A viga
        perfil = patches.Polygon(points ,closed=True, fill=True, edgecolor='black', hatch='//', facecolor='gray',linewidth=2)
        self.ax_frontal.add_patch(perfil)

        self.ax_frontal.axis('off')
        
        if not self.dev_mode:
            self.fig_frontal.savefig(os.path.join(self.settings.DATASET_URL,'base','front',f'{self.uuid}.png'))

        if SHOW:
            plt.show()
        
        return None
    
    
    def plotBasicTop(self, SHOW=False):
        '''
        Vista superior 
        '''
        self.ax_top.set_ylim(0, self.TAMANHO*1.17)  
        self.ax_top.set_xlim(0, self.TAMANHO*1.17)  
        offset = self.Conectante.t_ch.magnitude
        
        points = [
                (1, 1), (1, 1 + self.Coluna.bf.magnitude),
                (1 + self.Coluna.tf.magnitude, 1 + self.Coluna.bf.magnitude),
                (1 + self.Coluna.tf.magnitude, 1 + self.Coluna.bf.magnitude/2 + self.Coluna.tw.magnitude/2),
                (1 + self.Coluna.tf.magnitude + self.Coluna.h.magnitude, 1 + self.Coluna.bf.magnitude/2 + self.Coluna.tw.magnitude/2),
                (1 + self.Coluna.tf.magnitude + self.Coluna.h.magnitude, 1 + self.Coluna.bf.magnitude),
                (1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude, 1 + self.Coluna.bf.magnitude),
                (1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude, 1),
                (1 + self.Coluna.tf.magnitude + self.Coluna.h.magnitude, 1),
                (1 + self.Coluna.tf.magnitude + self.Coluna.h.magnitude, 1 + self.Coluna.bf.magnitude/2 - self.Coluna.tw.magnitude/2),
                (1 + self.Coluna.tf.magnitude , 1 + self.Coluna.bf.magnitude/2 - self.Coluna.tw.magnitude/2),
                (1 + self.Coluna.tf.magnitude , 1),
                (1, 1)
                ]
        
        coluna = patches.Polygon(points, closed=True, fill=True, edgecolor='black', hatch='//', facecolor='gray',linewidth=2)
        self.ax_top.add_patch(coluna)
        
        #-------------------------------------------------Viga----------------------------------------------------
        
        mesa = patches.Rectangle((offset + 1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude, 1 + self.Coluna.bf.magnitude/2 - self.Viga.bf.magnitude/2),
                                 200, self.Viga.bf.magnitude,edgecolor='black', facecolor='gray')
        self.ax_top.add_patch(mesa)
        
        self.ax_top.plot([offset + 1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude, 
                          offset + 1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude + 200],
                          [1 + self.Coluna.bf.magnitude/2 - self.Viga.tf.magnitude/2, 
                           1 + self.Coluna.bf.magnitude/2 - self.Viga.tf.magnitude/2], linestyle='--', color='black') # alma 1
        
        self.ax_top.plot([offset + 1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude, 
                          offset + 1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude + 200],
                          [1 + self.Coluna.bf.magnitude/2 + self.Viga.tf.magnitude/2, 
                           1 + self.Coluna.bf.magnitude/2 + self.Viga.tf.magnitude/2], linestyle='--', color='black') # alma 1
        
        
        #---------------------------------------------------------------------------------------------------------
        
        self.ax_top.axis('off')

        if not self.dev_mode:
            self.fig_top.savefig(os.path.join(self.settings.DATASET_URL,'base','top',f'{self.uuid}.png'))

        if SHOW:
            plt.show()
        
        
    
    def plateShear(self):
        ''' 
        Status Verificado
        -----------------
        
        Função para cálculo do cisalhamento da chapa de extermidade bruta e liquída
        
        Parameters
        ----------
        * f_yc: float
                Resistência de cálculo ao escoamento da chapa
        
        * f_uc: float
                Limite de resistência a tração do aço do elemento de ligação (cantoneira ou chapa 
                
        * t_ch: float
                Espessura da chapa de extremidade

        * n_ps: int
                Número de parafusos na chapa de extremidade  
        
        * s: float
                Distância vertical entre furos

        * e: float
                Distância vertical entre furo e borda; excentricidade em placas de base (Md/Nd)
        
        * d_h: float
                Diâmetro do furo
                
        * coef: float
                Coeficiente de ponderação
        Return
        ------
        Resistência de cálculo ao cisalhamento da placa, o mínimo entre as duas resistências
        
        '''
        # Área bruta da seção 
        ag = ((0.5*self.n_ps - 1)*self.s + 2*self.e)*self.Conectante.t_ch
        
        v_bruta = 2*0.6*self.Conectante.f_yc*ag/self.coef1
        
        # Resistência da seção liquída
        # Ver NBR 8800:2008 - Item 5.2.4.1
        anv = (self.n_ps*0.5*(self.d_h + 2*unit['millimeter'])*self.Conectante.t_ch)
         
        v_liquida = 2*0.6*self.Conectante.f_uc*(ag - anv)/self.coef
        
        
        return min(v_bruta, v_liquida).to(self.Result_unit)


    def plateCrush(self) ->float:
        '''
        Status Verificado
        -----------------
        
        Cálculo do pressão de contato do elemento conector para o conjunto de parafusos
        NBR880:2008. item 6.3.3.3
        
        Parameters
        ----------
        
        * d_b: float
                Diâmetro do parafuso
        
        * t_ch: float
                Espessura da chapa de extremidade

        * f_uc: float
                Limite de resistência a tração do aço do elemento de ligação (cantoneira ou chapa 

        * n_ps: int
                Número de parafusos na chapa de extremidade  
        
        * s: float
                Distância vertical entre furos

        * e: float
                Distância vertical entre furo e borda; excentricidade em placas de base (Md/Nd)

        * d_h: float
                Diâmetro do furo

        * coef: float
                Coeficiente de ponderação
        
        
        Return
        ------
        * saida: float
                Resistência mínima da chapa a pressão de contato incluindo rasgamento e esmagamento
        
        * individual: lista
                Lista com as resistência indiviuais de cada região conectada
        '''
        # Quantidade de regiões q eu tenho
        times = int(2+self.n_ps/2-1)
        saida = [] # Lista com os valores individuais
        
        # O calculo é feito para cada parafuso
        for i in range(times):

                crush = 2.4*self.Parafuso.d_b*self.Conectante.t_ch*self.Conectante.f_uc/self.coef
                if i == 0 or i == times - 1:
                        # Furo Externo
                        crush_hole = 1.2*(self.s - self.d_h)*self.Conectante.t_ch*self.Conectante.f_uc/self.coef
                else:
                        # Furo interna
                        crush_hole = 1.2*(self.e - 0.5*self.d_h)*self.Conectante.t_ch*self.Conectante.f_uc/self.coef
                
                saida.append(min(crush,crush_hole).to(self.Result_unit))   
                
        
        return sum(saida).to(self.Result_unit), saida


class BeamChecker:

    def __init__(self, 
                 n_ps:float,
                 Viga,
                 s:float,
                 e:float,
                 Dimension_unit='millimeter',
                 Result_unit='kilonewton',
                 coef1=1.1
                 ):

        self.s = s*unit[Dimension_unit] # Distancia entre centroide de furo interno
        self.e = e
        self.Result_unit = Result_unit
        self.coef1 = coef1
        self.Viga = Viga


    def beamWebShear(self):
        '''
        Status Verificado
        -----------------
        
        Cálculo do cisalhamento na alma da viga apoiada - Viga
        (NBR 8800:2008 – item 6.5.5.a) 
        
        Parameters
        ---------
        
        * fy: Float
                Resistência ao escoamento do aço
        * n_ps: int
                Quantidade de parafusos na conexão
        * tw: float
                Espessura da alma da viga
        * e: float
                Distância entre a extermidade da placa e o parafuso
        * s: float
                Distância entre parafusos consecutivos 
        Return
        ------
        Resistência ao cortante 
        
        '''
        # Área bruta da seção
        ag = ((self.n_ps*0.5 - 1)*self.s + 2*self.e)*self.Viga.tw
        
        return (0.6*self.Viga.fy*ag/self.coef1).to(self.Result_unit)


    def crushBeam(self):
        '''
        Cálculo do Rasgamento/Pressão de contato na alma da viga apoiada conector para o conjunto de parafusos
        NBR880:2008. item 6.3.3.3
        
        Parameters
        ----------
        
        * d_b: float
                Diâmetro do parafuso
        
        * t_ch: float
                Espessura da chapa de extremidade

        * f_uc: float
                Limite de resistência a tração do aço do elemento de ligação (cantoneira ou chapa 

        * n_ps: int
                Número de parafusos na chapa de extremidade  
        
        * s: float
                Distância vertical entre furos

        * e: float
                Distância vertical entre furo e borda; excentricidade em placas de base (Md/Nd)

        * d_h: float
                Diâmetro do furo

        * coef: float
                Coeficiente de ponderação
        
        
        Return
        ------
        * saida: float
                Resistência mínima da chapa a pressão de contato incluindo rasgamento e esmagamento
        
        * individual: lista
                Lista com as resistência indiviuais de cada região conectada
        '''
        # Quantidade de regiões q eu tenho
        times = int(2+self.n_ps/2-1)
        saida = [] # Lista com os valores individuais
        
        # O calculo é feito para cada parafuso
        for i in range(times):

                crush = 2.4*self.Parafuso.d_b*self.Viga.tw*self.Viga.fu/self.coef
                if i == 0 or i == times - 1:
                        # Furo Externo
                        crush_hole = 1.2*(self.s - self.d_h)*self.Viga.tw*self.Viga.fu/self.coef
                else:
                        # Furo interna
                        crush_hole = 1.2*(self.e - 0.5*self.d_h)*self.Viga.tw*self.Viga.fu/self.coef
                
                saida.append(min(crush,crush_hole).to(self.Result_unit))   
                
        
        return sum(saida).to(self.Result_unit), saida


class EndPLate(BoltChecker, BasicConnection, BeamChecker):
    
    def __init__(self,
                 Conector, 
                 Plate, 
                 Viga,
                 Coluna, 
                 s:float,
                 n_ps:float,
                 g_ch:float,
                 uuid:UUID,
                 Dimension_unit='millimeter',
                 Result_unit='kilonewton',
                 coef=1.35,
                 coef1=1.1,
                 dev_mode=True) -> None:
        '''
        Status Não Testado
        -----------------
        
        Parameters
        ----------
        * Conector:
                Classe de Conector
        
        * Plate:
                Classe de Plate
        * Viga: 
                Classe de Viga
        * Coluna:
                Classe de Coluna
        * n_ps: int
                Quantidade de parafusos na conexão
        * s: float
                Distância entre centros de parafusos consecutivos na linha de ação da conexão 
        * e: float
                Distância entre parafusos e a extermidade
                
        * g_ch: float
                gabarito de furação da chapa de extremidade
        * uuid: UUID
                Identificador unico da conexão
        
        '''
        # Chamando os construtores das classes pai diretamente
        BoltChecker.__init__(self, Conector, n_ps, coef, Result_unit)
        
        # Instanciando uma conexão básica
        BasicConnection.__init__(self, n_ps= n_ps, 
                                 Conector=Conector, 
                                 Viga=Viga, 
                                 s= s, 
                                 Dimension_unit=Dimension_unit, 
                                 Result_unit=Result_unit,
                                 coef=coef,
                                 Conectante=Plate,
                                 uuid=uuid,
                                 dev_mode=dev_mode,
                                 Coluna=Coluna,)
        
        
        BeamChecker.__init__(self, n_ps=n_ps, 
                             Viga=Viga, 
                             s=s,
                             e=self.e,
                             Dimension_unit= Dimension_unit, 
                             Result_unit=Result_unit, 
                             coef1=coef1)

         
        # Classes
        self.Chapa = Plate
        self.Viga = Viga

        self.Coluna = Coluna
        
        # Dados
        self.g_ch = g_ch*unit[Dimension_unit] # Distancia entre linhas de parafusos
        
        # Dimensoes
        self.Dimension_unit = Dimension_unit
        self.Result_unit = Result_unit

        # Admensional
        self.n_ps = n_ps # Quantidade de parafusos
        self.coef = coef

        self.TAMANHO = Settings().TAMANHO_IMG
        
        self.settings = Settings()
        
        self.uuid = uuid
        self.pontos_ancoragem = {}
        
        #dev_mode controla se a classe irá ou não salvar as imagens
        # Caso seja True, as imagens não serão salvar
        # Caso contrario, serão
        self.dev_mode = dev_mode


    def platePlot(self, show=False): 
        '''
        Vista Frontal detalhada
        '''
        # Criar uma figura e eixos
        unit.setup_matplotlib()
        
        # Tamanho da imagem - dos eixos 
        width = self.Chapa.c.magnitude*1.2
        height = self.Viga.h.magnitude*1.2
        
        # Ponto de ancoragem
        local_plate = (self.Chapa.c.magnitude*0.1, self.Viga.h.magnitude*0.1) # Chapa
        local_web = ((width - self.Viga.tw.magnitude)*0.5, self.Viga.h.magnitude*0.1) # Alma da viga
        

        
        # Defindo os limites dos eixos
        self.ax_frontal.set_xlim(-width*0.5, width*1.5)  
        self.ax_frontal.set_ylim(-height*0.5, height*1.5)  
        
        # PLotagem da chapa
        rect = patches.Rectangle(local_plate, 
                                 self.Chapa.c.magnitude, self.Viga.h.magnitude, edgecolor='black', facecolor='#D3D3D3')
        self.ax_frontal.add_patch(rect)  
        
        # Plotagem da alma
        hatch_rect = patches.Rectangle(local_web, self.Viga.tw.magnitude, self.Viga.h.magnitude, 
                                       lw=2.5,edgecolor='black', facecolor='gray', hatch='//')
        self.ax_frontal.add_patch(hatch_rect)

        #--------------- Adicionar cota horizontal-----------------------------

        self.ax_frontal.annotate('', 
                xy=(self.Chapa.c.magnitude*0.1, (self.Viga.h.magnitude + self.Viga.tf.magnitude)*1.20), 
                xytext=(self.Chapa.c.magnitude*1.1, (self.Viga.h.magnitude + self.Viga.tf.magnitude)*1.20), 
                arrowprops={'arrowstyle': '<->'})
        
        self.ax_frontal.text(width*0.5, (self.Viga.h.magnitude + self.Viga.tf.magnitude)*1.25, f'L = {round(self.Chapa.c.magnitude, 2)}', ha='center', va='center',fontsize=8) 
        
        self.ax_frontal.annotate('', 
                xy=(width/2 - self.g_ch.magnitude/2, (self.Viga.h.magnitude + self.Viga.tf.magnitude)*1.12), 
                xytext=(width/2 + self.g_ch.magnitude/2, (self.Viga.h.magnitude + self.Viga.tf.magnitude)*1.12), 
                arrowprops={'arrowstyle': '<->'})
        
        self.ax_frontal.text(width*0.5, (self.Viga.h.magnitude + self.Viga.tf.magnitude)*1.15, f'{round(self.g_ch.magnitude, 2)}', ha='center', va='center',fontsize=8) 

        
        #--------------------------------------- Adicionar cota Vertical-------------------------------------
        self.ax_frontal.annotate('', 
                    xy=(self.Chapa.c.magnitude*0.07, self.Viga.h.magnitude*0.1), 
                    xytext=(self.Chapa.c.magnitude*0.07, self.Viga.h.magnitude*1.1), 
                    arrowprops={'arrowstyle': '<->'})
        
        self.ax_frontal.text(self.Chapa.c.magnitude*0.00000001, height*0.5, f'{round(self.Viga.h.magnitude, 2)}', 
                                                                        ha='left', va='center', rotation=90)
        ## Definicao do e inferior
        self.ax_frontal.annotate('', 
                    xy=(self.Chapa.c.magnitude*1.15, self.Viga.h.magnitude*0.1), 
                    xytext=(self.Chapa.c.magnitude*1.15, self.Viga.h.magnitude*0.1 + self.e.magnitude), 
                    arrowprops={'arrowstyle': '<->'})
        
        self.ax_frontal.text(self.Chapa.c.magnitude*1.16, (self.Viga.h.magnitude*0.1 + 0.5*self.e.magnitude), 
                                                f'{round(self.e.magnitude,2)}', ha='left', va='center',rotation=90)
        
        ## Definicao do e superior
        self.ax_frontal.annotate('', 
                    xy=(self.Chapa.c.magnitude*1.15, self.Viga.h.magnitude*1.1), 
                    xytext=(self.Chapa.c.magnitude*1.15, self.Viga.h.magnitude*1.1 - self.e.magnitude), 
                    arrowprops={'arrowstyle': '<->'})
        
        self.ax_frontal.text(self.Chapa.c.magnitude*1.16, (self.Viga.h.magnitude*1.1 - 0.5*self.e.magnitude), 
                                                f'{round(self.e.magnitude,2)}', ha='left', va='center',rotation=90)
        
        # Definição das cotas intermediárias
        for i in range(int(self.n_ps/2 - 1)):
                
                self.ax_frontal.annotate('', 
                    xy=(self.Chapa.c.magnitude*1.15, 
                        self.Viga.h.magnitude*0.1 + self.e.magnitude + self.s.magnitude*i), 
                    
                    xytext=(self.Chapa.c.magnitude*1.15,
                            self.Viga.h.magnitude*0.1 + self.e.magnitude + self.s.magnitude*(i+1)), 
                    arrowprops={'arrowstyle': '<->'})
        
                self.ax_frontal.text(self.Chapa.c.magnitude*1.16, 
                        (self.Viga.h.magnitude*0.1 + self.e.magnitude + (((i)*2 + 1)*self.s.magnitude)/2), 
                                                f'{round(self.s.magnitude,2)}', ha='left', va='center',rotation=90)
                
        
        #---------------------------------------------------------------------------------------------------
        parafuso_annotate = True
        for i in range(int(self.n_ps*0.5)):
                # Definindo as coordenadas do centro de cada furo
                x_d = width/2 + self.g_ch.magnitude/2
                
                x_e = width/2 - self.g_ch.magnitude/2
                
                y = self.Viga.h.magnitude*0.1 + self.e.magnitude + self.s.magnitude*i

                # Linha de centro e furo
                for x_i in [x_d, x_e]:
                        circle = plt.Circle((x_i, y), 
                                    self.d_h.magnitude/2, 
                                    edgecolor='black', 
                                    facecolor='white')
                
                        self.ax_frontal.add_patch(circle)
                        
                        # linha horizontal de centro
                        self.ax_frontal.plot([(x_i + self.d_h.magnitude/2) + self.d_h.magnitude/2*0.5 , 
                        (x_i - self.d_h.magnitude/2) - self.d_h.magnitude/2*0.5], 
                                [y, y], 
                                color='red', linestyle='-.', linewidth=1)
                        
                        # linha Vertical de centro
                        self.ax_frontal.plot([x_i , x_i], 
                        [(y + self.d_h.magnitude/2) + self.d_h.magnitude/2*0.5 , 
                        (y - self.d_h.magnitude/2) - self.d_h.magnitude/2*0.5  ], 
                                color='red', linestyle='-.', linewidth=1)

                        if parafuso_annotate:
                                parafuso_annotate = False
                                self.ax_frontal.annotate('', 
                                        xy=(x_e, y), 
                                        xytext=(x_e, y - self.e.magnitude - self.Viga.tf.magnitude - 12), 
                                        arrowprops={'arrowstyle': '->'})

                                self.ax_frontal.text(x_e , (y - self.e.magnitude - self.Viga.tf.magnitude) - 12, f'{self.Parafuso.name}', ha='left', va='center',)
        
        # Deligando a moldura
        self.ax_frontal.axis('off')

        if not self.dev_mode:
            self.fig_frontal.savefig(os.path.join(self.settings.DATASET_URL,'img','frontal',f'{self.uuid}.png'))
  
        if show:
            plt.show()
        

    def plotLateral(self, show=False):
        '''
        Vista lateral detalhada
        '''
        unit.setup_matplotlib()

        parafuso_interno = int((self.n_ps/2 - 1))
        
        # ---------------------------------Chapa-----------------------------------------------------
        chapa_ponto_init = (self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1, self.TAMANHO/2 - self.Viga.h.magnitude/2 )
        chapa_ponto_final = (self.Chapa.t_ch.magnitude, self.Viga.h.magnitude,)
        rect = patches.Rectangle(chapa_ponto_init, 
                                 self.Chapa.t_ch.magnitude, self.Viga.h.magnitude, edgecolor='black', facecolor='#D3D3D3')
        
        # Salvando ponto de ancoragem do elemento
        self.pontos_ancoragem['Chapa'] = {'Start':chapa_ponto_init,'Final':chapa_ponto_final}
        self.ax.add_patch(rect)
        
        # ----------------------------------------Furos-----------------------------------------------------
        
        furo = patches.Rectangle((self.Coluna.h.magnitude + self.Coluna.tf.magnitude + 1 , 
                                  self.TAMANHO/2 - self.Viga.h.magnitude/2 + self.e.magnitude - self.d_h.magnitude/2), 
                                 self.Coluna.tf.magnitude+self.Chapa.t_ch.magnitude, self.d_h.magnitude, edgecolor='black', facecolor='black')
        self.ax.add_patch(furo)
        
        furo = patches.Rectangle((self.Coluna.h.magnitude + self.Coluna.tf.magnitude + 1 , 
                                  self.TAMANHO/2 + self.Viga.h.magnitude/2 - self.e.magnitude - self.d_h.magnitude/2), 
                                 self.Coluna.tf.magnitude+self.Chapa.t_ch.magnitude, self.d_h.magnitude, edgecolor='black', facecolor='black')
        self.ax.add_patch(furo)
        
        for i in range(parafuso_interno-1):
                
                furo_interno = patches.Rectangle((
                                self.Coluna.h.magnitude + self.Coluna.tf.magnitude + 1 , 
                                self.TAMANHO/2 - self.Viga.h.magnitude/2 + self.e.magnitude - self.d_h.magnitude/2 + self.s.magnitude*(i+1)), 
                                self.Coluna.tf.magnitude+self.Chapa.t_ch.magnitude, 
                                self.d_h.magnitude, 
                                edgecolor='black', facecolor='black')
                self.ax.add_patch(furo_interno)
        
        
        self.ax.annotate('', 
                    xy=(self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude*0.5, 
                        self.TAMANHO/2 + self.Viga.h.magnitude/2 ), 
                    xytext=(self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude,
                            self.TAMANHO/2 + self.Viga.h.magnitude*0.65), 
                    arrowprops={'arrowstyle': '->'})
        self.ax.text(self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude,
                self.TAMANHO/2 + self.Viga.h.magnitude*0.65, f'CH {self.Chapa.t_ch.magnitude}', ha='left', va='center',)
        
        self.ax.axis('off')
        
        if not self.dev_mode:
            self.fig.savefig(os.path.join(self.settings.DATASET_URL,'img', 'lateral', f'{self.uuid}.png'))
        
        if show:
                plt.show() # if you need...
        
        return self.ax

    
    def plotTop(self, show=False):
        '''
        Plot da vista superior detalhada
        '''
  
        chapa = patches.Rectangle((1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude ,1 + self.Coluna.bf.magnitude/2 - self.Conectante.c.magnitude/2),
                                   self.Conectante.t_ch.magnitude, self.Conectante.c.magnitude ,edgecolor='black', facecolor='#D3D3D3') # Desennhando a chapa
        
        self.ax_top.add_patch(chapa) # Inserindo no desenho
        
        # Salvando a imagem no local correto      
        if not self.dev_mode:
            self.fig_top.savefig(os.path.join(self.settings.DATASET_URL,'img','top',f'{self.uuid}.png'))
        
        if show:
            plt.show()


    def plotConnection(self):
        '''
        Função para plotar a conexão feita
        '''
        self.platePlot() # Conexão frontal
        self.plotLateral() # conexão lateral
        self.plotTop() # Conexão superior
        

    def mask(self):
        '''
        Método para geração da mascara da imagem da conexão
        '''
        
        #-----------------mascara da imagem lateral----------------
        
        background = patches.Rectangle((0, 0 ),
                                       self.TAMANHO*1.17, self.TAMANHO*1.17,
                                       edgecolor='black', facecolor='black')
        
        self.ax.add_patch(background)
        
        mask = patches.Rectangle((self.Coluna.h.magnitude + self.Coluna.tf.magnitude + 1 + self.lc.magnitude, 
                                  self.TAMANHO/2 - self.Viga.h.magnitude/2-self.Viga.tf.magnitude-10),
                                 self.Conectante.t_ch.magnitude+30, self.Viga.h.magnitude+50, 
                                 edgecolor='white', facecolor='white', zorder=10)
        self.ax.add_patch(mask)
              
        # Salavando mascara
        self.fig.savefig(os.path.join(self.settings.DATASET_URL,'mask','lateral',f'{self.uuid}.png'), facecolor="black")
        
        #-----------------mascara da imagem frontal----------------
        
        
        
        background = patches.Rectangle(((self.Conectante.c.magnitude*0.1 + self.Chapa.c.magnitude)/2 + self.Conectante.c.magnitude*0.05 - self.Coluna.bf.magnitude/2 ,
                                        -self.TAMANHO/2),
                                       self.Coluna.bf.magnitude , self.TAMANHO*2,
                                       edgecolor='black', 
                                       facecolor='black',
                                       zorder=9)
                                       
        self.ax_frontal.add_patch(background)
        
        mask = patches.Rectangle((0, self.Viga.h.magnitude*0.1 - self.Viga.tf.magnitude - 16),
                                 self.Chapa.c.magnitude+50, self.Viga.h.magnitude*1.25 +self.Viga.tf.magnitude*2.25+16, 
                                 edgecolor='white', 
                                 facecolor='white',
                                 zorder=10)
        self.ax_frontal.add_patch(mask)
        
        self.fig_frontal.savefig(os.path.join(self.settings.DATASET_URL,'mask','front',f'{self.uuid}.png'), facecolor="black")
         
        #-----------------mascara da imagem superior---------------
        
        # Ocultando o desenho
        background = patches.Rectangle((0, 0 ),
                                       self.TAMANHO*1.17, self.TAMANHO*1.17, edgecolor='black', facecolor='black')
        
        self.ax_top.add_patch(background)
        
        # Inserindo mascara
        mask = patches.Rectangle((1 + self.Coluna.tf.magnitude*2 + self.Coluna.h.magnitude, 
                                  1 + self.Coluna.bf.magnitude/2 - self.Conectante.c.magnitude/2),
                                 self.Conectante.t_ch.magnitude + 50, self.Chapa.c.magnitude, edgecolor='white', facecolor='white', zorder=10)
        self.ax_top.add_patch(mask)
        
        # Removendo as linhas que dão problema
        [line.remove() for line in self.ax_top.lines]
        
        # Salavando mascara
        self.fig_top.savefig(os.path.join(self.settings.DATASET_URL,'mask','top',f'{self.uuid}.png'), facecolor="black")
        
        return None

        

    def plateBearing(self):
        '''
        Flexão da chapa de extremidade
        
        ATUALMENTE É UMA RECOMENDAÇÃO DA GERDAU, NÃO VEJO LOGICA EM TER RESISTÊNCIA DE PLACA DE FUNDO
        NO FINAL DE UMA VIGA QUE AINDA POR CIMA É FLEXÍVEL
        
        APARENTEMENTE O EUROCODE TEM ALGO--- VER
        
        '''
        
        l_fch = (0.5*self.n_ps - 1)*self.s + 2*self.e
        
        return (((4*self.Chapa.t_ch*l_fch**2)/(6*self.g_ch)*self.Chapa.f_yc)/self.coef1).to(self.Result_unit)


    def blockShear(self, cts=1):
        '''
        Status Verificado
        -----------------
        
        Função para cálculo do block Shear da placa NBR880:2008. item 6.5.6
        
        Parameters
        ----------
        
        * t_ch: float
                Espessura da chapa de extremidade
        
        * c: float
                Comprimento da chapa

        * f_uc: float
                Limite de resistência a tração do aço do elemento de ligação (cantoneira ou chapa 
        
        * f_yc: float
                Limite de resistência ao escoamento do aço do elemento de ligação

        * n_ps: int
                Número de parafusos na chapa de extremidade  
        
        * s: float
                Distância vertical entre furos

        * e: float
                Distância vertical entre furo e borda; excentricidade em placas de base (Md/Nd)

        * d_h: float
                Diâmetro do furo

        * coef: float
                Coeficiente de ponderação
        
        
        Return
        ------
        Resistência ao rasgamento da chapa
        '''
        # Variaveis
        qntd_s = ((self.n_ps/2) - 1) # quantidade de espaçamentos s
        
        ## Caso 1 -- Caso com tração indo para borda externa
        # área de cisalhamento bruta
        a_gv = 2*(qntd_s*self.s + self.e)*self.Chapa.t_ch
        
        # Área líquida interna
        a_nv_int = qntd_s*((self.d_h +2*unit['millimeter'])*self.Chapa.t_ch)
        
        # Área líquida externa
        a_nv_ext = (0.5*(self.d_h +2*unit['millimeter'])*self.Chapa.t_ch)
        
        # Área líquida
        a_nv = a_gv - 2*(a_nv_ext + a_nv_int)
        
        # Área líquida de tração
        a_nt = 2*(-(0.5*(self.d_h +2*unit['millimeter'])*self.Chapa.t_ch) + self.Chapa.t_ch*(self.Chapa.c - self.g_ch )*0.5)
        
        # Cálculo da resistência de rasgamento para o caso 1
        f_rRd = min(0.6*self.Chapa.f_uc*a_nv + cts*self.Chapa.f_uc*a_nt,
                0.6*self.Chapa.f_yc*a_gv + cts*self.Chapa.f_uc*a_nt)

        
        ## Caso 2 -- Tração nos furos internos se conectam
        # Área líquida de tração
        a_nt = -((self.d_h +2*unit['millimeter'])*self.Chapa.t_ch) + self.Chapa.t_ch*(self.g_ch)
        
        # Cálculo da resistência de rasgamento para o caso 2
        f_rRd = min(0.6*self.Chapa.f_uc*a_nv + cts*self.Chapa.f_uc*a_nt,
                0.6*self.Chapa.f_yc*a_gv + cts*self.Chapa.f_uc*a_nt,
                f_rRd)
        
        
        return (f_rRd/self.coef).to(self.Result_unit)


    def crushBeam(self):
        # Proteger contra a verificação da alama da viga
        raise AttributeError('O cálculo da pressão de contato na viga apoiada não é aplicada a esse tipo de conexão') 


    def plateWelding(self):
        pass


    def analyze(self):
        """
        Análise do dimensionamento da conexão e suas partes constituintes
        """
        return {
            "blockShear":self.blockShear(),
            "plateBearing":self.plateBearing(),
            "blotShear":self.boltShear(),
            "platShear":self.plateShear(),
            "plateCrush":self.plateCrush(),
            "beamWebShear":self.beamWebShear(),
            "crushBeam":self.crushBeam()
        }


class LCPP(BoltChecker, BeamChecker, BasicConnection):
    '''
    Classe ded ligação metálicas estrutural flexível Dupla cantoneira
    '''
    def __init__(self, Conector,
                 Viga, 
                 Angle,
                 Coluna,
                 n_ps:float,
                 s:float, 
                 uuid:UUID,
                 coef=1.35, 
                 coef1=1.1,
                 dev_mode=True,
                 Dimension_unit='millimeter',
                 Result_unit='kilonewton'):
         
        BoltChecker.__init__(self, Conector, n_ps, coef, Result_unit)


        # Instanciando uma conexão básica
        BasicConnection.__init__(self, n_ps= n_ps, 
                                 Conector=Conector, 
                                 Viga=Viga, 
                                 s= s, 
                                 Dimension_unit=Dimension_unit, 
                                 Result_unit=Result_unit,
                                 coef=coef,
                                 dev_mode=dev_mode,
                                 uuid=uuid,
                                 Conectante=Angle,
                                 Coluna=Coluna,)
        
        
        BeamChecker.__init__(self, n_ps=n_ps, 
                             Viga=Viga, 
                             s=s,
                             e=self.e,
                             Dimension_unit= Dimension_unit, 
                             Result_unit=Result_unit, 
                             coef1=coef1)
        
        self.scale_corretion = Angle.lc.magnitude
        assert Angle.lc.magnitude < Viga.h.magnitude, 'Cantoneira maior que alma da viga'
    
    
    def plotView(self, show=False):
        unit.setup_matplotlib()
        parafuso_interno = int((self.n_ps/2 - 1))
        
        #----------------------------------Vista Frontal da aba------------------------------------------
        chapa_ponto_init = (self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.scale_corretion, 
                            self.TAMANHO/2 - self.Conectante.lc.magnitude/2)

        aba_frontal = patches.Rectangle(chapa_ponto_init,
                                 self.Conectante.t_ch.magnitude, self.Conectante.lc.magnitude, edgecolor='black', facecolor='#D3D3D3')
        self.ax.add_patch(aba_frontal)
        
        #---------------------------------Vista lateral da aba------------------------------------------
        # Por causa da escala, pode parecer que os valores de x são superior aos de y
        aba_lateral = patches.Rectangle((chapa_ponto_init[0] + self.Conectante.t_ch.magnitude, chapa_ponto_init[1]),
                                          self.Conectante.lc.magnitude - self.Conectante.t_ch.magnitude, self.Conectante.lc.magnitude,
                                         edgecolor='black', facecolor='#D3D3D3')
        
        self.ax.add_patch(aba_lateral)
        #--------------------------------------Furo-----------------------------------------------

        furo = patches.Circle((chapa_ponto_init[0] + self.Conectante.lc.magnitude - self.e.magnitude ,
                               chapa_ponto_init[1] + self.e.magnitude), 
                              radius=self.Parafuso.d_b.magnitude/2, 
                              edgecolor='black', 
                              facecolor='white')
        
        self.ax.add_patch(furo)
        
        furo = patches.Circle((chapa_ponto_init[0] + self.Conectante.lc.magnitude - self.e.magnitude,
                               chapa_ponto_init[1] +  self.Conectante.lc.magnitude - self.e.magnitude), 
                              radius=self.Parafuso.d_b.magnitude/2, 
                              edgecolor='black', 
                              facecolor='white')
        
        self.ax.add_patch(furo)
        
        for i in range(parafuso_interno-1):
                
                furo_interno = patches.Circle((
                                chapa_ponto_init[0] + self.Conectante.lc.magnitude - self.e.magnitude, 
                                chapa_ponto_init[1] + self.e.magnitude + self.s.magnitude*(i+1)), 
                                radius=self.Parafuso.d_b.magnitude/2,
                                edgecolor='black', facecolor='white')
                
                self.ax.add_patch(furo_interno) 
        #-----------------------------------------------------------------------------------------------
        # Definição das cotas intermediárias
        
             
        self.ax.annotate('', 
                    xy=(chapa_ponto_init[0] + self.Conectante.lc.magnitude+10, 
                        chapa_ponto_init[1]), 
                    
                    xytext=(chapa_ponto_init[0] + self.Conectante.lc.magnitude + 10,
                            chapa_ponto_init[1] + self.e.magnitude), 
                    arrowprops={'arrowstyle': '<->'})
        
        self.ax.text(chapa_ponto_init[0] + self.Conectante.lc.magnitude + 12, 
                        (chapa_ponto_init[1] + self.e.magnitude/2), 
                                                f'{round(self.e.magnitude,2)}', ha='left', va='center',rotation=90)        
        
                     
        self.ax.annotate('', 
                    xy=(chapa_ponto_init[0] + self.Conectante.lc.magnitude+10, 
                        chapa_ponto_init[1] + self.lc.magnitude - self.e.magnitude), 
                    
                    xytext=(chapa_ponto_init[0] + self.Conectante.lc.magnitude + 10,
                            chapa_ponto_init[1] + self.lc.magnitude), 
                    arrowprops={'arrowstyle': '<->'})
        
        self.ax.text(chapa_ponto_init[0] + self.Conectante.lc.magnitude + 12, 
                        (chapa_ponto_init[1] +  self.lc.magnitude - self.e.magnitude/2), 
                                                f'{round(self.e.magnitude,2)}', ha='left', va='center',rotation=90)        
                
        for i in range(int(self.n_ps/2 - 1)):
                
            self.ax.annotate('', 
                    xy=(chapa_ponto_init[0] + self.Conectante.lc.magnitude+10, 
                        chapa_ponto_init[1] + self.e.magnitude + self.s.magnitude*i), 
                    
                    xytext=(chapa_ponto_init[0] + self.Conectante.lc.magnitude + 10,
                            chapa_ponto_init[1] + self.e.magnitude + self.s.magnitude*(i+1)), 
                    arrowprops={'arrowstyle': '<->'})
        
            self.ax.text(chapa_ponto_init[0] + self.Conectante.lc.magnitude + 12, 
                        (chapa_ponto_init[1] + self.e.magnitude + (((i)*2 + 1)*self.s.magnitude)/2), 
                                                f'{round(self.s.magnitude,2)}', ha='left', va='center',rotation=90)
        
        #--------------------------------NOMENCLATURA DA CHAPA-------------------------------------------------
        
              
        self.ax.annotate('', 
                    xy=(chapa_ponto_init[0] + self.Conectante.lc.magnitude/2, 
                        chapa_ponto_init[1] + 10), 
                    
                    xytext=(chapa_ponto_init[0] + self.Conectante.lc.magnitude/2 + 25,
                            chapa_ponto_init[1] + 10 - self.TAMANHO/3 + 50), 
                    arrowprops={'arrowstyle': '->'})
        
        self.ax.text(chapa_ponto_init[0] + self.Conectante.lc.magnitude/2 + 25, 
                        (chapa_ponto_init[1] + 10 - self.TAMANHO/3 + 50), 
                                                f'{self.Conectante.name}', ha='left', va='center')       
        
        
        #self.ax.set_aspect('equal')
        self.ax.axis('off')
        if show:
                plt.show() # if you need...
        
        return self.ax

    
    def platePlot(self, ax=0, show=False):
        unit.setup_matplotlib()
        
        # Tamanho da imagem - dos eixos 
        width = (self.Conectante.lc.magnitude + self.Viga.tw.magnitude)*1.45
        height = (self.Conectante.lc.magnitude + self.Viga.tw.magnitude)*1.45
        
        if ax == 0:
                fig, ax = plt.subplots(figsize=(8, 6))
        
        # Defindo os limites dos eixos
        #ax.set_xlim(0, width)  
        #ax.set_ylim(0, height)  
        
        for e, anchor_conectante in enumerate([(width/2 - self.Viga.tw.magnitude/2 - self.Conectante.lc.magnitude ),(width/2 + self.Viga.tw.magnitude/2)]):
                
                rect = patches.Rectangle((anchor_conectante, height/2 - self.Conectante.lc.magnitude/2), 
                                        self.Conectante.lc.magnitude, self.Conectante.lc.magnitude, edgecolor='black', facecolor='#D3D3D3')
                ax.add_patch(rect)  
                
                if e == 0:
                        anchor = anchor_conectante + self.Conectante.lc.magnitude - self.Conectante.t_ch.magnitude
                else:
                        anchor = anchor_conectante
                
                aba = patches.Rectangle((anchor, height/2 - self.Conectante.lc.magnitude/2), 
                                        self.Conectante.t_ch.magnitude, self.Conectante.lc.magnitude, edgecolor='black', facecolor='#a9a9a9')
               
                ax.add_patch(aba)  
        
        for i in range(int(self.n_ps*0.5)):
                # Definindo as coordenadas do centro de cada furo
                x_d = width/2 + self.Viga.tw.magnitude/2 + self.Conectante.lc.magnitude - self.e.magnitude
                
                x_e = width/2 - self.Viga.tw.magnitude/2 - self.Conectante.lc.magnitude + self.e.magnitude
                
                y = height/2 - self.Conectante.lc.magnitude/2  + self.e.magnitude + self.s.magnitude*i

                # Linha de centro e furo
                for x_i in [x_d, x_e]:
                        circle = plt.Circle((x_i, y), 
                                    self.d_h.magnitude/2, 
                                    edgecolor='black', 
                                    facecolor='white')
                
                        ax.add_patch(circle)
                        
                        # linha horizontal de centro
                        ax.plot([(x_i + self.d_h.magnitude/2) + self.d_h.magnitude/2*0.5 , 
                        (x_i - self.d_h.magnitude/2) - self.d_h.magnitude/2*0.5], 
                                [y, y], 
                                color='red', linestyle='-.', linewidth=1)
                        
                        # linha Vertical de centro
                        ax.plot([x_i , x_i], 
                        [(y + self.d_h.magnitude/2) + self.d_h.magnitude/2*0.5 , 
                        (y - self.d_h.magnitude/2) - self.d_h.magnitude/2*0.5  ], 
                                color='red', linestyle='-.', linewidth=1)
       
       
        # Definição das cotas intermediárias
        for i in range(int(self.n_ps/2 - 1)):
                
                ax.annotate('', 
                    xy=(width/2 + self.Viga.tw.magnitude/2 + self.Conectante.lc.magnitude*1.05, 
                        height/2 - self.Conectante.lc.magnitude/2 + self.e.magnitude + self.s.magnitude*i), 
                    
                    xytext=(width/2 + self.Viga.tw.magnitude/2 + self.Conectante.lc.magnitude*1.05,
                            height/2 - self.Conectante.lc.magnitude/2 + self.e.magnitude + self.s.magnitude*(i+1)), 
                    arrowprops={'arrowstyle': '<->'})
        
                ax.text(width/2 + self.Viga.tw.magnitude/2 + self.Conectante.lc.magnitude*1.06, 
                        (height/2 - self.Conectante.lc.magnitude/2 + self.e.magnitude + (((i)*2 + 1)*self.s.magnitude)/2), 
                                                f'{round(self.s.magnitude,2)}', ha='left', va='center',rotation=90)
        ax.set_aspect('equal')
        ax.axis('off')
        if show:
                plt.show()
        return ax
    
    
    def AngleCrush(self):
        '''
        Status Verificado
        -----------------
        
        Cálculo do pressão de contato do elemento conector para o conjunto de parafusos
        NBR880:2008. item 6.3.3.3
        '''
        return 2*super().plateCrush()
   
   
    def angleShear(self):
        ''' 
        Status Verificado
        -----------------
        
        Função para cálculo do cisalhamento da chapa de extermidade bruta e liquída
        '''
        
        return 2*super().plateShear()

