---
name: omie-secure-bootstrap
description: Executar bootstrap seguro de integrações Omie. Use para smoke tests reais, operação multi-base com credenciais efêmeras, provisionamento de conta corrente e categoria por API, e documentação pública sanitizada do processo.
---

# Omie Secure Bootstrap

## Quando usar

Use esta skill quando a tarefa envolver **validar uma base Omie**, **operar várias bases** ou **provisionar a estrutura mínima por API** sem salvar segredos no repositório.

| Cenário | Recurso |
| --- | --- |
| Base única com estrutura já conhecida | `scripts/run_live_omie_smoke_test.py` |
| Múltiplas bases ou estrutura incerta | `scripts/run_multi_base_omie_bootstrap.py` |
| Configuração sanitizada multi-base | `templates/multi-base-config.example.json` |
| Detalhes de payload e decisões validadas | `references/omie-bootstrap-notes.md` |
| Empacotamento em repositório público | `references/repo-packaging-pattern.md` |

## Workflow

### 1. Proteger segredos

Usar `app_key` e `app_secret` apenas em variáveis de ambiente de runtime. Não salvar credenciais reais em arquivos versionados, exemplos públicos ou documentação.

### 2. Escolher o modo

Se a tarefa for de **base única** e a conta corrente e categoria já forem conhecidas, usar `run_live_omie_smoke_test.py`.

Se a tarefa for **multi-base** ou exigir descoberta e criação de estrutura, usar `run_multi_base_omie_bootstrap.py`.

### 3. Resolver a estrutura mínima

Seguir sempre esta ordem:

1. localizar conta corrente;
2. criar conta corrente se não existir;
3. localizar categoria;
4. criar categoria se não existir;
5. criar cliente de teste transitório;
6. criar conta a receber de teste.

### 4. Aplicar as regras já validadas

| Ponto | Regra |
| --- | --- |
| Conta a receber | Usar `id_conta_corrente`. |
| Documento de teste | Limitar a 20 caracteres. |
| Multi-base | Referenciar nomes de variáveis de ambiente, não segredos. |
| Provisionamento | Reutilizar estruturas existentes antes de criar novas. |
| Segurança | Preferir `--dry-run` quando houver risco ou incerteza. |

### 5. Registrar o resultado

Ao concluir, reportar de forma curta:

| Campo | Conteúdo |
| --- | --- |
| Modo | `single-base` ou `multi-base` |
| Estrutura | Conta e categoria encontradas ou criadas |
| Execução | `dry-run` ou real |
| Resultado | Códigos Omie retornados e mensagem final |
| Segurança | Confirmação de que segredos não foram persistidos |

## Recursos

| Caminho | Uso |
| --- | --- |
| `scripts/run_live_omie_smoke_test.py` | Smoke test real em uma base Omie. |
| `scripts/run_multi_base_omie_bootstrap.py` | Bootstrap e execução em várias bases. |
| `references/omie-bootstrap-notes.md` | Regras e decisões técnicas já validadas. |
| `references/repo-packaging-pattern.md` | Padrão de commits e documentação pública. |
| `templates/multi-base-config.example.json` | Exemplo sanitizado de configuração. |

## Não fazer

Não persistir credenciais reais. Não assumir existência prévia de conta ou categoria sem consultar a API. Não duplicar estruturas desnecessariamente. Não publicar logs ou documentação com segredos ou dados privados.
