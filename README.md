## 🏦 Fintech Credit Scoring — Observabilidade Contínua e Governança

Repositório desenvolvido para o Tech Challenge — Fase 4, focado na construção de pipelines de dados, validação de contratos rígidos, detecção de Data Drift, observabilidade operacional e governança de modelos de risco de crédito em Python 3.13.

O projeto utiliza **dados sintéticos** para simular um cenário de produção e demonstrar validação, inferência e monitoramento de mudanças na distribuição dos dados.

---

### 📂 Estrutura do Projeto

```text
tech-challenge-fintech/
│
├── data/                  # Datasets de referência, produção e lote corrompido
├── docs/                  # Documentação técnica de métricas
├── models/                # Modelos treinados (.pkl)
├── reports/               # Relatórios HTML, resultados de inferência e métricas JSON
├── src/                   # Contratos, treino, validação, inferência e observabilidade
├── venv/                  # Ambiente virtual isolado (ignorado pelo git)
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do projeto
```

### 1. Clonar o repositório e entrar na pasta do projeto

```powershell
git clone https://github.com/enzolucato/tech-challenge-fintech.git
cd tech-challenge-fintech
```

Se o projeto foi baixado como ZIP, entre na pasta extraída que contém diretamente `src/`, `data/` e `requirements.txt`. Nesse caso, o nome da pasta pode ser `tech-challenge-fintech-main`.

### 2. Criar o ambiente virtual (venv) isolado

```powershell
python -m venv venv
```

### 3. Ativar o ambiente virtual no Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Atualizar o pip e instalar todas as dependências

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

A integração do Evidently utiliza a dependência `evidently>=0.7,<0.8`, declarada no `requirements.txt`.

**Importante:** execute os comandos na raiz do projeto, com o ambiente virtual ativo.

---

## 🛡️ Etapa 1 — Validação de Dados, Contratos e Modelo Baseline

### 🎯 Objetivo

Garantir a qualidade dos dados na camada de ingestão (Data Quality First), utilizando contratos rígidos para rejeitar entradas que violem as regras definidas antes da predição.

### 📜 Contrato de Dados (`src/contracts.py`)

Utilizamos a biblioteca **Pandera** para definir o esquema de validação dos dados:

**Idade (`age`):** inteiros obrigatórios entre 18 e 120 anos (`ge=18`, `le=120`), conforme a regra adotada no cenário acadêmico.

**Renda (`income`):** valor numérico estritamente maior que zero (`gt=0`), sem valores nulos (`nullable=False`).

**Score de Crédito (`credit_score`):** inteiro entre 300 e 850 (`ge=300`, `le=850`), conforme a escala sintética adotada no projeto.

**Valor do Empréstimo (`loan_amount`):** valor solicitado estritamente maior que zero (`gt=0`).

**Alvo (`target`):** rótulo binário de inadimplência, sendo `1` para inadimplente e `0` para adimplente.

**Tipagem e Colunas Estritas:** utilização de `strict=True` para rejeitar colunas não previstas no contrato e `coerce=True` para converter tipos compatíveis.

As regras representam o cenário da demonstração, não uma política completa de concessão de crédito.

### 🤖 Modelo Baseline de Risco (`src/train.py`)

**Algoritmo:** `XGBClassifier` — XGBoost.

**Dataset de Referência:** 5.000 amostras sintéticas, salvas em `data/reference_data.csv`.

**Variáveis de Entrada:** `age`, `income`, `credit_score` e `loan_amount`.

**Divisão dos Dados:** 80% para treinamento e 20% para validação, com estratificação do alvo e `random_state=42`.

**Métricas:** ROC-AUC e relatório de classificação calculados sobre o conjunto de validação.

**Resultado de Referência:** ROC-AUC aproximadamente **0.82**. O valor da execução é apresentado no terminal.

**Artefato:** modelo treinado e serializado em `models/baseline_model.pkl`.

O ROC-AUC deve ser interpretado em conjunto com precisão, recall e distribuição das classes; não representa, isoladamente, a qualidade de uma política de aprovação de crédito.

### 🚨 Simulação de Interceptação / Bloqueio (`src/validate_ingestion.py`)

Para demonstrar o funcionamento do contrato, criamos um lote corrompido em `data/corrupted_data.csv`, contendo idade abaixo do limite, renda nula ou negativa e score inválido.

```powershell
python src/train.py
python src/validate_ingestion.py
```

**Resultado Esperado:** o Pandera identifica violações e o script captura `pa.errors.SchemaErrors`, apresenta os erros e rejeita o lote, retornando `None`.

A mensagem **“BLOQUEIO DE INGESTÃO”** é o resultado esperado dessa demonstração.

