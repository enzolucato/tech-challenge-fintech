Documentação de Métricas de Saúde Operacional
Este documento define e formaliza as métricas de observabilidade e saúde do pipeline de dados, da infraestrutura e do modelo de crédito em produção.

Métricas de Infraestrutura e Execução do Pipeline
Status de Execução da Ingestão: Monitora o sucesso ou falha na leitura dos lotes de dados de crédito (Validação via Pandera).
Latência Média do Pipeline: Tempo de processamento por lote (Alvo: $< 1.0$ segundo).
Versão do Ambiente: Python 3.13 operando em ambiente virtual isolado (venv), garantindo estabilidade e reprodutibilidade de dependências.

Métricas de Qualidade e Confiabilidade de Dados
Taxa de Erro de Contrato: Percentual de registos rejeitados por violação de regras rígidas (ex: nulos em colunas obrigatórias, idades inválidas).
Volume de Dados Processados: Contagem de linhas ativas nos datasets de Referência (Treino) e Produção (Inferência).

Métricas de Degradação e Alertas do Modelo
Data Drift Detectado: Monitoramento contínuo das variáveis críticas (age e income) utilizando testes estatísticos (Kolmogorov-Smirnov / PSI).
Status de Alerta Ativo: Disparo automático de alertas operacionais quando o p-value do teste estatístico for inferior ao limiar de significância ($p < 0.05$).