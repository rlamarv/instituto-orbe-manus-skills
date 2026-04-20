# instituto-orbe-manus-skills

Este repositório foi estruturado para **publicação supervisionada de código sanitizado por IA** no contexto do Instituto ORBE, com foco em integrações de dados que precisem permanecer públicas sem expor credenciais, arquivos `.env`, cargas de teste inseguras, segredos operacionais ou dados sensíveis de terceiros.

A primeira trilha de trabalho deste repositório é um projeto de ingestão e tratamento orientado à Omie, preparado para operar com **Docker**, com geração de **DAGs do Airflow** e com bootstrap local de **Apache Superset**. O objetivo não é publicar um ambiente produtivo pronto, mas sim uma base pública segura, auditável, reproduzível e preparada para endurecimento adicional em servidores elásticos ou ambientes orquestrados.

## Princípios de publicação

| Princípio | Aplicação neste repositório |
| --- | --- |
| Segregação de segredos | Nenhuma chave real, segredo, token, senha, cookie ou `.env` privado deve ser versionado. |
| Sanitização obrigatória | Mocks inseguros, dados identificáveis, endpoints privados e exemplos derivados de produção devem ser removidos ou substituídos por amostras sintéticas. |
| Docker first | Cada módulo é preparado para execução controlada em containers, com variáveis injetadas em tempo de execução. |
| Reprodutibilidade | O repositório prioriza templates, exemplos mínimos e documentação explícita de bootstrap. |
| Evolução segura | O código público deve permitir extensão futura para Airflow, Superset, webhooks e orquestração sem refatoração destrutiva. |

## Estrutura inicial

| Pasta | Finalidade |
| --- | --- |
| `github-sanitized-publisher/` | Procedimentos, utilitários e convenções para sanitizar código antes da publicação pública. |
| `omie-xml-intake/` | Base do primeiro projeto, dedicada à ingestão de XML e parametrização segura para operações Omie. |
| `airflow-dag-generator/` | Geração e organização de DAGs a partir de pipelines saneados e configuráveis. |
| `superset-local-bootstrap/` | Bootstrap local do Superset para exploração analítica e visualização de dados. |
| `docker-secure-runtime/` | Runtime containerizado com foco em isolamento, injeção de variáveis e composição local segura. |
| `docs/` | Documentação de arquitetura, segurança, sanitização e operação. |
| `templates/` | Modelos públicos de configuração e arquivos de exemplo. |

## Parâmetros funcionais do primeiro projeto

O primeiro projeto deve ser estruturado para receber, fora do Git, os seguintes parâmetros operacionais:

| Parâmetro | Diretriz de tratamento |
| --- | --- |
| Repositório de XML ou pasta de entrada | Informado por caminho local, volume Docker ou conector externo, sem caminhos internos sensíveis hardcoded. |
| Conta corrente a receber | Mantida como parâmetro operacional, sem dados produtivos reais no repositório. |
| Categoria da conta corrente a receber | Mantida como parâmetro externo ou catálogo saneado. |
| API Key da Omie | Somente via ambiente local ou segredo injetado em runtime. |
| API Secret da Omie | Somente via ambiente local ou segredo injetado em runtime. |

## Estado atual

Neste momento, o repositório já foi criado como **área de staging segura**. A abertura pública ocorrerá após a revisão e sanitização da base sensível do projeto de origem, evitando exposição acidental de credenciais ou mocks inseguros.

## Scripts de Integração Omie

### `omie-xml-intake/scripts/run_multi_base_omie_bootstrap.py`

Este script é responsável por provisionar a estrutura mínima (contas correntes, categorias) e realizar um smoke test em múltiplas bases Omie. Ele espera as credenciais da API Omie via variáveis de ambiente.

**Uso:**

```bash
python omie-xml-intake/scripts/run_multi_base_omie_bootstrap.py --config-file <caminho_para_config.json> [--dry-run]
```

### `omie-xml-intake/scripts/process_xml_to_omie.py`

Este script processa arquivos XML de NFCom (Nota Fiscal de Comunicação) e cria contas a receber correspondentes na API da Omie. Ele utiliza as mesmas variáveis de ambiente para as credenciais da Omie e um arquivo de configuração JSON para as bases.

**Uso:**

```bash
python omie-xml-intake/scripts/process_xml_to_omie.py --xml-dir <caminho_para_diretorio_xml> --config-file <caminho_para_config.json> [--dry-run]
```

**Exemplo de `config.json` para ambos os scripts:**

```json
[
  {
    "base_name": "Base_Principal",
    "app_key_env": "OMIE_APP_KEY_BASE1",
    "app_secret_env": "OMIE_APP_SECRET_BASE1",
    "target_account_name": "Conta Corrente Principal",
    "target_account_type": "CC",
    "target_category_description": "Vendas de Produtos",
    "amount": 100.50
  },
  {
    "base_name": "Base_Secundaria",
    "app_key_env": "OMIE_APP_KEY_BASE2",
    "app_secret_env": "OMIE_APP_SECRET_BASE2",
    "target_account_name": "Caixinha Manus",
    "target_account_type": "CX",
    "target_category_description": "Serviços de Consultoria",
    "amount": 50.25
  }
]
```

## Habilidade reutilizável derivada deste processo

O fluxo consolidado de bootstrap seguro da Omie também foi formalizado como uma **skill reutilizável**, permitindo reaproveitar o processo em novas execuções sem depender apenas do histórico desta conversa.

| Recurso | Local |
| --- | --- |
| Skill operacional | `/home/ubuntu/skills/omie-secure-bootstrap/` |
| Espelho versionado no repositório | `skills/omie-secure-bootstrap/` |
| Documento explicativo | `docs/omie-secure-bootstrap-skill.md` |

Essa skill encapsula o padrão de smoke test em base única, bootstrap multi-base, provisionamento condicional por API, uso de credenciais efêmeras e empacotamento do resultado em documentação pública sanitizada.
