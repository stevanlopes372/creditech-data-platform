# CrediTech Data Platform

Este repositório documenta um projeto de portfólio de engenharia de dados end-to-end, simulando a criação da plataforma de dados para uma fintech de crédito pessoal fictícia, a "CrediTech".<br><br><br>


# 1. O Desafio de Negócio

A CrediTech é uma fintech digital que concede empréstimos pessoais. O processo é 100% online, desde a solicitação até a análise de risco e a concessão.

A empresa precisa de uma plataforma de dados robusta (Data Warehouse) para centralizar suas informações e extrair inteligência de negócio. O objetivo é parar de depender de relatórios manuais e planilhas, permitindo análises evarcharatégicas que respondam a perguntas-chave:

- Qual a taxa de aprovação de empréstimos por faixa de score de crédito e por região do país?
- Qual o perfil demográfico (idade, estado civil, renda) dos clientes que mais atrasam pagamentos?
- Qual é o valor médio de empréstimo solicitado por faixa de renda declarada?<br><br><br>


# 2. Arquitetura da Solução (Planejada)

Para atender a esses requisitos, este projeto implementa uma plataforma de dados moderna na nuvem, seguindo a Arquitetura Medallion (Bronze, Silver, Gold).

- Camada Bronze: Recebe os dados brutos, simulados por um script Python, representando as fontes operacionais (OLTP) da fintech.
- Camada Silver: Aplica limpeza, transformações, tipagem e enriquece os dados.
- Camada Gold: Modela os dados em um Star Schema otimizado para consultas analíticas (OLAP), pronto para ser consumido por ferramentas de Business Intelligence.
<br><br><br>


[inserir diagrama aqui]
<br><br><br>



# 3. Modelagem de Dados (Data Warehouse)
O núcleo da camada Gold é um Modelo Dimensional (Star Schema), projetado para responder às perguntas de negócio com alta performance.


## Desafio Técnico: Dimensão de Mudança Lenta (SCD Tipo 2)

Um requisito crítico do negócio é analisar as propostas de empréstimo com a "fotografia" exata do cliente no momento da solicitação (renda, score, etc.). Para resolver isso, a Dim_Cliente é implementada usando a técnica SCD (Slowly Changing Dimension) Tipo 2, que versiona o regivarcharo do cliente a cada mudança relevante, preservando todo o histórico.

## Esquema Físico
`fato_propostas`

Grão: Uma linha por proposta de empréstimo.

```SQL
- PK_Proposta (PK, int)
- ID_Proposta_Negocio (varchar)
- FK_Cliente (int)           -- Chave para a versão exata do cliente
- FK_Data_Proposta (int)     -- Chave para a Dim_Data
- valor_solicitado (decimal)
- valor_aprovado (decimal)
- taxa_juros_anual (decimal)
- cet_anual (decimal)
- foi_aprovada (boolean)     -- Flag (True=Sim, False=Não)
```

`dim_cliente`

Grão: Uma linha por versão de um cliente (SCD Tipo 2).

```SQL
- PK_Cliente (PK, int)         -- Chave Surrogada única
- ID_Cliente_Negocio (varchar) -- ID de negócio (agrupa versões)
- nome_cliente (varchar)
- idade (int)
- genero (varchar)
- faixa_renda (varchar)
- faixa_score (varchar)
- cidade (varchar)
- estado (varchar)
- regiao (varchar)
-- Colunas de Controle SCD Tipo 2
- data_inicio_validade (date)
- data_fim_validade (date)
- flag_versao_atual (boolean)
```

`Dim_Data`

Grão: Um dia do calendário.

```SQL
- PK_Data (PK, int)            -- Formato YYYYMMDD
- data_completa (date)
- ano (int)
- mes (int)
- nome_mes (str)
- dia (int)
- dia_da_semana (str)
- trimestre (int)
- flag_fim_de_semana (boolean)
```
<br><br><br>

# 4. Tecnologias Utilizadas (Planejado)
Geração de Dados: Python, Pandas, Faker

Infraestrutura como Código (IaC): Terraform

Armazenamento (Data Lake): AWS S3

Processamento (ETL/ELT): PySpark

Data Warehouse (Camada Gold): TBD

Orquestração: TBD

Business Intelligence: TBD

<br><br><br>

# 5. Status do Projeto e Próximos Passos
Este projeto está sendo desenvolvido ativamente. As etapas abaixo definem o roadmap:

[ X ] Etapa 0: Definição do Problema de Negócio (Fintech de Crédito)

[ X ]  Etapa 1: Modelagem de Dados Dimensional (Star Schema com SCD Tipo 2)

[ WIP ] Etapa 2: Geração de Dados Sintéticos (Task DE-101)

[ ] Etapa 3: Provisionamento da Infraestrutura na Nuvem (IaC com Terraform)

[ ] Etapa 4: Desenvolvimento da Pipeline de Dados (Bronze -> Silver -> Gold com PySpark)

[ ] Etapa 5: Implementação da Orquestração (Airflow/Mage)

[ ] Etapa 6: Criação de Dashboards de BI (Power BI/Looker)