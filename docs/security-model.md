# Modelo de segurança para publicação pública

A abertura deste repositório segue o princípio de **publicar estrutura, não segredos**. Em termos práticos, o código público deve permitir entendimento, reprodução controlada e evolução do projeto, mas não pode revelar material que permita acesso indevido a contas, ambientes, integrações ou dados de negócio.

## Superfícies de risco consideradas

| Superfície | Risco principal | Tratamento exigido |
| --- | --- | --- |
| Arquivos `.env` | Exposição direta de credenciais e parâmetros privados | Nunca versionar; manter apenas modelos com placeholders. |
| Mocks e fixtures | Vazamento indireto de dados reais ou estrutura produtiva | Substituir por amostras sintéticas e mínimas. |
| Scripts auxiliares | Hardcodes de URL, token, usuário, senha ou path interno | Revisar e parametrizar antes do commit. |
| Logs e notebooks | Vazamento acidental de payloads, stack traces e dados operacionais | Excluir ou limpar integralmente antes da publicação. |
| Compose e Dockerfiles | Fixação indevida de segredos ou portas sensíveis | Usar variáveis externas, rede interna e portas mínimas necessárias. |
| Metadados analíticos | Exposição de nomes de clientes, contas e fluxos internos | Anonimizar ou remover. |

## Regras para credenciais Omie

As credenciais da Omie devem existir apenas em ambiente local ou em mecanismo externo de segredo, nunca em banco de dados versionado e nunca em arquivos públicos do repositório. O código deve assumir a presença de `OMIE_APP_KEY` e `OMIE_APP_SECRET` apenas em tempo de execução.

## Regras para o primeiro projeto

O primeiro projeto deve aceitar parâmetros de pasta de XML, conta corrente a receber e categoria de conta a receber sem congelar valores internos do ambiente de origem. Os exemplos publicados devem ser meramente demonstrativos, preservando a lógica de configuração sem reproduzir dados reais.

## Critério para tornar o repositório público

O repositório só deve mudar de visibilidade após a conclusão dos seguintes pontos:

| Critério | Estado necessário |
| --- | --- |
| Credenciais removidas | Nenhum segredo residual no histórico ou nos arquivos atuais. |
| `.env` saneado | Apenas `.env.example` ou template público. |
| Mocks revisados | Sem dados reais, dados bancários, fiscais ou identificáveis. |
| Documentação pronta | Bootstrap local descrito e responsabilidades de segurança explícitas. |
| Revisão do código-fonte | Concluída sobre a base sensível original do usuário. |
