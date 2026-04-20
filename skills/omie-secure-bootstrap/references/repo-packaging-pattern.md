# Padrão de empacotamento no repositório

## Objetivo

Usar esta referência quando a tarefa não terminar apenas na execução técnica da Omie, mas também precisar resultar em **commits compreensíveis, documentação pública sanitizada e trilha de auditoria útil para terceiros**.

## Estrutura recomendada no repositório

Distribuir o material em duas camadas:

| Camada | Finalidade |
| --- | --- |
| Código reutilizável | Scripts, templates e módulos executáveis dentro do diretório funcional do projeto. |
| Documentação pública | Arquivos em `docs/` ou diretórios equivalentes, explicando objetivo, parâmetros sanitizados, validação e limites operacionais. |

## Conteúdo mínimo da documentação pública

Sempre que um fluxo Omie for formalizado no repositório, explicar pelo menos:

1. o problema que o script resolve;
2. quando usar o script;
3. quais parâmetros são esperados;
4. quais decisões de segurança foram adotadas;
5. o que foi validado de forma real e o que continua sendo template.

## Padrão de commit

Preferir commits pequenos e semanticamente claros. Alguns padrões úteis são:

| Tipo de alteração | Exemplo de mensagem |
| --- | --- |
| Novo script reutilizável | `Add multi-base Omie bootstrap runner` |
| Documentação de validação | `Document live Omie smoke test flow` |
| Empacotamento da skill | `Package Omie bootstrap workflow as reusable skill` |

## Regras de publicação

Não publicar credenciais, `.env` reais, payloads sensíveis completos ou dados privados do ambiente original. Quando um resultado real for documentado, reter apenas os identificadores e mensagens realmente úteis para auditoria, evitando qualquer detalhe que comprometa segurança ou privacidade.
