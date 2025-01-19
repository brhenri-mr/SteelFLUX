import streamlit as st

st.set_page_config(layout="wide")

st.title('Introdução')

st.markdown('''
            Aplicação feita para treinamento e testes de modelos de inteligência artificial generativa de imagem para a tese de Mestrado de Breno Henrique Mariano Rodrigues.
        Quantidade já concluida     ''')


col1, col2 = st.columns(2)
with col1:
    st.markdown('''
                ### Frontend
                ''')

    st.progress(80, text='80%')
    
with col2:
    st.markdown('''
                ### BackEnd
                ''')

    st.progress(0, text='0%')

st.header('Conteúdos')
st.markdown('''
           Modelos de inteligência artifical já implementados
           ''')

for element in ["GAN","Stable Diffusor","Flux"]:
    st.checkbox(element, value=False, disabled=True)


