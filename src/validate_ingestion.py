import pandas as pd
import pandera as pa
from contracts import CreditDataContract


def create_corrupted_batch() -> pd.DataFrame:
    """Cria um lote com anomalias intencionais para testar o bloqueio do contrato."""
    data = {
        "age": [25, 17, 45, 30, 80],  # 17 anos -> Erro: age < 18
        "income": [
            4500.0,
            3000.0,
            None,
            -500.0,
            6000.0,
        ],  # None e -500.0 -> Erro: Nulo e <= 0
        "credit_score": [700, 650, 500, 800, 200],  # 200 -> Erro: score < 300
        "loan_amount": [10000.0, 5000.0, 15000.0, 20000.0, 5000.0],
        "target": [None, None, None, None, None],
    }
    return pd.DataFrame(data)


def process_ingestion(df_batch: pd.DataFrame):
    print("\n--- Processando Lote de Ingestão ---")
    try:
        df_clean = CreditDataContract.validate(df_batch, lazy=True)
        print("✓ Lote aprovado. Enviando para o pipeline de predição...")
        return df_clean

    except pa.errors.SchemaErrors as err:
        print("🚨 BLOQUEIO DE INGESTÃO! Dados inválidos detectados pelo contrato:\n")
        failure_cases = err.failure_cases[
            ["schema_context", "column", "check", "failure_case"]
        ]
        print(failure_cases.to_string(index=False))
        print("\n--> Lote rejeitado e enviado para a fila de erro/Dead Letter Queue (DLQ).")
        return None


if __name__ == "__main__":
    df_corrupted = create_corrupted_batch()
    df_corrupted.to_csv("data/corrupted_data.csv", index=False)
    process_ingestion(df_corrupted)