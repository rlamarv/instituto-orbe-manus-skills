# Estratégia de compartilhamento seguro de acesso no GitHub

A necessidade de compartilhar a administração de um repositório público não deve ser resolvida pelo compartilhamento da **conta pessoal** do proprietário. A abordagem mais segura e governável é manter a conta pessoal apenas como identidade individual do owner e delegar o acesso ao repositório por meio de uma **organização GitHub**, com times e papéis explícitos. Essa recomendação é consistente com a documentação oficial do GitHub sobre organizações, papéis de repositório e exigência de autenticação de dois fatores [1] [2].

## Recomendação prática para o Instituto ORBE

| Tema | Recomendação |
| --- | --- |
| Conta principal | Manter sua conta pessoal como owner original e não compartilhar senha nem dispositivo de 2FA. |
| Governança | Criar uma organização dedicada, por exemplo `instituto-orbe`, e transferir ou espelhar os repositórios públicos relevantes para lá. |
| Compartilhamento operacional | Adicionar pessoas por **times** com níveis de acesso adequados, em vez de compartilhar login. |
| Automação | Se houver contas de automação, tratá-las como identidades próprias e compatíveis com 2FA quando exigido. |
| Auditoria | Usar histórico de commits, papéis de repositório e trilha de auditoria da organização para rastrear quem fez cada mudança. |

## Por que não compartilhar sua conta pessoal

Quando a conta pessoal é compartilhada, perde-se a separação entre identidade, responsabilidade e trilha de auditoria. Além disso, o próprio modelo de segurança do GitHub foi desenhado para que o acesso seja concedido a contas individuais, membros de organização, colaboradores externos e times, cada qual com permissões próprias [1] [3]. Em termos operacionais, compartilhar a conta também fragiliza a gestão do 2FA, porque várias pessoas passam a depender do mesmo segredo de login e do mesmo segundo fator.

> "You can require all members, outside collaborators, and billing managers in your organization to enable two-factor authentication on GitHub." [1]

Essa orientação reforça que a governança correta ocorre no nível da **organização**, não pelo reuso informal da conta do proprietário.

## Modelo recomendado de implantação

| Etapa | Ação |
| --- | --- |
| 1 | Criar uma organização GitHub do Instituto ORBE. |
| 2 | Manter você como owner principal da organização. |
| 3 | Convidar outros humanos ou operadores para times como `maintainers`, `reviewers` e `publishers`. |
| 4 | Definir papéis mínimos necessários por repositório, evitando acesso administrativo desnecessário. |
| 5 | Exigir 2FA na organização assim que os membros estiverem preparados para isso. |
| 6 | Se necessário, adicionar contas de automação separadas, nunca reutilizando sua conta pessoal. |

## Aplicação imediata a este repositório

Para o repositório público [`rlamarv/instituto-orbe-manus-skills`](https://github.com/rlamarv/instituto-orbe-manus-skills), a recomendação imediata é mantê-lo funcionalmente publicado na sua conta atual, mas preparar uma próxima etapa de governança institucional. Isso pode ser feito criando uma organização do Instituto ORBE e então transferindo o repositório ou mantendo um espelho controlado, sempre com acesso concedido por papéis e times, não por compartilhamento de login.

## Referências

[1] [GitHub Docs — Requiring two-factor authentication in your organization](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization)

[2] [GitHub Docs — Managing team access to an organization repository](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/managing-team-access-to-an-organization-repository)

[3] [GitHub Docs — About two-factor authentication](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication)
