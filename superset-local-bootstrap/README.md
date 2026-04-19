# superset-local-bootstrap

Este diretório reúne a base para **bootstrap local do Apache Superset** com finalidade analítica, de exploração e de validação visual de dados saneados. A documentação oficial do Superset também distingue claramente o ambiente `docker compose` como opção de desenvolvimento local, não como padrão pronto para produção de alta disponibilidade.

Por essa razão, o objetivo aqui é fornecer uma base pública e segura para iniciar rapidamente um ambiente local, conectar fontes autorizadas e evoluir dashboards sem publicar segredos, metadados produtivos ou dados confidenciais.

## Diretrizes

| Tema | Diretriz |
| --- | --- |
| Credenciais | Devem ser injetadas localmente e nunca versionadas. |
| Banco de metadados | Exige backup e gestão própria fora deste template. |
| Dados de exemplo | Devem ser sintéticos ou anonimizados. |
| Perfil de uso | Focado em laboratório local, staging leve e documentação operacional. |
