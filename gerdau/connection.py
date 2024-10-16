import numpy as np
from gerdau.unit import unit
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from gerdau.plot import breakline

class EndPLate:
    
    def __init__(self,
                 Conector, 
                 Plate, 
                 Viga,
                 Coluna, 
                 n_ps:int,
                 s:float,
                 g_ch:float,
                 Dimension_unit='millimeter',
                 Result_unit='kilonewton',
                 coef=1.35) -> None:
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
        
        '''
        # Classes
        self.Chapa = Plate
        self.Viga = Viga
        self.Parafuso = Conector
        self.Coluna = Coluna
        
        # Dados
        self.d_h = Conector.d_b + 1.5*unit['millimeter'] # Diametro de furo
        self.s = s*unit[Dimension_unit] # Distancia entre centroide de furo interno
        self.e = (Viga.h - (n_ps/2 -1)*s*unit[Dimension_unit])/2 # Distancia entre centro do furo e borda
        self.g_ch = g_ch*unit[Dimension_unit] # Distancia entre linhas de parafusos
        
        # Dimensoes
        self.Dimension_unit = Dimension_unit
        self.Result_unit = Result_unit

        # Admensional
        self.n_ps = n_ps # Quantidade de parafusos
        self.coef = coef
        self.coef1 = 1.1

        self.TAMANHO = 300

    def platePlot(self):
        # Criar uma figura e eixos
        unit.setup_matplotlib()
        
        # Tamanho da imagem - dos eixos 
        width = self.Chapa.c.magnitude*1.2
        height = self.Viga.h.magnitude*1.2
        
        # Ponto de ancoragem
        local_plate = (self.Chapa.c.magnitude*0.1, self.Viga.h.magnitude*0.1) # Chapa
        local_web = ((width - self.Viga.tw.magnitude)*0.5, self.Viga.h.magnitude*0.1) # Alma da viga
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Defindo os limites dos eixos
        ax.set_xlim(0, width)  
        ax.set_ylim(0, height)  
        
        # PLotagem da chapa
        rect = patches.Rectangle(local_plate, 
                                 self.Chapa.c.magnitude, self.Viga.h.magnitude, edgecolor='black', facecolor='#D3D3D3')
        ax.add_patch(rect)  
        
        # Plotagem da alma
        hatch_rect = patches.Rectangle(local_web, self.Viga.tw.magnitude, self.Viga.h.magnitude, edgecolor='black', facecolor='gray', hatch='//')
        ax.add_patch(hatch_rect)

        #--------------- Adicionar cota horizontal-----------------------------
        ax.annotate('', 
                    xy=(self.Chapa.c.magnitude*0.1, self.Viga.h.magnitude*0.03), 
                    xytext=(self.Chapa.c.magnitude*1.1, self.Viga.h.magnitude*0.03), 
                    arrowprops={'arrowstyle': '<->'})
        
        ax.text(width*0.5, self.Viga.h.magnitude*0.01, f'L = {self.Chapa.c.magnitude}', ha='center', va='center') 
        
        ax.annotate('', 
                    xy=(width/2 - self.g_ch.magnitude/2, self.Viga.h.magnitude*0.08), 
                    xytext=(width/2 + self.g_ch.magnitude/2, self.Viga.h.magnitude*0.08), 
                    arrowprops={'arrowstyle': '<->'})
        
        ax.text(width*0.5, self.Viga.h.magnitude*0.06, f'g_ch = {self.g_ch.magnitude}', ha='center', va='center') 
        

        
        
        #--------------------------------------- Adicionar cota Vertical-------------------------------------
        ax.annotate('', 
                    xy=(self.Chapa.c.magnitude*1.20, self.Viga.h.magnitude*0.1), 
                    xytext=(self.Chapa.c.magnitude*1.20, self.Viga.h.magnitude*1.1), 
                    arrowprops={'arrowstyle': '<->'})
        
        ax.text(self.Chapa.c.magnitude*1.21, height*0.5, f'{self.Viga.h.magnitude}', 
                                                                        ha='left', va='center', rotation=90)
        ## Definicao do e inferior
        ax.annotate('', 
                    xy=(self.Chapa.c.magnitude*1.15, self.Viga.h.magnitude*0.1), 
                    xytext=(self.Chapa.c.magnitude*1.15, self.Viga.h.magnitude*0.1 + self.e.magnitude), 
                    arrowprops={'arrowstyle': '<->'})
        
        ax.text(self.Chapa.c.magnitude*1.16, (self.Viga.h.magnitude*0.1 + 0.5*self.e.magnitude), 
                                                f'{self.e.magnitude}', ha='left', va='center',rotation=90)
        
        ## Definicao do e superior
        ax.annotate('', 
                    xy=(self.Chapa.c.magnitude*1.15, self.Viga.h.magnitude*1.1), 
                    xytext=(self.Chapa.c.magnitude*1.15, self.Viga.h.magnitude*1.1 - self.e.magnitude), 
                    arrowprops={'arrowstyle': '<->'})
        
        ax.text(self.Chapa.c.magnitude*1.16, (self.Viga.h.magnitude*1.1 - 0.5*self.e.magnitude), 
                                                f'{self.e.magnitude}', ha='left', va='center',rotation=90)
        
        # Definição das cotas intermediárias
        for i in range(int(self.n_ps/2 - 1)):
                
                ax.annotate('', 
                    xy=(self.Chapa.c.magnitude*1.15, 
                        self.Viga.h.magnitude*0.1 + self.e.magnitude + self.s.magnitude*i), 
                    
                    xytext=(self.Chapa.c.magnitude*1.15,
                            self.Viga.h.magnitude*0.1 + self.e.magnitude + self.s.magnitude*(i+1)), 
                    arrowprops={'arrowstyle': '<->'})
        
                ax.text(self.Chapa.c.magnitude*1.16, 
                        (self.Viga.h.magnitude*0.1 + self.e.magnitude + (((i)*2 + 1)*self.s.magnitude)/2), 
                                                f'{self.s.magnitude}', ha='left', va='center',rotation=90)
                
        
        #---------------------------------------------------------------------------------------------------
        
        # Adicionando corta vertical
        ax.annotate('', 
                    xy=(width*0.5, self.Viga.h.magnitude*1.1), 
                    xytext=(width*0.55,self.Viga.h.magnitude*1.15), 
                    arrowprops={'arrowstyle': '->'})
        
        ax.text(width*0.55, self.Viga.h.magnitude*1.15, f'{self.Viga.name}', ha='left', va='center',)
        
        
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
                

        # Deligando a moldura

        plt.axis('off')
        plt.show()


    def plotConnection(self):
        unit.setup_matplotlib()
        fig, ax = plt.subplots(figsize=(8, 6))
        
        
        parafuso_interno = int((self.n_ps/2 - 1))
        
        # -------------------------------Coluna Definição das Breakline-------------------------------
        for altura in [1, self.TAMANHO]:
                coord = list(zip(*breakline(-1, altura, 
                                            length=self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude)))
                plt.plot(coord[0],coord[1], color='black', linewidth=0.8)
        
        # -------------------------------Coluna Definição das mesas-------------------------------
        for offset in [0, self.Coluna.h.magnitude + self.Coluna.tf.magnitude]:
                
                mesa2 = patches.Rectangle((1 + offset,1), 
                                 self.Coluna.tf.magnitude, self.TAMANHO-1, edgecolor='black', facecolor='gray')
                ax.add_patch(mesa2)

        coluna = patches.Rectangle((1 + self.Coluna.tf.magnitude,1), 
                                 self.Coluna.h.magnitude, self.TAMANHO-1, edgecolor='black', facecolor='gray')
        ax.add_patch(coluna)
        
        # ---------------------------------Chapa-----------------------------------------------------
        rect = patches.Rectangle((self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1, self.TAMANHO/2 - self.Viga.h.magnitude/2 ), 
                                 self.Chapa.t_ch.magnitude, self.Viga.h.magnitude, edgecolor='black', facecolor='#D3D3D3')
        ax.add_patch(rect)
        # ---------------------------------VIGA-----------------------------------------------------
        mesa1 = patches.Rectangle((self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude, 
                                  self.TAMANHO/2 + self.Viga.h.magnitude/2), 
                                 100, self.Viga.tf.magnitude*1.6, edgecolor='black', facecolor='gray')
        ax.add_patch(mesa1)
        
        mesa2 = patches.Rectangle((self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude, 
                                  self.TAMANHO/2 - self.Viga.h.magnitude/2 - self.Viga.tf.magnitude*1.6 ), 
                                 100, self.Viga.tf.magnitude*1.6, edgecolor='black', facecolor='gray')
        ax.add_patch(mesa2)
        
        alma = patches.Rectangle((self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude, 
                                  self.TAMANHO/2 - self.Viga.h.magnitude/2), 
                                 100, self.Viga.h.magnitude, edgecolor='black', facecolor='gray')
        ax.add_patch(alma)
        
        # ----------------------------------------Furos-----------------------------------------------------
        
        furo = patches.Rectangle((self.Coluna.h.magnitude + self.Coluna.tf.magnitude + 1 , 
                                  self.TAMANHO/2 - self.Viga.h.magnitude/2 + self.e.magnitude - self.d_h.magnitude/2), 
                                 self.Coluna.tf.magnitude+self.Chapa.t_ch.magnitude, self.d_h.magnitude, edgecolor='black', facecolor='black')
        ax.add_patch(furo)
        
        furo = patches.Rectangle((self.Coluna.h.magnitude + self.Coluna.tf.magnitude + 1 , 
                                  self.TAMANHO/2 + self.Viga.h.magnitude/2 - self.e.magnitude - self.d_h.magnitude/2), 
                                 self.Coluna.tf.magnitude+self.Chapa.t_ch.magnitude, self.d_h.magnitude, edgecolor='black', facecolor='black')
        ax.add_patch(furo)
        
        for i in range(parafuso_interno-1):
                
                furo_interno = patches.Rectangle((
                                self.Coluna.h.magnitude + self.Coluna.tf.magnitude + 1 , 
                                self.TAMANHO/2 - self.Viga.h.magnitude/2 + self.e.magnitude - self.d_h.magnitude/2 + self.s.magnitude*(i+1)), 
                                self.Coluna.tf.magnitude+self.Chapa.t_ch.magnitude, 
                                self.d_h.magnitude, 
                                edgecolor='black', facecolor='black')
                ax.add_patch(furo_interno)
        
        
        ax.annotate('', 
                    xy=(self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude*0.5, 
                        self.TAMANHO/2 + self.Viga.h.magnitude/2 ), 
                    xytext=(self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude,
                            self.TAMANHO/2 + self.Viga.h.magnitude*0.65), 
                    arrowprops={'arrowstyle': '->'})
        ax.text(self.Coluna.h.magnitude + 2*self.Coluna.tf.magnitude + 1 + self.Chapa.t_ch.magnitude,
                self.TAMANHO/2 + self.Viga.h.magnitude*0.65, f'CH {self.Chapa.t_ch.magnitude}', ha='left', va='center',)
        
        
        plt.axis('off')
        plt.show() # if you need...


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


    def plateCrush(self) ->float:
        '''
        Status Verificado
        -----------------
        
        Cálculo do pressão de contato da chapa para o conjunto de parafusos
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

                crush = 2.4*self.Parafuso.d_b*self.Chapa.t_ch*self.Chapa.f_uc/self.coef
                if i == 0 or i == times - 1:
                        # Furo Externo
                        crush_hole = 1.2*(self.s - self.d_h)*self.Chapa.t_ch*self.Chapa.f_uc/self.coef
                else:
                        # Furo interna
                        crush_hole = 1.2*(self.e - 0.5*self.d_h)*self.Chapa.t_ch*self.Chapa.f_uc/self.coef
                
                saida.append(min(crush,crush_hole).to(self.Result_unit))   
                
        
        return sum(saida).to(self.Result_unit), saida


    def plateShear(self):
        ''' 
        Status Verificado
        -----------------
        
        Função para cálculo do cisalhametno da chapa de extermidade bruta e liquída
        
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
        ag = ((0.5*self.n_ps - 1)*self.s + 2*self.e)*self.Chapa.t_ch
        
        v_bruta = 2*0.6*self.Chapa.f_yc*ag/self.coef1
        
        # Resistência da seção liquída
        # Ver NBR 8800:2008 - Item 5.2.4.1
        anv = (self.n_ps*0.5*(self.d_h + 2*unit['millimeter'])*self.Chapa.t_ch)
         
        v_liquida = 2*0.6*self.Chapa.f_uc*(ag - anv)/self.coef
        
        
        return min(v_bruta, v_liquida).to(self.Result_unit)


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


    def plateBearing(self):
        '''
        Flexão da chapa de extremidade
        
        ATUALMENTE É UMA RECOMENDAÇÃO DA GERDAU, NÃO VEJO LOGICA EM TER RESISTÊNCIA DE PLACA DE FUNDO
        NO FINAL DE UMA VIGA QUE AINDA POR CIMA É FLEXÍVEL
        
        APARENTEMENTE O EUROCODE TEM ALGO--- VER
        
        '''
        
        l_fch = (0.5*self.n_ps - 1)*self.s + 2*self.e
        
        return (((4*self.Chapa.t_ch*l_fch**2)/(6*self.g_ch)*self.Chapa.f_yc)/self.coef1).to(self.Result_unit)

        
    def dunkerStability(self, v_d):
        '''
        Cálculo da envoltória da resistência pela interação de dunker
        VERIFICAR SE ISSO É UTIL DE VDD
        '''
        v_x = 1*unit[self.Result_unit]/unit['millimeter']
        l_fch = (0.5*self.n_ps - 1)*self.s + 2*self.e
        v_dm = v_d/2*unit[self.Result_unit]   
        v_z = v_dm/(2*l_fch)
        t_lich = v_z/(0.6*self.Chapa.f_yc/1.1)
        v_ox = 0.6*self.Chapa.f_yc*(self.Chapa.t_ch - t_lich)/1.1
        m_oz = 0.25*(self.Chapa.t_ch**2 - t_lich**2)*self.Chapa.f_yc/1.1
           
 
        
        for _ in range(100):
                 
                
                m_z = 0.25*v_x*(self.g_ch - self.Viga.tw)
                
                
                v_x = v_ox*(1 - m_oz/m_z)**(1/4)
        
        nd = 2*l_fch*v_x
        
        return m_z/m_oz + (v_x/v_ox)**4


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
        
        ## Caso 1
        # área de cisalhamento bruta
        a_gv = 2*((((self.n_ps) - 1) - 1)*self.s + self.e)*self.Chapa.t_ch
        
        # Área líquida interna
        a_nv_int = (self.n_ps/2 - 1)*((self.d_h +2*unit['millimeter'])*self.Chapa.t_ch)
        
        # Área líquida externa
        a_nv_ext = (0.5*(self.d_h +2*unit['millimeter'])*self.Chapa.t_ch)
        
        # Área líquida
        a_nv = a_gv - 2*(a_nv_ext - a_nv_int)
        
        # Área líquida de tração
        a_nt = 2*((0.5*(self.d_h +2*unit['millimeter'])*self.Chapa.t_ch) + self.Chapa.t_ch*(self.Chapa.c - self.g_ch )*0.5)
        
        # Cálculo da resistência de rasgamento para o caso 1
        f_rRd = min(0.6*self.Chapa.f_uc*a_nv + cts*self.Chapa.f_uc*a_nt,
                0.6*self.Chapa.f_yc*a_gv + cts*self.Chapa.f_uc*a_nt)
        
        
        ## Caso 2
        # Área líquida de tração
        a_nt = ((self.d_h +2*unit['millimeter'])*self.Chapa.t_ch) + self.Chapa.t_ch*(self.g_ch)
        
        # Cálculo da resistência de rasgamento para o caso 2
        f_rRd = min(0.6*self.Chapa.f_uc*a_nv + cts*self.Chapa.f_uc*a_nt,
                0.6*self.Chapa.f_yc*a_gv + cts*self.Chapa.f_uc*a_nt,
                f_rRd)
        
        # o CASO 3 ERA UM CASO A VER COM O RASGAMENTO ENTRE PARAFUSO NA ZONA EXTERNA, MAS NÃO
        #FAZ SENTIDO
        
        ## Caso 4
        
        # área de cisalhamento bruta
        a_gv = ((((self.n_ps) - 1) - 1)*self.s)*self.Chapa.t_ch
        
        # Área líquida interna
        a_nv_int = (self.n_ps/2 - 1)*((self.d_h + 2*unit['millimeter'])*self.Chapa.t_ch)
        
        # Área líquida externa
        a_nv_ext = (0.5*(self.d_h +2*unit['millimeter'])*self.Chapa.t_ch)
        
        # Área líquida
        a_nv = a_gv - (a_nv_ext - a_nv_int)
        
        # Área líquida de tração
        a_nt = ((0.5*(self.d_h +2*unit['millimeter'])*self.Chapa.t_ch) + self.Chapa.t_ch*((self.Chapa.c + self.g_ch)*0.5))
        
        # Cálculo da resistência de rasgamento para o caso 4
        f_rRd = min(0.6*self.Chapa.f_uc*a_nv + cts*self.Chapa.f_uc*a_nt,
                0.6*self.Chapa.f_yc*a_gv+ cts*self.Chapa.f_uc*a_nt,
                f_rRd)
        
        
        return (f_rRd/self.coef).to(self.Result_unit)

    def plateWelding(self):
        pass

 
if __name__ == '__main__':
    
    pass

