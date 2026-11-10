import os
import joblib
import pandas as pd
from contracts import ProductionDataContract
from pydantic import ValidationError

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
    
    # 3. Validar o contrato de dados linha a linha (Pydantic)
    valid_records = []
    errors_count = 0
    
    for idx, row in df.iterrows():
        try:
            validated_row = ProductionDataContract(**row.to_dict())
            valid_records.append(validated_row.model_dump())
        except ValidationError as e:
            errors_count += 1
            print(f"[Aviso] Linha {idx} rejeitada pelo contrato de dados: {e}")
            
    if not valid_records:
        raise ValueError("Nenhum registo passou na validação do contrato de dados.")
        
    df_valid = pd.DataFrame(valid_records)
    print(f"✓ Validação concluída: {len(df_valid)} registos válidos, {errors_count} rejeitados.")
    
    # 4. Executar predições
    features = ['age', 'income', 'credit_score', 'debt_ratio']
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
