# Habilidade reutilizável: omie-secure-bootstrap

Este documento registra a formalização do processo usado nesta automação como uma **habilidade reutilizável**. O objetivo foi transformar um fluxo operacional que já havia sido validado em uma base Omie em um pacote reaproveitável por outras instâncias, preservando as decisões de segurança, os scripts de execução e a lógica de documentação sanitizada.

## O que a habilidade cobre

A skill `omie-secure-bootstrap` foi criada para atender quatro necessidades recorrentes.

| Capacidade | Descrição |
| --- | --- |
| Smoke test em base única | Executa um teste real controlado na Omie usando conta corrente e categoria já definidas. |
| Bootstrap multi-base | Percorre várias bases Omie e cria conta corrente e categoria por API quando a estrutura ainda não existe. |
| Segurança de credenciais | Usa apenas variáveis de ambiente efêmeras e evita persistência de segredos em arquivos versionados. |
| Empacotamento público | Orienta como transformar a execução em commits e documentação compreensíveis para terceiros. |

## Onde a skill está estruturada

Para permitir inspeção pública por interessados, a skill foi organizada em dois lugares complementares.

| Local | Finalidade |
| --- | --- |
| `/home/ubuntu/skills/omie-secure-bootstrap/` | Diretório operacional da skill para uso por outra instância. |
| `skills/omie-secure-bootstrap/` | Espelho versionado no repositório público para auditoria, estudo e reaproveitamento. |

## Conteúdo incluído

| Caminho | Papel |
| --- | --- |
| `skills/omie-secure-bootstrap/SKILL.md` | Instruções centrais, critérios de uso e workflow da skill. |
| `skills/omie-secure-bootstrap/scripts/run_live_omie_smoke_test.py` | Script de validação real para uma base Omie. |
| `skills/omie-secure-bootstrap/scripts/run_multi_base_omie_bootstrap.py` | Script de bootstrap multi-base com provisionamento condicional. |
| `skills/omie-secure-bootstrap/references/omie-bootstrap-notes.md` | Decisões técnicas já validadas no processo Omie. |
| `skills/omie-secure-bootstrap/references/repo-packaging-pattern.md` | Padrão de commits e documentação pública sanitizada. |
| `skills/omie-secure-bootstrap/templates/multi-base-config.example.json` | Template sanitizado para configuração multi-base. |

## Decisão de desenho

A habilidade foi modelada com foco em **workflow** e **progressive disclosure**. Isso significa que o `SKILL.md` permanece enxuto e operacional, enquanto os detalhes reutilizáveis ficam em arquivos de referência separados. Dessa forma, a skill continua legível para execução rápida, sem perder a memória das decisões importantes já validadas durante a automação Omie.

## Resultado prático

Com essa formalização, o processo deixa de existir apenas como histórico de conversa ou conjunto de commits isolados. Ele passa a existir também como um ativo reutilizável, pronto para ser acionado quando houver necessidade de bootstrap seguro da Omie, smoke test supervisionado ou empacotamento público de uma integração semelhante.

## Validação da habilidade

A skill foi validada com o verificador oficial do fluxo `skill-creator`, confirmando que a estrutura em `/home/ubuntu/skills/omie-secure-bootstrap/` atende aos requisitos formais de uma habilidade reutilizável antes do versionamento público do espelho no repositório.
