# Notas de bootstrap Omie

## Objetivo

Esta referência resume as decisões operacionais já validadas durante a criação do fluxo público do Instituto ORBE para Omie. Ler este arquivo quando for necessário reexecutar o processo, adaptá-lo para outra base ou explicar por que certos campos e passos foram escolhidos.

## Sequência mínima validada

| Etapa | Ação |
| --- | --- |
| 1 | Listar contas correntes e tentar localizar a desejada pelo nome. |
| 2 | Criar a conta corrente com `IncluirContaCorrente` se ela não existir. |
| 3 | Listar categorias e tentar localizar a descrição desejada. |
| 4 | Criar a categoria com `IncluirCategoria` se ela não existir. |
| 5 | Criar um cliente de teste transitório com `UpsertClienteCpfCnpj`. |
| 6 | Criar a conta a receber com `IncluirContaReceber`. |

## Campos e decisões importantes

### Conta corrente

Para criação de conta corrente, o exemplo mínimo publicado pela Omie foi suficiente como referência de bootstrap: `cCodCCInt`, `tipo_conta_corrente`, `codigo_banco`, `descricao` e `saldo_inicial`.

### Categoria

Para criação de categoria, usar `categoria_superior`, `descricao` e `natureza`. Quando o grupo exato ainda não for conhecido, começar pela família superior `1.01` para receitas, desde que isso faça sentido para o caso do usuário.

### Conta a receber

Para o lançamento de conta a receber, a decisão já validada foi:

| Campo | Regra |
| --- | --- |
| `id_conta_corrente` | Usar este campo para vincular a conta corrente do lançamento. |
| `numero_documento` | Limitar a até 20 caracteres. |
| `numero_documento_fiscal` | Manter alinhado ao identificador curto do lançamento. |
| `codigo_categoria` | Usar o código real da categoria encontrada ou criada. |
| `codigo_lancamento_integracao` | Gerar valor curto, único e rastreável. |

## Estratégia de busca antes de criar

Sempre tentar localizar por nome antes de criar. Isso evita proliferação de contas correntes e categorias similares na mesma base.

| Objeto | Estratégia |
| --- | --- |
| Conta corrente | Comparar `descricao` por igualdade normalizada e depois por correspondência parcial. |
| Categoria | Comparar `descricao` por igualdade normalizada e depois por correspondência parcial. |

## Política de segredos

Não salvar `app_key` e `app_secret` em arquivos versionados. Não mover credenciais reais para `.env.example`. Não registrar corpos completos de requisição ou resposta se eles contiverem segredos. Preferir sempre variáveis de ambiente efêmeras no momento da execução.

## Quando usar dry run

Usar `--dry-run` quando o usuário quiser validar o plano de ação em múltiplas bases sem criar registros ainda, ou quando a estrutura esperada da base for desconhecida e o impacto precise ser observado primeiro.
