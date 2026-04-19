# omie-xml-intake

Este módulo publica uma versão **sanitizada e reaproveitável** do pipeline auditado no ambiente local. A base original foi avaliada quanto a acoplamento com `.env`, diretórios operacionais, XMLs reais, logs e nomenclaturas internas. A partir dessa avaliação, este diretório preserva a lógica funcional essencial do primeiro projeto, mas a reconstrói como **template público seguro**, pronto para uso local com Docker e para orquestração via Airflow.

O fluxo funcional permanece dividido em três etapas. Primeiro, os XMLs são varridos em um diretório parametrizável e convertidos para uma planilha com a aba `contas_a_receber`. Em seguida, essa planilha pode ser consumida por um módulo de upload para a Omie, que opera por variáveis de ambiente externas e suporta `dry run`. Por fim, existe uma trilha separada e opcional para sincronização de responsáveis a partir de uma API externa de origem, preservando o desacoplamento entre ingestão fiscal e cadastro relacional.

## Estrutura pública

| Caminho | Função |
| --- | --- |
| `app/xml_to_xlsx.py` | Converte XMLs para uma planilha saneada com foco em contas a receber. |
| `app/omie_uploader.py` | Envia clientes e títulos à Omie com suporte a prefixo e `dry run`. |
| `app/activesoft_client.py` | Cliente genérico para origem externa via token bearer. |
| `app/activesoft_to_omie.py` | Exemplo de sincronização de responsáveis para a Omie. |
| `app/logging_utils.py` | Logging padronizado para execução local e orquestrada. |
| `dags/omie_xml_pipeline.py` | DAG de exemplo para Airflow. |
| `.env.example` | Modelo público de configuração, sem segredos. |

## Parâmetros esperados

| Parâmetro | Objetivo |
| --- | --- |
| `XML_INPUT_DIR` | Diretório ou volume com XMLs de entrada. |
| `CUSTOMER_OMIE_ID_CONTA_CORRENTE` | Conta corrente de destino na Omie. |
| `CUSTOMER_OMIE_CODIGO_CATEGORIA` | Categoria a usar na criação de contas a receber. |
| `CUSTOMER_OMIE_APP_KEY` | Chave de integração injetada em runtime. |
| `CUSTOMER_OMIE_APP_SECRET` | Segredo de integração injetado em runtime. |

## Política de publicação

Nenhum XML real, payload produtivo, log operacional, banco local, ambiente virtual ou arquivo `.env` privado faz parte deste módulo. O objetivo aqui é expor um código-fonte compreensível, extensível e auditável, não reproduzir o ambiente operacional original.
