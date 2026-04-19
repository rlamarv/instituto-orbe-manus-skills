# airflow-dag-generator

Este módulo é reservado para a geração e organização de **DAGs saneadas** a partir dos pipelines públicos do projeto. A intenção é manter a lógica de orquestração desacoplada da configuração privada, permitindo que o código publicado seja reutilizável sem revelar nomes internos de servidores, bases, credenciais ou rotinas operacionais sensíveis.

A documentação oficial do Airflow deixa claro que o uso de `docker compose` é adequado para estudo, desenvolvimento e staging leve, mas não deve ser tratado como implantação produtiva endurecida. Por isso, este diretório deve concentrar DAGs públicas, fábricas de DAGs, validações e exemplos sintéticos, preservando fora do Git toda a configuração privada.

## Diretrizes

| Tema | Diretriz |
| --- | --- |
| Configuração | Variáveis, conexões e segredos devem ser resolvidos em runtime. |
| DAGs | Devem ser idempotentes, legíveis e desacopladas de caminhos privados. |
| Conectores | Nunca embutir chaves de API, URLs internas ou credenciais em código-fonte. |
| Exemplos | Usar apenas cargas sintéticas ou metadados anônimos. |
| Produção | Documentar que produção exige endurecimento adicional fora deste template. |
