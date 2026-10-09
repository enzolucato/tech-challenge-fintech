## 🛡️ Validação de Dados, Contratos e Modelo Baseline

### 🎯 Objetivo
Garantir a integridade dos dados na camada de ingestão (Data Quality First) através da definição de contratos rígidos, impedindo que dados inconsistentes ou anómalos alimentem o modelo de *Credit Scoring*.

---

### 📋 Contrato de Dados (src/contracts.py)
Utilizamos a biblioteca *Pandera* para definir o esquema estrito de validação do lote de dados de entrada.

#### Regras de Validação Aplicadas:
1. *Idade (age): Valores inteiros obrigatórios entre **18 e 120 anos* (ge=18, le=120). Garante a elegibilidade legal para concessão de crédito.
2. *Renda (income): Valor numérico contínuo estritamente maior que zero (gt=0), **não sendo permitidos valores nulos (nullable=False)*.
3. *Score de Crédito (credit_score): Padrão FICO/Serasa variando obrigatoriamente entre **300 e 850* (ge=300, le=850).
4. *Valor do Empréstimo (loan_amount)*: Valor solicitado estritamente maior que zero (gt=0).
5. *Tipagem e Colunas Estritas*: Ativação da flag strict=True, que rejeita colunas não mapeadas no contrato para evitar contaminação do dataset.

---

### 🤖 Modelo Baseline de Risco (src/train.py)
* *Algoritmo*: XGBClassifier (XGBoost).
* *Dataset de Referência*: Gerado/Limpo com 5.000 amostras sintéticas representando o cenário ideal de treino (data/reference_data.csv).
* *Métrica de Desempenho: **ROC-AUC ~0.82*.
* *Artefato*: Modelo treinado e serializado salvo em models/baseline_model.pkl.

---

### 🚨 Simulação de Interceptação / Bloqueio (src/validate_ingestion.py)
Para comprovar o funcionamento do contrato, simulamos a entrada de um lote corrompido (data/corrupted_data.csv) contendo:
* Cliente menor de idade (age = 17);
* Renda nula (income = NaN);
* Renda negativa (income = -500.0);
* Score de crédito inválido (credit_score = 200).

#### Resultado Esperado:
O pipeline dispara uma exceção pa.errors.SchemaErrors, interrompendo o fluxo de ingestão e direcionando as mensagens com falhas para uma fila de tratamento de erros (Dead Letter Queue — DLQ), garantindo que nenhum dado ruim chegue à camada de predição.

🚀 Instalar dependências:
   ```bash
   pip install -r requirements.txt