**Observação:** a referência a uma fila de erro/DLQ na mensagem do terminal é ilustrativa. Não existe integração com uma fila externa nesta versão.

---

## 📈 Etapa 2 — Simulação de Produção e Detecção de Data Drift

### 🛠️ Execução da Simulação (`src/drift_simulation.py`)

Simulamos um ambiente de produção com 5.000 amostras, criando uma cópia do dataset de referência e alterando intencionalmente duas variáveis:

- **`income`:** multiplicação por fatores aleatórios entre 1.3 e 1.8.
- **`age`:** acréscimo aleatório de 10 a 24 anos, com limitação ao intervalo de 18 a 100 anos.

As variáveis `credit_score` e `loan_amount` permanecem inalteradas.

O script salva `data/production_data.csv`, calcula predições para referência e produção e compara as distribuições das quatro variáveis de entrada.

- **Teste Estatístico:** Kolmogorov-Smirnov de duas amostras (KS-Test).
- **Limiar de Decisão por Variável:** `p-value < 0.05`.
- **Artefato Original:** relatório HTML tabular em `reports/data_drift_report.html`, gerado com os resultados do SciPy.

### 📊 Detecção de Data Drift com Evidently AI

Complementamos a análise estatística com a biblioteca **Evidently AI**, integrada ao script `src/drift_simulation.py`, para comparar os datasets de referência e produção e gerar um relatório visual das mudanças de distribuição.

**Biblioteca:** Evidently AI (`evidently>=0.7,<0.8`).

**Configuração:** `DataDriftPreset(method="ks", threshold=0.05)`.

**Variáveis analisadas:** `age`, `income`, `credit_score` e `loan_amount`.

**Teste Estatístico:** Kolmogorov-Smirnov (KS-Test), com detecção de drift por variável quando `p-value < 0.05`.

As colunas de alvo e predição não entram nessa avaliação de drift das variáveis de entrada.

### 🚀 Execução e Artefatos Gerados

Com as dependências instaladas e o modelo baseline treinado, execute:

```powershell
python src/drift_simulation.py
```

O script gera:

- **`reports/data_drift_report.html`** — Relatório tabular próprio com os resultados do teste KS do SciPy.
- **`reports/evidently_drift_report.html`** — Relatório visual interativo do Evidently com distribuições, testes e identificação das variáveis com drift.
- **`reports/evidently_drift_report.json`** — Resultados estruturados da avaliação do Evidently.

### ✅ Resultados Obtidos na Simulação

| Variável | Estatística KS no relatório próprio | Data Drift Detectado |
| --- | ---: | --- |
| `age` | 0.340 | Sim |
| `income` | 0.486 | Sim |
| `credit_score` | 0.000 | Não |
| `loan_amount` | 0.000 | Não |

O Evidently identificou drift em **2 das 4 variáveis analisadas (50%)**, correspondendo às alterações intencionais de idade e renda.

O relatório também sinalizou **Dataset Drift**, considerando o limiar padrão de proporção de variáveis com drift de **0.5 (50%)**. Esse limiar é distinto do nível de significância de **0.05** utilizado no teste KS de cada variável.

Valores de p exibidos como `0.0` podem refletir arredondamento ou limites de precisão numérica; não devem ser interpretados como uma probabilidade matematicamente exata de zero.

### 🔎 Visualização e Interpretação

Abra `reports/evidently_drift_report.html` no navegador para visualizar os gráficos e explorar os resultados por variável.

**Interpretação:** a detecção de Data Drift evidencia mudanças na distribuição dos dados. Isoladamente, ela não comprova perda de desempenho do modelo, mas fornece um sinal para investigação e avaliação da necessidade de retreinamento.

A base de produção deriva da referência e preserva os rótulos originais. Portanto, o experimento demonstra mudança nas entradas, mas não constitui, por si só, uma avaliação de degradação temporal com novos resultados reais de inadimplência.

---

## 🔍 Etapa 3 — Observabilidade de Pipelines, Infraestrutura e Modelos

O projeto apresenta uma demonstração local de observabilidade, com exportação de indicadores em JSON e visualização em um painel HTML.

Os relatórios são atualizados quando os scripts são executados. Não há atualização contínua em tempo real nesta versão.

### 🚀 Execução no Terminal

Com o ambiente virtual ativo, execute:

```powershell
python src/inference.py
python src/observability.py
```

O script de inferência carrega os dados de produção, aplica o contrato, seleciona as features do modelo e gera predições e probabilidades de inadimplência.

**Artefatos gerados:**

