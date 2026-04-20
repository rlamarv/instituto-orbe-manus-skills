---
name: omie-secure-bootstrap
description: Provisionar, validar e documentar integrações Omie de forma segura. Use quando precisar criar ou executar smoke tests reais na Omie, operar múltiplas bases com credenciais efêmeras, criar conta corrente e categoria por API quando a estrutura não existir, ou transformar automações Omie em entregas públicas sanitizadas.
---

# Omie Secure Bootstrap

## Visão geral

Usar esta skill para executar o fluxo que foi consolidado no projeto público do Instituto ORBE: **descobrir estrutura existente na Omie, provisionar o mínimo necessário por API quando faltar alguma parte, executar smoke tests reais com baixo acoplamento a segredos e documentar o resultado de forma sanitizada**.

Preferir esta skill quando a tarefa envolver qualquer combinação destes cenários:

| Cenário | Recurso principal |
| --- | --- |
| Validar uma única base Omie com cliente e conta a receber de teste | `scripts/run_live_omie_smoke_test.py` |
| Operar várias bases Omie com bootstrap automático de conta corrente e categoria | `scripts/run_multi_base_omie_bootstrap.py` |
| Preparar uma configuração sanitizada para múltiplas bases | `templates/multi-base-config.example.json` |
| Reusar decisões de implementação e restrições já validadas | `references/omie-bootstrap-notes.md` |
| Publicar ou explicar o processo em repositório | `references/repo-packaging-pattern.md` |

## Fluxo de decisão

Seguir esta árvore de decisão antes de agir:

1. Determinar se a tarefa é **base única** ou **multi-base**.
2. Determinar se a estrutura Omie já existe ou se deve ser criada por API.
3. Determinar se a execução pode ser **real** ou se deve começar por `--dry-run`.
4. Determinar se o usuário quer apenas operar a Omie ou também **empacotar o processo para publicação e documentação**.

## Workflow principal

### 1. Confirmar a política de segredos

Usar `app_key` e `app_secret` apenas em variáveis de ambiente de runtime. Não salvar credenciais reais em `SKILL.md`, arquivos versionados, `.env` público, documentação, exemplos ou logs permanentes.

### 2. Escolher o modo de execução

Para **uma única base**, preferir `scripts/run_live_omie_smoke_test.py` quando a conta corrente e a categoria já forem conhecidas.

Para **várias bases** ou quando a estrutura puder não existir, preferir `scripts/run_multi_base_omie_bootstrap.py`.

### 3. Resolver a estrutura mínima da Omie

Ao operar a Omie, seguir esta ordem:

1. Listar contas correntes existentes.
2. Tentar localizar a conta pelo nome.
3. Se não existir, criar a conta corrente por API.
4. Listar categorias existentes.
5. Tentar localizar a categoria pela descrição.
6. Se não existir, criar a categoria por API.
7. Criar um cliente de teste transitório.
8. Criar a conta a receber mínima para validar o fluxo fim a fim.

### 4. Aplicar as restrições já validadas

Respeitar estas decisões já comprovadas no processo:

| Ponto | Decisão operacional |
| --- | --- |
| Conta a receber na Omie | Usar `id_conta_corrente` no payload do lançamento. |
| Documento de teste | Manter `numero_documento` com no máximo 20 caracteres. |
| Configuração multi-base | Referenciar nomes de variáveis de ambiente no JSON, não valores secretos. |
| Provisionamento | Reutilizar conta e categoria já existentes antes de criar novos registros. |
| Segurança | Preferir documentação sanitizada e resultados sem segredos. |

Para detalhes e contexto, ler `references/omie-bootstrap-notes.md`.

### 5. Executar e inspecionar o retorno

Em execução real, capturar e interpretar pelo menos estes pontos:

| Item | O que verificar |
| --- | --- |
| Conta corrente | Se foi encontrada ou criada, e qual código retornou |
| Categoria | Se foi encontrada ou criada, e qual código retornou |
| Cliente de teste | Código do cliente Omie retornado |
| Conta a receber | Código do lançamento Omie e código de integração |
| Mensagem final | `descricao_status` ou corpo de erro retornado |

Quando o risco operacional for maior, iniciar por `--dry-run` no script multi-base.

### 6. Documentar e publicar sem expor segredos

Quando a tarefa também envolver reuso organizacional, documentar o procedimento no repositório com linguagem clara e anexar:

1. objetivo do fluxo;
2. parâmetros sanitizados;
3. decisões técnicas relevantes;
4. resultado validado;
5. orientação de uso com credenciais efêmeras.

Se a tarefa incluir commits e documentação pública, ler `references/repo-packaging-pattern.md` antes de escrever os arquivos finais.

## Recursos desta skill

### Scripts

| Caminho | Uso |
| --- | --- |
| `scripts/run_live_omie_smoke_test.py` | Executar smoke test real em uma base Omie com conta e categoria já definidas. |
| `scripts/run_multi_base_omie_bootstrap.py` | Operar múltiplas bases Omie, descobrindo ou criando conta corrente e categoria antes do lançamento. |

### Referências

| Caminho | Ler quando |
| --- | --- |
| `references/omie-bootstrap-notes.md` | Precisar lembrar as decisões de payload, segurança e provisionamento já validadas. |
| `references/repo-packaging-pattern.md` | Precisar transformar a execução em documentação e commits compreensíveis para um repositório público. |

### Templates

| Caminho | Uso |
| --- | --- |
| `templates/multi-base-config.example.json` | Partir de uma configuração sanitizada para execuções multi-base. |

## Padrão de saída esperado

Ao concluir uma tarefa com esta skill, preferir entregar um resumo curto com:

| Campo | Conteúdo esperado |
| --- | --- |
| Modo | `single-base` ou `multi-base` |
| Estrutura | Conta e categoria encontradas ou criadas |
| Execução | `dry-run` ou execução real |
| Resultado | Códigos Omie retornados e mensagem final |
| Segurança | Confirmação de que credenciais não foram persistidas |
| Publicação | Arquivos e commits gerados, se houver |

## Não fazer

Não persistir credenciais reais em arquivos versionados. Não assumir que uma conta corrente ou categoria existe sem consultar a API. Não multiplicar contas e categorias desnecessariamente quando uma estrutura válida já estiver presente. Não publicar documentação que revele segredos, payloads sensíveis ou caminhos privados desnecessários.
