import cv2
import os 
import glob



def mask_generate(nome_arquivo:str, path=r'dataset/img', EXT='png'):
    '''
    Generate uma única mask para uma imagem
    
    Parameters
    ----------
    nome_arquivo: str
        Nome do arquivo 
    
    Return
    ------
    
    ret: bool
    valor boleano que indica se a tarefa foi concluida
    '''
    # Caminho para o arquivo
    arquivo = os.path.join(path,f'{nome_arquivo}.{EXT}')
    
    color = (0,0,0) # Black
    
    # Points
    start_point = (300+20, 260) 
    end_point = (300+150, 500)
    
    # Verificando se o arquivo existe
    if os.path.isfile(arquivo):
        # Carregando a imagem
        img = cv2.imread(arquivo)
        
        # Desenhando o retangulo preto
        new_img = cv2.rectangle(img, start_point, end_point, color=color, thickness=-1 )
        
        # Salvando a imagem
        cv2.imwrite(os.path.join(r'dataset/img_mask', f'{nome_arquivo}.{EXT}'), new_img)
    
        return 1
    else:
        return False
    
def mask_all():
    '''
    Função que gera uma maskara para todas as imagens de uma pasta
    '''
    return 2

if __name__ == '__main__':
    mask_generate(nome_arquivo='Test1')