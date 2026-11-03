# 🏦 Fintech Credit Scoring — Observabilidade Contínua e Governança

Repositório desenvolvido para o Tech Challenge, focado na construção de pipelines de dados, validação de contratos rígidos, detecção de Data Drift, observabilidade operacional e governança de modelos de risco de crédito em Python 3.13.

---

## 📂 Estrutura do Projeto

```text
tech-challenge-fintech/
│
├── data/                  # Datasets de referência (treino) e produção (com drift)
├── docs/                  # Documentação técnica de métricas e governança
├── models/                # Modelos treinados (.pkl)
├── reports/               # Relatórios HTML (Drift e Dashboard) e métricas JSON
├── src/                   # Scripts principais (contratos, treino, inferência e observabilidade)
├── venv/                  # Ambiente virtual isolado (ignorado pelo git)
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação oficial do projeto
```
PowerShell
## 1. Clonar o repositório e entrar na pasta do projeto
```text
cd tech-challenge-fintech-main
```

## 2. Criar o ambiente virtual (venv) isolado
```text
python -m venv venv
```

## 3. Ativar o ambiente virtual
```text
.\venv\Scripts\Activate.ps1
```

## 4. Atualizar o pip e instalar todas as dependências exigidas
```text
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## 🛡️ Etapa 1 — Validação de Dados, Contratos e Modelo Baseline
🎯 Objetivo
Garantir a integridade dos dados na camada de ingestão (Data Quality First) através da definição de contratos rígidos, impedindo que dados inconsistentes ou anômalos alimentem o modelo de Credit Scoring.

📜 Contrato de Dados (src/contracts.py)
Utilizamos a biblioteca Pandera para definir o esquema estrito de validação do lote de dados de entrada:

Idade (age): Inteiros obrigatórios entre 18 e 120 anos (ge=18, le=120). Garante a elegibilidade legal para concessão de crédito.

Renda (income): Valor numérico contínuo estritamente maior que zero (gt=0), não sendo permitidos valores nulos (nullable=False).

Score de Crédito (credit_score): Padrão FICO/Serasa variando entre 300 e 850 (ge=300, le=850).

Valor do Empréstimo (loan_amount): Valor solicitado estritamente maior que zero (gt=0).

Tipagem e Colunas Estritas: Ativação da flag strict=True, que rejeita colunas não mapeadas no contrato para evitar contaminação do dataset.
🤖 Modelo Baseline de Risco (src/train.py)
Algoritmo: XGBClassifier (XGBoost).

Dataset de Referência: Gerado/Limpo com 5.000 amostras sintéticas representando o cenário ideal de treino (data/reference_data.csv).

Métrica de Desempenho: ROC-AUC ~0.82.

Artefato: Modelo treinado e serializado salvo em models/baseline_model.pkl.

🚨 Simulação de Interceptação / Bloqueio (src/validate_ingestion.py)
Para comprovar o funcionamento do contrato, simulamos a entrada de um lote corrompido (data/corrupted_data.csv) contendo clientes menores de idade, renda nula/negativa e score inválido.

Resultado Esperado: O pipeline dispara a exceção pa.errors.SchemaErrors, interrompendo o fluxo e garantindo que nenhum dado inconsistente chegue à camada de predição.



