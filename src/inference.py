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
    
    # 3. Validar o contrato de dados com Pandera
    try:
        df_valid = CreditDataContract.validate(df, lazy=True)
        print(f"✓ Validação de contrato concluída com sucesso: {len(df_valid)} registos válidos.")
    except Exception as e:
        print(f"[Erro] Falha na validação do contrato de dados: {e}")
        raise e
    
    # 4. Definir as features exatas exigidas pelo modelo XGBoost treinado
    features = ['age', 'income', 'credit_score', 'loan_amount']
    
    # Verificar se todas as colunas existem no DataFrame
    missing_cols = [col for col in features if col not in df_valid.columns]
    if missing_cols:
        raise ValueError(f"As seguintes colunas exigidas pelo modelo estão em falta nos dados: {missing_cols}")
        
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
