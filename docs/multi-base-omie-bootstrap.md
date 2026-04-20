# Run script multi-base para Omie com provisionamento automático

Este documento registra a criação de um novo script público para operar em **várias bases Omie**, com foco em segurança operacional, baixo acoplamento a segredos e capacidade de **provisionar estrutura mínima via API** quando ela ainda não existir.

## Objetivo

O objetivo do script `omie-xml-intake/scripts/run_multi_base_omie_bootstrap.py` é permitir que diferentes bases Omie sejam processadas em sequência a partir de um arquivo de configuração sanitizado. Para cada base, o fluxo tenta localizar a conta corrente e a categoria desejadas. Se elas não existirem, o script passa a criá-las por API e só então executa o lançamento de teste.

## Estratégia de configuração

A configuração foi desenhada para evitar a persistência de credenciais no repositório. Em vez de carregar `app_key` e `app_secret` diretamente do arquivo JSON, o script espera que cada base informe apenas o nome das variáveis de ambiente que deverão conter esses segredos em runtime.

| Campo | Função |
| --- | --- |
| `base_name` | Nome lógico da base Omie dentro da execução multi-base. |
| `app_key_env` | Nome da variável de ambiente que contém a `app_key`. |
| `app_secret_env` | Nome da variável de ambiente que contém a `app_secret`. |
| `target_account_name` | Nome da conta corrente a localizar ou criar. |
| `target_account_type` | Tipo de conta corrente a provisionar, se necessário. |
| `target_bank_code` | Código do banco para criação da conta corrente. |
| `target_category_description` | Nome da categoria a localizar ou criar. |
| `target_category_superior` | Grupo superior da categoria, usado na criação. |
| `amount` | Valor do lançamento de teste em conta a receber. |

## Fluxo funcional

O comportamento do script foi estruturado em cinco etapas. Primeiro, ele lista as contas correntes existentes e tenta encontrar a conta desejada pelo nome. Se não encontrar, chama `IncluirContaCorrente` com o conjunto mínimo de parâmetros recomendado pela documentação oficial da Omie.

Depois, ele lista as categorias já cadastradas e tenta encontrar a descrição desejada. Se a categoria não existir, chama `IncluirCategoria` usando a categoria superior configurada e uma natureza descritiva mínima.

Na sequência, o script cria um cliente de teste transitório, gera um identificador curto de integração compatível com a Omie e cadastra uma conta a receber usando `id_conta_corrente`, que foi o campo efetivamente aceito no cenário validado.

## Validação realizada

A implementação foi validada com uma execução real em uma base Omie já estruturada. Nesse cenário, a conta corrente e a categoria já existiam, então o script reutilizou ambos os cadastros e seguiu para o smoke test.

| Item | Resultado da validação |
| --- | --- |
| Base lógica validada | `orbe_meta_pay` |
| Conta corrente encontrada | `Meta Pay - Caixinha Manus` |
| Código da conta | `3086599760` |
| Categoria encontrada | `1.110 - Receitas Manus` |
| Código da categoria | `1.01.99` |
| Cliente de teste criado | `3086600193` |
| Lançamento criado | `3086600195` |
| Código de integração | `ORBEME2604193726` |
| Resultado final | `Lançamento cadastrado com sucesso!` |

## Segurança operacional

O script foi projetado para cumprir quatro restrições de segurança. A primeira é **não versionar credenciais**. A segunda é **não depender de `.env` interno ao repositório**. A terceira é **reutilizar a estrutura existente antes de criar novos cadastros**, evitando proliferação desnecessária de contas e categorias. A quarta é oferecer `--dry-run` para inspeção prévia do que seria provisionado.

## Arquivos adicionados

| Caminho | Papel |
| --- | --- |
| `omie-xml-intake/scripts/run_multi_base_omie_bootstrap.py` | Execução multi-base com descoberta e provisionamento automático. |
| `omie-xml-intake/templates/multi-base-config.example.json` | Exemplo sanitizado de configuração para múltiplas bases. |
| `docs/multi-base-omie-bootstrap.md` | Documento de arquitetura, uso e validação da solução. |

## Observação final

Esse novo run script estabelece uma base pública mais robusta para homologação e operação supervisionada em múltiplos tenants Omie. A partir dele, fica simples conectar futuras execuções por Airflow, pipelines Dockerizados ou rotinas agendadas, mantendo o mesmo padrão de credenciais efêmeras e estrutura provisionada sob demanda.
