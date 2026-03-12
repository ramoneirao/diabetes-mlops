### Projeto: Pipeline de Dados com DVC e MLflow para Machine Learning
Este projeto demonstra como construir um pipeline completo de machine learning usando DVC (Data Version Control) para versionamento de dados e modelos, e MLflow para rastreamento de experimentos. O pipeline é focado no treinamento de um Random Forest Classifier com o conjunto de dados Pima Indians Diabetes, com etapas claras de pré-processamento, treinamento e avaliação.

Principais características do projeto:
Data Version Control (DVC):

O DVC é usado para rastrear e versionar o dataset, os modelos e as etapas do pipeline, garantindo reprodutibilidade em diferentes ambientes.
O pipeline é estruturado em etapas (pré-processamento, treinamento e avaliação) que podem ser reexecutadas automaticamente se qualquer dependência mudar (por exemplo, dados, scripts ou parâmetros).
O DVC também permite armazenamento remoto de dados (por exemplo, DagsHub, S3) para datasets e modelos grandes.
Rastreamento de experimentos com MLflow:

O MLflow é usado para rastrear métricas, parâmetros e artefatos dos experimentos.
Ele registra os hiperparâmetros do modelo (por exemplo, n_estimators, max_depth) e métricas de desempenho como acurácia.
O MLflow ajuda a comparar diferentes execuções e modelos para otimizar o pipeline de machine learning.
Etapas do pipeline:
Pré-processamento:

O script preprocess.py lê o dataset bruto (data/raw/data.csv), realiza um pré-processamento básico (como renomear colunas) e salva os dados processados em data/processed/data.csv.
Essa etapa garante que os dados sejam processados de forma consistente entre execuções.
Treinamento:

O script train.py treina um Random Forest Classifier com os dados pré-processados.
O modelo é salvo em models/random_forest.pkl.
Os hiperparâmetros e o próprio modelo são registrados no MLflow para rastreamento e comparação.
Avaliação:

O script evaluate.py carrega o modelo treinado e avalia seu desempenho (acurácia) no dataset.
As métricas de avaliação são registradas no MLflow para rastreamento.
Objetivos:
Reprodutibilidade: ao usar DVC, o pipeline garante que os mesmos dados, parâmetros e código possam reproduzir os mesmos resultados, tornando o fluxo de trabalho confiável e consistente.
Experimentação: o MLflow permite que usuários rastreiem facilmente diferentes experimentos (com hiperparâmetros variados) e comparem o desempenho dos modelos.
Colaboração: DVC e MLflow permitem colaboração fluida em equipe, onde diferentes pessoas podem trabalhar no mesmo projeto e rastrear mudanças de forma integrada.
Casos de uso:
Equipes de Data Science: equipes podem usar esta estrutura de projeto para rastrear datasets, modelos e experimentos de forma reprodutível e organizada.
Pesquisa em Machine Learning: pesquisadores podem iterar rapidamente em diferentes experimentos, rastrear métricas de desempenho e gerenciar versões de dados com eficiência.
Stack de tecnologias:
Python: linguagem principal para processamento de dados, treinamento e avaliação de modelos.
DVC: para controle de versão de dados, modelos e etapas do pipeline.
MLflow: para registro e rastreamento de experimentos, métricas e artefatos de modelo.
Scikit-learn: para construir e treinar o Random Forest Classifier.
Este projeto demonstra como gerenciar o ciclo de vida de um projeto de machine learning, garantindo que dados, código, modelos e experimentos sejam rastreados, versionados e reprodutíveis.

### Para adicionar etapas

dvc stage add -n preprocess \
    -p preprocess.input,preprocess.output \
    -d src/preprocess.py -d data/raw/data.csv \
    -o data/processed/data.csv \
    python src/preprocess.py
	
	
dvc stage add -n train \
    -p train.data,train.model,train.random_state,train.n_estimators,train.max_depth \
    -d src/train.py -d data/raw/data.csv \
    -o models/model.pkl \
    python src/train.py
	
dvc stage add -n evaluate \
    -d src/evaluate.py -d models/model.pkl -d data/raw/data.csv \
    python src/evaluate.py
