import pandas as pd
import sys
import yaml 
import os 

# Carregando os parâmetros do arquivo YAML
params = yaml.safe_load(open("params.yaml"))["preprocess"]

def preprocess(input_path, output_path):
    data = pd.read_csv(input_path)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_csv(output_path, index=False, header=None)
    print(f"Dados pré-processados salvos em: {output_path}")


if __name__ == "__main__":
    preprocess(params["input"], params["output"])
