# Auditoria inicial da base local compartilhada

A base local `projeto_data_by_orbe` está sob versionamento Git ativo e possui trabalho recente em paralelo, incluindo cinco commits voltados a limpeza, orquestração, documentação e refatoração de naming interno. Por isso, a estratégia adotada nesta tarefa é **não editar a origem diretamente** e tratar qualquer sanitização como preparação de uma versão pública derivada.

## Estado observado

| Aspecto | Observação |
| --- | --- |
| Repositório Git local | Ativo, com histórico recente em `main`. |
| Trabalho concorrente | Há alterações locais e arquivos não rastreados, o que reforça a necessidade de isolamento da publicação pública. |
| Arquivo `.env` | Presente e modificado localmente. |
| Diretórios de runtime | Presentes, incluindo `input`, `output`, `logs`, `airflow_db`, `airflow_logs` e `.venv`. |
| Artefatos de dados | Há XMLs de entrada e JSONs operacionais em `dados_para_importar/`. |
| Compose atual | Injeta segredos por variáveis de ambiente, mas ainda referencia `.env` diretamente e usa nomes internos legados. |
| `.gitignore` | Na prática, está vazio ou sem regras efetivas no estado observado. |

## Commits recentes informados e confirmados

| Commit | Síntese auditada |
| --- | --- |
| `c880aea` | Adiciona script de limpeza com backup temporário e remoção de artefatos operacionais. |
| `ea2cb84` | Adiciona orquestrador do pipeline completo. |
| `6f42bbd` | Adiciona README principal com quick start. |
| `dece109` | Documenta a integração ActiveSoft → Omie. |
| `5395bab` | Inicia neutralização de naming interno ao renomear variável de token. |

## Riscos ainda identificados

| Risco | Evidência |
| --- | --- |
| Segredos ainda parametrizados com naming legado | Persistem referências a `IED_OMIE_APP_KEY`, `IED_OMIE_APP_SECRET` e `IED_ACTIVE_SOFT_TOKEN` em scripts e compose. |
| Acoplamento direto ao `.env` | Há scripts e módulos que carregam `.env` localmente, inclusive com caminho fixo para `/opt/airflow/.env`. |
| Diretórios e arquivos não públicos | Existem XMLs de entrada, logs, banco local do Airflow e ambiente virtual. |
| Falta de proteção contra commits acidentais | O `.gitignore` atual não protege adequadamente segredos, runtime e artefatos. |
| Potencial exposição semântica | O nome do projeto e parte dos caminhos ainda refletem uso operacional específico, não um template público sanitizado. |

## Direção de sanitização recomendada

A publicação pública deve ser feita a partir de uma **versão derivada e saneada**, com novo `.gitignore`, `env template`, dados sintéticos mínimos, compose adaptado, remoção de `.venv` e de diretórios de runtime, além de padronização de variáveis para nomes públicos e neutros. Também será necessário revisar os arquivos em `scripts/`, `app/` e `dags/` para substituir nomenclaturas legadas e remover dependência rígida do `.env` versionado.
