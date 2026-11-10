## 🏦 Fintech Credit Scoring — Observabilidade Contínua e Governança

Repositório desenvolvido para o Tech Challenge, focado na construção de pipelines de dados, validação de contratos rígidos, detecção de Data Drift, observabilidade operacional e governança de modelos de risco de crédito em Python 3.13.

---

### 📂 Estrutura do Projeto

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

### 1. Clonar o repositório e entrar na pasta do projeto
```text
cd tech-challenge-fintech-main
```

### 2. Criar o ambiente virtual (venv) isolado
```text
python -m venv venv
```

### 3. Ativar o ambiente virtual
```text
.\venv\Scripts\Activate.ps1
```

### 4. Atualizar o pip e instalar todas as dependências exigidas
```text
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## 🛡️ Etapa 1 — Validação de Dados, Contratos e Modelo Baseline

### 🎯 Objetivo

Garantir a integridade dos dados na camada de ingestão (Data Quality First) através da definição de contratos rígidos, impedindo que dados inconsistentes ou anômalos alimentem o modelo de Credit Scoring.

### 📜 Contrato de Dados (src/contracts.py)

Utilizamos a biblioteca Pandera para definir o esquema estrito de validação do lote de dados de entrada:

Idade (age): Inteiros obrigatórios entre 18 e 120 anos (ge=18, le=120). 

Garante a elegibilidade legal para concessão de crédito.

Renda (income): Valor numérico contínuo estritamente maior que zero (gt=0), não sendo permitidos valores nulos (nullable=False).

Score de Crédito (credit_score): Padrão FICO/Serasa variando entre 300 e 850 (ge=300, le=850).

Valor do Empréstimo (loan_amount): Valor solicitado estritamente maior que zero (gt=0).

Tipagem e Colunas Estritas: Ativação da flag strict=True, que rejeita colunas não mapeadas no contrato para evitar contaminação do dataset.

🤖 Modelo Baseline de Risco (src/train.py)

Algoritmo: XGBClassifier (XGBoost).

Dataset de Referência: Gerado/Limpo com 5.000 amostras sintéticas representando o cenário ideal de treino (data/reference_data.csv).

Métrica de Desempenho: ROC-AUC ~0.82.

Artefato: Modelo treinado e serializado salvo em models/baseline_model.pkl.

### 🚨 Simulação de Interceptação / Bloqueio (src/validate_ingestion.py)
Para comprovar o funcionamento do contrato, simulamos a entrada de um lote corrompido (data/corrupted_data.csv) contendo clientes menores de idade, renda nula/negativa e score inválido.

## 📈 Etapa 2 — Simulação de Produção e Detecção de Data Drift

### 🛠️ Execução da Simulação (src/drift_simulation.py)

Simulamos um ambiente de produção contendo 5.000 amostras com alteração no perfil socioeconômico dos solicitantes (induzindo drift nas variáveis age e income).Teste Estatístico: Kolmogorov-Smirnov (KS-Test).Limiar de Decisão: $p\text{-value} < 0.05$.Artefato Gerado: Relatório interativo em reports/data_drift_report.html.

```text
python src/train.py
python src/drift_simulation.py
```
Resultado Esperado: O pipeline dispara a exceção pa.errors.SchemaErrors, interrompendo o fluxo e garantindo que nenhum dado inconsistente chegue à camada de predição.

## 🔍 Etapa 3 — Observabilidade de Pipelines, Infraestrutura e Modelos

Centralizamos os logs, as métricas operacionais e a saúde do pipeline, garantindo a visibilidade completa do sistema em produção.

### 🚀 Execução no Terminal
Com o ambiente virtual (venv) ativo, execute os scripts de inferência e observabilidade:
```text
python src/inference.py
python src/observability.py
```
Isso gera automaticamente:

O ficheiro JSON de métricas em reports/observability_metrics.json.

Isso gera automaticamente:

O ficheiro JSON de métricas em reports/observability_metrics.json.

O painel interativo de observabilidade em reports/observability_dashboard.html.

### 📊 Evidências Visuais e Dashboards
Para visualizar os dashboards interativos no seu navegador:

Abra o Explorador de Ficheiros do Windows e navegue até a pasta reports/.

Dê duplo clique em qualquer um dos ficheiros HTML:

observability_dashboard.html (Painel de Saúde da Infraestrutura, Latência, Alertas e Volume).

data_drift_report.html (Relatório detalhado do Teste KS para age e income).

1. Painel de Observabilidade & Saúde do Pipeline
<img width="795" height="534" alt="image" src="https://github.com/user-attachments/assets/fb39261f-98c4-4f15-941b-be3fe1ab0a52" />


2. Relatório de Detecção de Data Drift (KS-Test)
<img width="1222" height="361" alt="image" src="https://github.com/user-attachments/assets/9b55afe1-7ff5-43e5-b2d4-71fe74ed80a8" />


O painel interativo de observabilidade em reports/observability_dashboard.html.

## 🔒 Etapa 4 — Governança, Privacy by Design e Compliance (LGPD)

Em conformidade com as diretrizes de Privacy by Design e Privacy by Default, este projeto foi arquitetado para garantir a máxima segurança, privacidade e conformidade regulatória no tratamento de dados para análise de risco de crédito, alinhado à Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018).

**1.** Tratamento de Dados Pessoais e PII (Personally Identifiable Information)
   
Minimização de Dados (Data Minimization): 
O pipeline processa exclusivamente atributos estritamente necessários para a tomada de decisão financeira (age, income, credit_score, loan_amount), evitando a recolha excessiva ou desnecessária de dados pessoais.

Anonimização e Pseudonimização: 
Os conjuntos de dados utilizados nos ambientes de referência (treino) e produção (inferência) são desidentificados (sem nomes, CPFs, e-mails ou moradas), mitigando o risco de exposição de PII.

**2.** Base Legal para a Decisão de Crédito
   
Proteção ao Crédito e Execução de Contrato:
O tratamento dos dados e a execução do modelo preditivo fundamentam-se no artigo 7º, inciso V (execução de contrato ou procedimentos preliminares) e no artigo 7º, inciso X (proteção ao crédito) da LGPD.

Direito à Explicabilidade:
Como o modelo implementado baseia-se em algoritmos auditáveis (XGBoost/Scikit-Learn), a instituição garante a transparência nos critérios de aprovação ou recusa de crédito, atendendo ao direito de revisão de decisões automatizadas.

**3.** Plano de Retenção e Ciclo de Vida dos Dados

Limitação do Armazenamento: 
Os dados de produção e os logs operacionais são mantidos apenas pelo período estritamente necessário para a auditoria do modelo e monitoramento de Data Drift.

Descarte Seguro:
Ficheiros temporários e artefactos sensíveis são gerados em diretórios locais controlados e isolados do versionamento público através de regras restritivas no .gitignore.




