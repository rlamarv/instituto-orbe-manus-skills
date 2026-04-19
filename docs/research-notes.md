# Notas de pesquisa

## Airflow em Docker

Fonte consultada: documentação oficial do Apache Airflow 3.2.0 sobre execução em Docker Compose.

Principais pontos assimilados:

- O arquivo `docker-compose.yaml` oficial é indicado para **aprendizado, exploração e ambientes locais**, mas **não oferece garantias de segurança para produção**.
- Para produção, a própria documentação recomenda **Kubernetes com o Helm Chart oficial**.
- O bootstrap local requer Docker Compose v2.14.0 ou superior e memória adequada para os containers.
- A estrutura padrão monta diretórios `dags`, `logs`, `config` e `plugins`.
- Em Linux, recomenda-se definir `AIRFLOW_UID=$(id -u)` em um arquivo `.env` local para evitar problemas de permissão de arquivos.
- A inicialização da base e do primeiro usuário ocorre via `docker compose up airflow-init`.
- O compose de referência usa `postgres` e `redis` para suportar `CeleryExecutor`.
- Ajustes permissivos como `chmod 777` são explicitamente tratados como paliativos e **não devem ser usados em produção**.

## Superset em Docker Compose

Fonte consultada: documentação oficial do Apache Superset sobre instalação com Docker Compose.

Principais pontos assimilados:

- O uso de `docker compose` no Superset é recomendado para **desenvolvimento local** e **não é considerado pronto para produção**.
- A documentação apresenta múltiplos perfis de execução, incluindo ambiente interativo, variante leve, build não-dev e execução por tag de imagem.
- O metadata store do Superset fica no banco relacional e precisa de **backup explícito** em cenários reais.
- O projeto referencia `docker/.env` e `docker/.env-local`, com o arquivo local ignorado por `.gitignore` para reduzir risco de commit de segredos.
- O carregamento de exemplos pode ser desativado com `SUPERSET_LOAD_EXAMPLES` para economizar recursos e evitar dados desnecessários.
- Para uso seguro no contexto deste projeto, o compose deve ser adaptado para **rede interna**, **variáveis externas não versionadas**, **persistência explícita** e **templates de configuração sem credenciais reais**.

## Implicações para o repositório ORBE

- O repositório público deve conter apenas **modelos**, **exemplos saneados**, **arquivos `.env.example`**, e documentação de injeção de segredos em tempo de execução.
- A publicação do primeiro projeto deve separar claramente o que é:
  - código versionável e público;
  - configuração local privada;
  - dados de exemplo seguros e sintéticos;
  - credenciais de integração Omie fornecidas apenas fora do Git.
- O stack local deverá ser montado como base de referência e não como template de produção final. A documentação deverá deixar explícito que produção exige endurecimento adicional.

## Omie: autenticação, APIs e webhooks

A navegação pelo portal do desenvolvedor e pela central de ajuda da Omie confirmou a estrutura de documentação voltada para **Aplicativos**, **Lista das APIs** e **notificações de webhook**. A central de ajuda agrega materiais específicos sobre boas práticas de integração, obtenção de chave de acesso, limites de consumo, tratamento de erros, histórico de APIs e webhooks e exemplos operacionais para entidades diretamente ligadas ao primeiro projeto, como **conta corrente**, **conta a receber** e **categorias**.

Para a arquitetura pública do repositório, isso reforça que o código deve ser organizado para receber `OMIE_APP_KEY` e `OMIE_APP_SECRET` apenas por injeção externa de ambiente, sem persistência em banco e sem versionamento. Também é coerente manter templates parametrizados para os campos operacionais citados pelo usuário, incluindo repositório de XML ou pasta de entrada, conta corrente a receber e categoria da conta corrente a receber, deixando claro em documentação que esses valores são sensíveis ao contexto de cada operação.

A presença de documentação dedicada a webhooks indica que o projeto pode evoluir de ingestão por lote para integração orientada a eventos. Portanto, a base pública deve prever uma interface limpa para recebimento de notificações, idempotência, registro auditável e segregação entre configuração pública e segredos privados, sem incluir endpoints reais, tokens, URLs privadas ou cargas de exemplo derivadas de dados produtivos.
