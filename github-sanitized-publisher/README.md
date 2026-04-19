# github-sanitized-publisher

Este módulo define a disciplina de **sanitização antes da publicação**. Ele existe para reduzir o risco de expor segredos, arquivos `.env`, endpoints internos, logs, dumps, notebooks com credenciais, tokens, cookies, payloads reais, dados pessoais ou mocks inseguros ao abrir código em repositório público.

## Checklist de publicação

| Item | Regra |
| --- | --- |
| `.env` e equivalentes | Nunca publicar; manter apenas `.env.example` com placeholders. |
| Credenciais Omie | Sempre externas ao código versionado. |
| Mocks | Apenas sintéticos, mínimos e sem semelhança com produção. |
| Logs e exports | Excluir ou anonimizar antes do commit. |
| URLs internas | Remover ou substituir por domínios reservados de exemplo. |
| Dados bancários e fiscais | Não publicar em nenhuma forma identificável. |
