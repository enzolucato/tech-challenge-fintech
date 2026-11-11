import os
import joblib
import pandas as pd
from contracts import CreditDataContract

def run_inference():
    print("--- Iniciando Pipeline de Inferência e Validação de Contrato ---")
    
    # 1. Carregar o modelo treinado
    model_path = "models/baseline_model.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em '{model_path}'. Certifique-se de executar o treino primeiro.")
    
    model = joblib.load(model_path)
    print(f"✓ Modelo carregado com sucesso de '{model_path}'")
    
    # 2. Carregar dados de produção/inferência
    data_path = "data/production_data.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dados de produção não encontrados em '{data_path}'.")
    
    df = pd.read_csv(data_path)
    print(f"✓ Dados carregados: {len(df)} amostras encontradas.")
    print(f"✓ Colunas disponíveis no dataset: {list(df.columns)}")
    
    # 3. Validar o contrato de dados com Pandera
    try:
        df_valid = CreditDataContract.validate(df, lazy=True)
        print(f"✓ Validação de contrato concluída com sucesso: {len(df_valid)} registos válidos.")
    except Exception as e:
        print(f"[Erro] Falha na validação do contrato de dados: {e}")
        raise e
    
    # 4. Definir dinamicamente as features esperadas pelo modelo base
    # Mapeia as colunas comuns do modelo de crédito
    possible_features = ['age', 'income', 'credit_score', 'debt_ratio', 'dti', 'debt-to-income']
    features = [col for col in possible_features if col in df_valid.columns]
    
    # Se o modelo foi treinado com uma ordem específica ou número fixo, garantimos as colunas
    print(f"✓ Utilizando features para inferência: {features}")
    X = df_valid[features]
    
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba") else [None] * len(predictions)
    
    df_valid['prediction'] = predictions
    df_valid['default_probability'] = probabilities
    
    # 5. Guardar os resultados da inferência
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "inference_results.csv")
    df_valid.to_csv(output_path, index=False)
    
    print(f"✓ Inferência concluída com sucesso! Resultados guardados em '{output_path}'.")
    return df_valid

if __name__ == "__main__":
    run_inference()