- **`reports/inference_results.csv`** — Resultados da inferência, incluindo `prediction` e `default_probability`.
- **`reports/observability_metrics.json`** — Indicadores utilizados pelo painel demonstrativo.
- **`reports/observability_dashboard.html`** — Painel HTML de observabilidade.

### 📏 Origem dos Indicadores

| Indicador | Implementação nesta versão |
| --- | --- |
| Quantidade de registros | Calculada pela leitura dos datasets de referência e produção. |
| Presença do modelo e do relatório | Verificada pela existência dos arquivos. |
| Latência de `0.38` segundos | Valor demonstrativo fixo, não cronometrado. |
| Taxa de erro de `0.0%` | Valor demonstrativo fixo. |
| Status de sucesso da ingestão e saúde do ambiente | Informações demonstrativas definidas no script. |
| Alerta de drift no dashboard | Texto fixo do cenário, sem integração automática com o resultado do Evidently. |

Os testes estatísticos efetivamente calculados estão nos relatórios da **Etapa 2**.

Os scripts apresentam mensagens de execução no terminal. A consolidação automática de um histórico persistente de logs, falhas e latências permanece como evolução do projeto.

A documentação das métricas está disponível em `docs/observability_metrics.md` e deve ser interpretada considerando o escopo descrito acima.

### 📊 Evidências Visuais e Dashboards

Para visualizar os relatórios, navegue até a pasta `reports/` e abra no navegador:

- **`observability_dashboard.html`** — Painel demonstrativo de infraestrutura, latência, alertas e volume.
- **`data_drift_report.html`** — Relatório tabular do teste KS para as quatro variáveis.
- **`evidently_drift_report.html`** — Relatório visual interativo do Evidently AI.

O GitHub pode exibir o código-fonte dos arquivos HTML. Para visualizar a interface dos relatórios, baixe os arquivos e abra-os localmente no navegador.

**1. Painel de Observabilidade & Saúde do Pipeline — indicadores demonstrativos**

<img width="795" height="534" alt="Painel demonstrativo de observabilidade" src="https://github.com/user-attachments/assets/fb39261f-98c4-4f15-941b-be3fe1ab0a52" />

**2. Relatório de Detecção de Data Drift — KS-Test**

<img width="1222" height="361" alt="Relatório tabular de detecção de Data Drift com teste KS" src="https://github.com/user-attachments/assets/9b55afe1-7ff5-43e5-b2d4-71fe74ed80a8" />

**3. Relatório Visual Interativo — Evidently AI**

<img width="1340" height="599" alt="Relatório de Data Drift gerado pelo Evidently AI" src="https://github.com/user-attachments/assets/304a2e7b-dbc3-466f-ac99-e7220fadc9f8" />

---

## 🔒 Etapa 4 — Governança, Privacy by Design e Compliance (LGPD)

O projeto documenta diretrizes de privacidade e governança para o cenário de análise de crédito, considerando os princípios de Privacy by Design e Privacy by Default.

A implementação acadêmica utiliza dados sintéticos. As medidas propostas para uso com dados reais dependem de implementação e validação e não representam uma certificação de conformidade com a LGPD.

### 1. Tratamento de Dados e Minimização

**Dados Sintéticos:**

Os datasets são gerados por código, sem coleta de cadastros reais, nomes, CPFs, e-mails ou endereços. Não houve anonimização ou pseudonimização de uma base de pessoas reais.

**Minimização de Dados:**

A predição utiliza quatro atributos: `age`, `income`, `credit_score` e `loan_amount`. O rótulo sintético `target` é utilizado no treinamento.

Em uma aplicação real, a necessidade e a finalidade de cada atributo devem ser justificadas e documentadas.

**Controles Propostos:**

Restringir o acesso por função, proteger armazenamento e transferência, evitar exposição de dados pessoais em logs e impedir a publicação de bases reais e credenciais no repositório.

Esses controles são diretrizes para evolução; não estão integralmente implementados no protótipo.

### 2. Base Legal e Revisão de Decisões

**Proteção ao Crédito e Execução de Contrato:**

Em eventual aplicação com dados pessoais reais, a base legal deve ser definida pelo controlador conforme a finalidade da operação.

O artigo 7º da LGPD contempla a execução de contrato ou procedimentos preliminares solicitados pelo titular, no inciso V, e a proteção do crédito, no inciso X. Sua aplicação depende do contexto concreto, não apenas da existência de um modelo de crédito.

**Transparência e Revisão:**

O artigo 20 prevê a solicitação de revisão de decisões unicamente automatizadas que afetem interesses e o fornecimento de informações sobre critérios e procedimentos, observados os segredos comercial e industrial.

