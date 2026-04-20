# instituto-orbe-manus-skills

Este repositório foi estruturado para **publicação supervisionada de código sanitizado por IA** no contexto do Instituto ORBE, com foco em integrações de dados que precisem permanecer públicas sem expor credenciais, arquivos `.env`, cargas de teste inseguras, segredos operacionais ou dados sensíveis de terceiros.

Este projeto integra-se ao [Omie.ERP][omie].

---

### ⚠️ Disclaimer Experimental
Este é um **projeto experimental** em estágio de desenvolvimento. O código é fornecido "COMO ESTÁ" (AS IS), sem garantias de qualquer tipo, expressas ou implícitas. O uso deste software é de total responsabilidade do usuário. O Instituto ORBE não se responsabiliza por quaisquer danos ou perdas decorrentes do uso deste código.

---

## 📑 Índice Navegável

1.  [🚀 Guia Rápido: Importação de Contas a Receber via XML (NFCom) no Omie.ERP](#-guia-rápido-importação-de-contas-a-receber-via-xml-nfcom-no-omieerp)
2.  [⚖️ Licença](#️-licença)
3.  [🏗️ Princípios de Publicação](#️-princípios-de-publicação)
4.  [📂 Estrutura Inicial](#-estrutura-inicial)
5.  [⚙️ Parâmetros Funcionais](#️-parâmetros-funcionais)
6.  [📜 Scripts de Integração Omie](#-scripts-de-integração-omie)
7.  [🧠 Habilidade Reutilizável (Skill)](#-habilidade-reutilizável-skill)
8.  [🔗 Referências e Avisos Legais](#-referências-e-avisos-legais)

---

## 🚀 Guia Rápido: Importação de Contas a Receber via XML (NFCom) no Omie.ERP

Siga estes passos para processar Notas Fiscais de Comunicação (NFCom) e gerar lançamentos no [Omie.ERP][omie] com segurança:

1.  **Obtenha o código e prepare o ambiente:**
    ```bash
    git clone https://github.com/rlamarv/instituto-orbe-manus-skills.git
    cd instituto-orbe-manus-skills
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Prepare seus dados de entrada:**
    Crie uma pasta para seus XMLs e coloque os arquivos `.xml` nela:
    ```bash
    mkdir xml_input
    # Copie seus arquivos NFCom para a pasta xml_input/
    ```

3.  **Configure seus segredos (efêmeros):**
    Exporte suas chaves da Omie como variáveis de ambiente no terminal:
    ```bash
    export OMIE_APP_KEY="SUA_CHAVE_AQUI"
    export OMIE_APP_SECRET="SEU_SECRET_AQUI"
    ```

4.  **Crie seu `config.json` (SAMPLE):**
    Crie um arquivo chamado `config.json` na raiz do projeto com este conteúdo, garantindo que `app_key_env` aponte para o **nome** da variável exportada:
    ```json
    [
      {
        "base_name": "Minha Base Omie",
        "app_key_env": "OMIE_APP_KEY",
        "app_secret_env": "OMIE_APP_SECRET",
        "target_account_name": "Meta Pay - Caixinha Manus",
        "target_account_type": "CC",
        "target_category_description": "Recebimentos de NFCom",
        "amount": 1.00
      }
    ]
    ```

5.  **Execute a importação:**
    ```bash
    python3 omie-xml-intake/scripts/process_xml_to_omie.py \
      --xml-dir ./xml_input/ \
      --config-file config.json
    ```

*Para detalhes completos e avançados, consulte o [Guia Técnico de Execução](docs/guia-tecnico-execucao.md).*

---

## ⚖️ Licença

Este projeto está licenciado sob a **MIT License**.

> **MIT License**
>
> Copyright (c) 2026 Instituto ORBE
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🏗️ Princípios de Publicação

| Princípio | Aplicação neste repositório |
| --- | --- |
| Segregação de segredos | Nenhuma chave real, segredo, token, senha, cookie ou `.env` privado deve ser versionado. |
| Sanitização obrigatória | Mocks inseguros, dados identificáveis, endpoints privados e exemplos derivados de produção devem ser removidos ou substituídos por amostras sintéticas. |
| Docker first | Cada módulo é preparado para execução controlada em containers, com variáveis injetadas em tempo de execução. |
| Reprodutibilidade | O repositório prioriza templates, exemplos mínimos e documentação explícita de bootstrap. |
| Evolução segura | O código público deve permitir extensão futura para Airflow, Superset, webhooks e orquestração sem refatoração destrutiva. |

## 📂 Estrutura Inicial

| Pasta | Finalidade |
| --- | --- |
| `github-sanitized-publisher/` | Procedimentos, utilitários e convenções para sanitizar código antes da publicação pública. |
| `omie-xml-intake/` | Base do primeiro projeto, dedicada à ingestão de XML e parametrização segura para operações Omie. |
| `airflow-dag-generator/` | Geração e organização de DAGs a partir de pipelines saneados e configuráveis. |
| `superset-local-bootstrap/` | Bootstrap local do Superset para exploração analítica e visualização de dados. |
| `docker-secure-runtime/` | Runtime containerizado com foco em isolamento, injeção de variáveis e composição local segura. |
| `docs/` | Documentação de arquitetura, segurança, sanitização e operação. |
| `templates/` | Modelos públicos de configuração e arquivos de exemplo. |

## ⚙️ Parâmetros Funcionais

O primeiro projeto deve ser estruturado para receber, fora do Git, os seguintes parâmetros operacionais:

| Parâmetro | Diretriz de tratamento |
| --- | --- |
| Repositório de XML ou pasta de entrada | Informado por caminho local, volume Docker ou conector externo, sem caminhos internos sensíveis hardcoded. |
| Conta corrente a receber | Mantida como parâmetro operacional, sem dados produtivos reais no repositório. |
| Categoria da conta corrente a receber | Mantida como parâmetro externo ou catálogo saneado. |
| API Key da Omie | Somente via ambiente local ou segredo injetado em runtime. |
| API Secret da Omie | Somente via ambiente local ou segredo injetado em runtime. |

## 📜 Scripts de Integração Omie

### `omie-xml-intake/scripts/run_multi_base_omie_bootstrap.py`
Provisiona estrutura mínima (contas correntes, categorias) e realiza smoke test em múltiplas bases Omie.

### `omie-xml-intake/scripts/process_xml_to_omie.py`
Processa arquivos XML de NFCom e cria contas a receber correspondentes na API da Omie.

## 🧠 Habilidade Reutilizável (Skill)

O fluxo consolidado de bootstrap seguro da Omie também foi formalizado como uma **skill reutilizável**, permitindo reaproveitar o processo em novas execuções sem depender apenas do histórico desta conversa.

| Recurso | Local |
| --- | --- |
| Skill operacional | `/home/ubuntu/skills/omie-secure-bootstrap/` |
| Espelho versionado no repositório | `skills/omie-secure-bootstrap/` |
| Documento explicativo | `docs/omie-secure-bootstrap-skill.md` |

---

## 🔗 Referências e Avisos Legais

### Referências
- **Omie.ERP** – [https://www.omie.com.br/](https://www.omie.com.br/)

### Aviso Legal
Omie.ERP é uma marca registrada de seus respectivos proprietários. Este projeto é uma iniciativa independente do Instituto ORBE e **não possui afiliação oficial** com a Omie.

[omie]: https://www.omie.com.br/
