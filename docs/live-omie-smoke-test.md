# Smoke test real na Omie sem persistência de credenciais

Este documento registra um **caso de teste real** executado contra a API da Omie utilizando credenciais transitórias fornecidas em tempo de execução, sem persistência em arquivos do projeto, sem inclusão em `.env` e sem versionamento de segredos.

## Objetivo

O objetivo do teste foi validar que o repositório público já consegue alimentar uma base Omie de maneira controlada, usando um cliente de teste e um lançamento de **conta a receber** mínimo, compatível com o primeiro projeto publicado.

## Parâmetros confirmados online

| Item | Valor validado |
| --- | --- |
| Conta corrente | `Meta Pay - Caixinha Manus` |
| Código da conta corrente | `3086599760` |
| Tipo | `CV` |
| Status | Ativa |
| Categoria | `1.110 - Receitas Manus` |
| Código da categoria | `1.01.99` |

## Ajustes necessários durante a execução

Durante a validação, dois pontos ficaram evidentes. O primeiro foi que a conta corrente anterior do tipo caixinha estava inativa, o que fazia a Omie rejeitar o lançamento. O segundo foi que a API de `IncluirContaReceber` aceitou o campo `id_conta_corrente`, mas rejeitou a variação `codigo_conta_corrente`. Além disso, o campo `numero_documento` precisou respeitar o limite de 20 caracteres imposto pela API.

Esses achados foram incorporados no script público `omie-xml-intake/scripts/run_live_omie_smoke_test.py`, que agora gera um identificador curto de integração e usa somente `id_conta_corrente` para o lançamento.

## Resultado do teste executado

| Item | Resultado |
| --- | --- |
| Nome do cliente de teste | `Cliente Teste Manus ORBE 2026-04-19` |
| Código do cliente Omie | `3086599956` |
| Código de integração do lançamento | `MORBE2604194317` |
| Código do lançamento Omie | `3086599958` |
| Valor testado | `1,23` |
| Status final | `Lançamento cadastrado com sucesso` |

## Forma segura de uso

O script foi desenhado para receber credenciais apenas por variáveis de ambiente efêmeras no momento da execução. Isso permite reproduzir o teste em ambiente controlado sem gravar `app_key` e `app_secret` em arquivos versionados.

Um exemplo de uso, com credenciais informadas apenas no shell da sessão corrente, é o seguinte:

```bash
OMIE_APP_KEY='preencher_em_runtime' \
OMIE_APP_SECRET='preencher_em_runtime' \
python3.11 scripts/run_live_omie_smoke_test.py \
  --account-code 3086599760 \
  --category-code 1.01.99 \
  --amount 1.23
```

## Observação operacional

Esse smoke test é propositalmente simples e foi criado para validar o caminho mínimo de integração real com a Omie. Ele não substitui testes idempotentes mais robustos, trilhas de reversão, nem políticas de saneamento de dados de homologação. Ainda assim, ele comprova que o pipeline público já possui um ponto de entrada funcional para alimentar a base Omie sob supervisão e com baixo acoplamento a segredos.
