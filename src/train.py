import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import yaml
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from mlflow.models import infer_signature
import os

from sklearn.model_selection import train_test_split, GridSearchCV
from urllib.parse import urlparse

import mlflow

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MLFLOW_TRACKING_USERNAME = os.getenv("MLFLOW_TRACKING_USERNAME")
MLFLOW_TRACKING_PASSWORD = os.getenv("MLFLOW_TRACKING_PASSWORD")

if not all([MLFLOW_TRACKING_URI, MLFLOW_TRACKING_USERNAME, MLFLOW_TRACKING_PASSWORD]):
    raise EnvironmentError(
        "Defina as variaveis MLFLOW_TRACKING_URI, MLFLOW_TRACKING_USERNAME e MLFLOW_TRACKING_PASSWORD no ambiente."
    )

def hyperparameter_tuning(X_train, y_train, param_grid):
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    return grid_search

# Carregando os parâmetros do arquivo YAML
params = yaml.safe_load(open("params.yaml"))["train"]

def train(data_path, model_path, random_state, n_estimators, max_depth):
    data = pd.read_csv(data_path)
    X = data.drop(columns=["Outcome"])
    y = data["Outcome"]

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    with mlflow.start_run():
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
        signature = infer_signature(X_train, y_train)

        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [None, 5, 10],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }

        # Realizando a busca em grade para encontrar os melhores hiperparâmetros
        grid_search = hyperparameter_tuning(X_train, y_train, param_grid)

        # Pegando os melhores hiperparâmetros
        best_model = grid_search.best_estimator_

        # Predizendo e avaliando o modelo com os melhores hiperparâmetros
        y_pred = best_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Acurácia: {accuracy}")

        # Log de métricas adicionais
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_params({"best_n_estimators": grid_search.best_params_["n_estimators"],
                           "best_max_depth": grid_search.best_params_["max_depth"],
                           "best_min_samples_split": grid_search.best_params_["min_samples_split"],
                           "best_min_samples_leaf": grid_search.best_params_["min_samples_leaf"]})
        
        # Log da matriz de confusão e do relatório de classificação
        cm = confusion_matrix(y_test, y_pred)
        cr = classification_report(y_test, y_pred)

        mlflow.log_text(str(cm), "confusion_matrix.txt")
        mlflow.log_text(cr, "classification_report.txt")

        tracking_url_type_store = urlparse(MLFLOW_TRACKING_URI).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(best_model, "model", registered_model_name="Best Model")
        else:
            mlflow.sklearn.log_model(best_model, "model", signature=signature)

        # Salvando o modelo localmente
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        filename = model_path
        pickle.dump(best_model, open(filename, 'wb'))
        print(f"Modelo treinado e salvo em: {model_path}")

if __name__ == "__main__":
    train(params["data"], params["model"], params["random_state"], params["n_estimators"], params["max_depth"])