O uso de XGBoost não garante automaticamente explicabilidade. Para uma aplicação real, são propostos mecanismos de explicação, registro das decisões e atendimento a solicitações de revisão.

**Referência:** [LGPD — texto atualizado, artigos 7º e 20](https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html).

### 3. Plano de Retenção e Ciclo de Vida dos Dados

**Plano Proposto para o Ambiente Acadêmico:**

| Material | Retenção proposta | Ação prevista |
| --- | --- | --- |
| Datasets sintéticos, modelo e relatórios da entrega | Até o encerramento da avaliação e do prazo institucional de revisão. | Revisar a necessidade de manutenção para reprodução acadêmica. |
| Cópias temporárias e resultados intermediários | Até 30 dias após o encerramento da avaliação. | Remover cópias desnecessárias das pastas e dos backups controlados pelo grupo. |
| Código, documentação e evidências sintéticas no GitHub | Enquanto o projeto for mantido como portfólio acadêmico. | Revisar o conteúdo antes de publicar novas versões. |

O prazo de 30 dias é uma proposta de organização acadêmica, não um prazo determinado pela LGPD. O projeto não implementa exclusão automática desses materiais.

Para dados reais, os prazos devem considerar finalidade, necessidade e obrigações aplicáveis. Os artigos 15 e 16 da LGPD tratam do término do tratamento, da eliminação e das hipóteses de conservação.

**Referência:** [LGPD — artigos 15 e 16](https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html).

**Descarte e Versionamento:**

O `.gitignore` auxilia a evitar a inclusão de arquivos não rastreados no Git, mas não apaga dados, não remove arquivos já versionados e não garante descarte seguro.

Arquivos publicados podem permanecer no histórico do repositório, em clones ou forks. Por isso, dados reais e credenciais não devem ser publicados.

### 4. 🔎 Análise Causal do Cenário Simulado

**Problema:**

Mudanças no perfil dos solicitantes podem tornar os dados de produção diferentes daqueles utilizados no treinamento, criando risco de degradação silenciosa.

**Causa Conhecida no Experimento:**

O script altera deliberadamente renda e idade, mantendo score e valor do empréstimo inalterados.

| Intervenção | Evidência observada | Interpretação |
| --- | --- | --- |
| Multiplicação da renda por fatores entre 1.3 e 1.8 | KS de 0.486 e drift detectado. | Mudança na distribuição de renda da base sintética. |
| Acréscimo de 10 a 24 anos, com limites | KS de 0.340 e drift detectado. | Mudança na distribuição etária da população simulada. |
| Preservação de score e valor do empréstimo | KS de 0 e ausência de drift. | Ausência de mudança nas variáveis mantidas iguais. |

**Hipóteses de Negócio:**

Mudanças no público-alvo poderiam alterar o perfil de idade e renda dos solicitantes. Mudanças econômicas também poderiam afetar renda nominal e capacidade de pagamento.

Essas possibilidades são hipóteses para investigação, não causas comprovadas com dados reais neste projeto.

O aumento de idade aplicado representa uma mudança na composição da carteira, não o envelhecimento observado de clientes durante um curto período.

**Limites da Análise:**

O teste KS identifica diferenças de distribuição, mas não identifica suas causas econômicas. A interpretação causal desta demonstração se restringe à intervenção conhecida no gerador de dados.

Também não foi quantificada uma queda de desempenho em produção.

**Ações Propostas:**

Investigar a origem dos dados, verificar mudanças de coleta ou público, obter rótulos confiáveis e comparar métricas de desempenho antes de decidir por recalibração ou retreinamento.

Uma nova versão do modelo deve ser validada antes de substituir o baseline.

### 5. ⚖️ Plano de Mitigação de Vieses

A geração sintética do alvo depende dos atributos de entrada, incluindo idade e renda. O modelo pode reproduzir essas relações, e um bom resultado agregado não comprova ausência de vieses.

**Medidas propostas, ainda sem auditoria quantitativa implementada:**

- Verificar representatividade e quantidade de exemplos por faixas de idade e renda.
- Comparar precisão, recall, falsos positivos e falsos negativos entre segmentos, utilizando rótulos confiáveis.
- Considerar tamanho amostral e incerteza antes de interpretar diferenças entre grupos.
- Investigar possíveis variáveis substitutas de características protegidas.
- Avaliar ajustes na amostragem, nas variáveis e no limiar de decisão quando diferenças injustificadas forem identificadas.
- Documentar justificativas, limitações e revisões, prevendo mecanismos de supervisão e contestação em eventual uso real.

A ausência de identificadores pessoais e o retreinamento periódico, isoladamente, não garantem mitigação de vieses.

---
