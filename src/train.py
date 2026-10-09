import joblib
import numpy as np
import pandas as pd
from contracts import CreditDataContract
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


def generate_reference_dataset(n_samples: int = 5000) -> pd.DataFrame:
    """Gera um dataset sintético limpo representando o cenário ideal de treino."""
    np.random.seed(42)

    age = np.random.randint(18, 70, size=n_samples)
    income = np.random.normal(5500, 1800, size=n_samples).clip(1200, 25000)
    credit_score = np.random.randint(350, 850, size=n_samples)
    loan_amount = np.random.normal(12000, 5000, size=n_samples).clip(1000, 50000)

    # Probabilidade de default com regras lógicas
    p_default = 1 / (
        1
        + np.exp(
            -(
                0.03 * (60 - age)
                - 0.0004 * income
                - 0.008 * credit_score
                + 0.0001 * loan_amount
                + 2.0
            )
        )
    )
    target = (np.random.rand(n_samples) < p_default).astype(int)

    df = pd.DataFrame(
        {
            "age": age,
            "income": income,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "target": target,
        }
    )
    return df


def main():
    print("--- 1. Gerando Dataset de Referência Limpo ---")
    df_ref = generate_reference_dataset(n_samples=5000)
    df_ref.to_csv("data/reference_data.csv", index=False)

    print("--- 2. Validando Dataset de Referência com o Contrato ---")
    try:
        df_ref_validated = CreditDataContract.validate(df_ref)
        print("✓ Dataset de Referência aprovado no contrato de dados!")
    except Exception as e:
        print(f"✗ Falha na validação do dataset de referência: {e}")
        return

    print("--- 3. Treinando Modelo Baseline (XGBoost) ---")
    X = df_ref_validated.drop(columns=["target"])
    y = df_ref_validated["target"]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=100, max_depth=4, learning_rate=0.05, random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_val)
    probs = model.predict_proba(X_val)[:, 1]

    print(f"ROC-AUC: {roc_auc_score(y_val, probs):.4f}")
    print("\nRelatório de Classificação:\n", classification_report(y_val, preds))

    # Salva o modelo treinado
    joblib.dump(model, "models/baseline_model.pkl")
    print("✓ Modelo salvo em 'models/baseline_model.pkl'")


if __name__ == "__main__":
    main()