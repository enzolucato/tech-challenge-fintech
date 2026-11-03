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




