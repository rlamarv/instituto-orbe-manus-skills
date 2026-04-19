# docker-secure-runtime

Este diretório centraliza a composição local segura do projeto, com foco em isolamento, persistência explícita, rede interna e injeção de configuração em tempo de execução. O objetivo é permitir reprodução local e staging controlado sem cristalizar segredos no repositório.

## Escopo

| Serviço | Papel |
| --- | --- |
| PostgreSQL | Persistência operacional e metadados locais. |
| Redis | Mensageria e apoio a orquestração local. |
| omie-xml-intake | Processo de ingestão saneado do primeiro projeto. |

A composição aqui presente deve ser entendida como **base pública de referência**, não como manifesto final de produção. |
