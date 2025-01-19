import streamlit as st
import time 
import random

st.set_page_config(layout="wide")



def generate_progress_bar(progress:int, total=100, length=25)->str:
    '''
    Gera a barra de progresao de carregamento
    progress: progresso atual da barra
    total: valor máximo
    legth: tamanho da barra de carregamento
    return: str
    '''
    
    filled_length = int(length * progress // total)
    bar = '#' * filled_length + '-' * (length - filled_length)
    return f"|{bar}| {progress}%"


models = ['1']

col1, col2 = st.columns(2)

with col1:
    TRAIN_MODE = st.toggle('Train')

    option = st.selectbox(
        "Modelos disponíveis",
        models,
    )


    if TRAIN_MODE:
        metric_1, metric_2, metric_3 = st.columns(3)
        col3, col4 = st.columns(2)
        # Configurações do treinamento - Hiper parâmetros
        
        with metric_1:
            st.metric(label="Dados Disponíveis", value="200")
        with metric_2:
            st.metric(label="Classes", value="1" )
        with metric_3:
            pass


        
        st.caption("This is a string that explains something above.")
        with col3:
            batch_size = st.number_input("Batch Size", value=None, placeholder="Type a number...")
            
        with col4:
            epoch_number = st.number_input("Quantidade de Epocas", value=None, placeholder="Type a number...")
        
        pass
    
    else:
        uploaded_files = st.file_uploader(
        "Carregue a imagem", accept_multiple_files=True
    )
        # Mostrando imagem carregada
        if uploaded_files:
            st.image('')

start = st.button('Run')


with col2:
    if TRAIN_MODE:
        ## Carregar status de treinamento
        if start:
            st.toast('Iniciando o treinamento ⌛')
            with st.status("Treinamento...", expanded=True) as status:
                st.write("📦 Empacotando conteúdos...")
                time.sleep(2)
                st.write("🔍 Verificando Imagens...")
                time.sleep(10)
                st.write("📂 Definindo batchs...")
                time.sleep(2)
                st.write('🧠 Preparando a rede neural...')
                for _ in range(epoch_number):
                    with st.empty():

                        for i in range(5):
                            
                            #texto variando do carregamento
                            st.write(f'⏳ Treinamento época {_+1} {generate_progress_bar(100/5*i)}')
                            time.sleep(2)
                            
                        #texto final apos carregar  
                        st.write(f"✔ Treinando época {_+1}:   loss: {limite_inferior_loss:.2f}      accurary: {limite_inferior_accuracy:.2f}")
                        
                        limite_inferior_loss = random.uniform(limite_inferior_loss,1)
                        limite_inferior_accuracy = random.uniform(limite_inferior_accuracy,1)
                
                st.write('🔄Atualizando modelo...')
                time.sleep(5)
                
                
                status.update(label="Treinamento concluido", state="complete", expanded=False)
                st.toast('Treinamento realizado com Sucesso✅')
    else:
        ## Carregar resultado
        if uploaded_files and start:
            st.image()
        


