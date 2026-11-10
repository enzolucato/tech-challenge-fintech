import os
import joblib
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from numpy.random import default_rng


def generate_production_data(ref_df: pd.DataFrame) -> pd.DataFrame:
    prod_df = ref_df.copy()
    rng = default_rng(seed=42)

    if "income" in prod_df.columns:
        prod_df["income"] = prod_df["income"] * rng.uniform(
            1.3, 1.8, size=len(prod_df)
        )

    if "age" in prod_df.columns:
        prod_df["age"] = (
            prod_df["age"] + rng.integers(10, 25, size=len(prod_df))
        ).clip(18, 100)

    return prod_df


def main():
    print("--- Executando Etapa 2: Simulação e Detecção de Drift ---")

    ref_path = os.path.join("data", "reference_data.csv")
    model_path = os.path.join("models", "baseline_model.pkl")

    if not os.path.exists(ref_path) or not os.path.exists(model_path):
        print("✗ Erro: Arquivos de referência ou modelo não encontrados.")
        return

    ref_df = pd.read_csv(ref_path)
    model = joblib.load(model_path)

    # 1. Dataset de Produção
    prod_df = generate_production_data(ref_df)
    prod_path = os.path.join("data", "production_data.csv")
    prod_df.to_csv(prod_path, index=False)
    print(f"✓ Dataset de Produção gerado em: '{prod_path}'")

    # 2. Predições
    features = [col for col in ref_df.columns if col != "target"]
    ref_df["prediction"] = model.predict(ref_df[features])
    prod_df["prediction"] = model.predict(prod_df[features])

    # 3. Teste Estatístico de Drift (Kolmogorov-Smirnov)
    drift_results = []
    for col in features:
        stat, p_value = ks_2samp(ref_df[col], prod_df[col])
        has_drift = p_value < 0.05
        drift_results.append(
            {
                "Feature": col,
                "KS-Statistic": round(stat, 4),
                "p-value": round(p_value, 6),
                "Drift Detectado": "SIM ⚠️" if has_drift else "NÃO",
            }
        )

    drift_df = pd.DataFrame(drift_results)

    # 4. Salvar Relatório HTML
    os.makedirs("reports", exist_ok=True)
    report_output = os.path.join("reports", "data_drift_report.html")

    html_content = f"""
    <html>
    <head>
        <title>Relatório de Data Drift - Tech Challenge</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; }}
            h1 {{ color: #1a365d; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #2b6cb0; color: white; }}
            tr:nth-child(even) {{ background-color: #f7fafc; }}
        </style>
    </head>
    <body>
        <h1>Relatório de Detecção de Data Drift (KS-Test)</h1>
        <p>Abaixo estão os resultados do teste estatístico comparando o Dataset de Referência e Produção:</p>
        {drift_df.to_html(index=False)}
    </body>
    </html>
    """

    with open(report_output, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("\n--- Resultados do Drift ---")
    print(drift_df.to_string(index=False))
    print(f"\n✓ Relatório HTML salvo em: '{report_output}'")


if __name__ == "__main__":
    main()