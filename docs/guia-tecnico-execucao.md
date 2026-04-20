# Guia Técnico de Execução: Integração Omie via XML

Este guia descreve o procedimento padrão para configurar e executar o processamento de arquivos XML de NFCom para a criação de contas a receber na API da Omie, garantindo a **segregação de segredos** e a **reprodutibilidade** do ambiente.

## 1. Preparação do Ambiente Local

O projeto utiliza Python 3.11+ e recomenda o uso de ambientes virtuais para isolamento de dependências.

```bash
# 1. Clonar o repositório
git clone https://github.com/rlamarv/instituto-orbe-manus-skills.git
cd instituto-orbe-manus-skills

# 2. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt
```

## 2. Configuração de Segurança (Segredos)

**Nunca** insira chaves de API diretamente em arquivos de configuração ou no código. Utilize variáveis de ambiente efêmeras no terminal.

```bash
# Defina as credenciais da sua base Omie
export OMIE_APP_KEY="SUA_CHAVE_AQUI"
export OMIE_APP_SECRET="SEU_SECRET_AQUI"
```

## 3. Parametrização Operacional (`config.json`)

Crie um arquivo `config.json` na raiz do projeto. Este arquivo mapeia os nomes das variáveis de ambiente definidas no passo anterior para as configurações específicas da base.

```json
[
  {
    "base_name": "Nome da Sua Base",
    "app_key_env": "OMIE_APP_KEY",
    "app_secret_env": "OMIE_APP_SECRET",
    "target_account_name": "Meta Pay - Caixinha Manus",
    "target_account_type": "CC",
    "target_category_description": "Recebimentos de NFCom",
    "amount": 1.00
  }
]
```

## 4. Execução do Processamento

O script de processamento lê os XMLs de um diretório de entrada e realiza as chamadas de API conforme a configuração.

### Modo de Simulação (Dry-Run)
Recomendado para validar a extração de dados e a formação dos payloads sem afetar a base real.
```bash
python3 omie-xml-intake/scripts/process_xml_to_omie.py \
  --xml-dir ./xml_input/ \
  --config-file config.json \
  --dry-run
```

### Execução Real
```bash
python3 omie-xml-intake/scripts/process_xml_to_omie.py \
  --xml-dir ./xml_input/ \
  --config-file config.json
```

## 5. Fluxo de Trabalho do Script

1.  **Validação de Ambiente:** Verifica se as variáveis de ambiente citadas no `config.json` estão presentes.
2.  **Resolução de Estrutura:** Localiza a Conta Corrente e a Categoria na Omie pelos nomes fornecidos.
3.  **Iteração de XMLs:** Para cada arquivo no diretório `--xml-dir`:
    *   Extrai CNPJ, Valor, Vencimento e Número da NFCom.
    *   Executa `UpsertClienteCpfCnpj` para garantir que o destinatário existe na base.
    *   Executa `IncluirContaReceber` usando um código de integração único (`NFCOM-{numero}-{cnpj}`).

---
**Nota de Supervisão:** Este processo foi validado em ambiente macOS/Linux e segue os padrões de segurança do Instituto ORBE.
