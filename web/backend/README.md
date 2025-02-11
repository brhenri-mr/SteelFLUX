# Objetivo

Acesso aos modelos treinados/campeões do MLFlow. O BackEnd será responsável apenas
pela interação entre usuário e modelo no MLFlow. Não sendo seu papel o TREINAMENTO de modelo ou CADASTRO de novos modelos. A principio seu papel é unicamente a predição dos valores já existente no servidor do MLFLOW


## Auth

Router para controlar os cadastro da api

- [x] Cadastro de modelos novos
- [-] Compatiblização com o Huggienface

## Predict

Router para previsão de modelos especificios

Previsão do modelo

- [-] Integração com o banco de dados
- [-] API para o hugginface
- [-] Acesso a modelos via MLflow

## Status
Demonstra os status da aplicação

- [x] Baixar log
- [x] Status de modelos especifico
- [x] Status de modelo que treina 
- [-] Status em tempo real

## Train

Router para treinamentodos diferentes modelos

- [x] Sistema de log
- [x] Sistema de cadastro do modelo
- [-] Acesso ao banco de dados dee treino (outro arquivo)
- [-] Treinamento do modelo
- [-] Arquivamento de pesos

## Utils.log

Inicializa o arquivo de log -- TALVEZ SEJA DELETADO

- [x] Cabeçalho automático
- [x] Caminho automático
- [x] Adapta a diferentes hiperparâmtros