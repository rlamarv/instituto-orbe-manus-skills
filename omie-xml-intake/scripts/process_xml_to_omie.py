#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional
import xml.etree.ElementTree as ET

import requests

# URLs da API Omie (copiadas de run_multi_base_omie_bootstrap.py)
CONTAS_URL = "https://app.omie.com.br/api/v1/geral/contacorrente/"
CATEGORIAS_URL = "https://app.omie.com.br/api/v1/geral/categorias/"
CLIENTES_URL = "https://app.omie.com.br/api/v1/geral/clientes/"
CONTAS_RECEBER_URL = "https://app.omie.com.br/api/v1/financas/contareceber/"
REQUEST_TIMEOUT = 60
PAGE_SIZE = 100

# Namespace para o XML da NFCom
NS = {'nfcom': 'http://www.portalfiscal.inf.br/nfcom'}

class OmieClient:
    def __init__(self, base_name: str, app_key: str, app_secret: str, dry_run: bool = False):
        self.base_name = base_name
        self.app_key = app_key
        self.app_secret = app_secret
        self.dry_run = dry_run

    def post(self, url: str, call: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = {
            "call": call,
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": [payload],
        }
        if self.dry_run and call.startswith("Incluir"):
            print(f"DRY RUN: {call} - {payload}")
            return {"codigo_status": "0", "descricao_status": f"DRY RUN {call}", "call": call, "payload": payload}
        
        response = requests.post(url, json=body, timeout=REQUEST_TIMEOUT)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Base={self.base_name} call={call} status={response.status_code} body={response.text}"
            ) from exc
        return response.json()

def getenv_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente obrigatória ausente: {name}")
    return value

def normalize(text: Optional[str]) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text).strip()).casefold()

def iter_objects(node: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from iter_objects(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_objects(item)

def get_total_pages(data: Dict[str, Any]) -> int:
    total = data.get("total_de_paginas") or data.get("total_paginas") or 1
    try:
        return max(1, int(total))
    except Exception:
        return 1

def list_accounts(client: OmieClient) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    page = 1
    while True:
        response = client.post(
            CONTAS_URL,
            "ListarContasCorrentes",
            {"pagina": page, "registros_por_pagina": PAGE_SIZE},
        )
        for obj in iter_objects(response):
            if obj.get("nCodCC") and obj.get("descricao"):
                results.append(obj)
        if page >= get_total_pages(response):
            break
        page += 1
    dedup: Dict[int, Dict[str, Any]] = {}
    for item in results:
        dedup[int(item["nCodCC"])] = item
    return list(dedup.values())

def list_categories(client: OmieClient) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    page = 1
    while True:
        response = client.post(
            CATEGORIAS_URL,
            "ListarCategorias",
            {"pagina": page, "registros_por_pagina": PAGE_SIZE},
        )
        for obj in iter_objects(response):
            if obj.get("codigo") and obj.get("descricao"):
                results.append(obj)
        if page >= get_total_pages(response):
            break
        page += 1
    dedup: Dict[str, Dict[str, Any]] = {}
    for item in results:
        dedup[str(item["codigo"])] = item
    return list(dedup.values())

def find_account_by_name(accounts: List[Dict[str, Any]], desired_name: str) -> Optional[Dict[str, Any]]:
    desired = normalize(desired_name)
    for item in accounts:
        if normalize(item.get("descricao")) == desired:
            return item
    for item in accounts:
        if desired in normalize(item.get("descricao")):
            return item
    return None

def find_category_by_description(categories: List[Dict[str, Any]], desired_description: str) -> Optional[Dict[str, Any]]:
    desired = normalize(desired_description)
    for item in categories:
        if normalize(item.get("descricao")) == desired:
            return item
    for item in categories:
        if desired in normalize(item.get("descricao")):
            return item
    return None

def upsert_client(client: OmieClient, cnpj_cpf: str, razao_social: str, nome_fantasia: str, email: str) -> Dict[str, Any]:
    payload = {
        "cnpj_cpf": cnpj_cpf,
        "razao_social": razao_social,
        "nome_fantasia": nome_fantasia,
        "email": email,
        "observacao": f"Cliente criado via automação Manus para base {client.base_name}.",
    }
    return client.post(CLIENTES_URL, "UpsertClienteCpfCnpj", payload)

def include_receivable(
    client: OmieClient,
    codigo_cliente: int,
    account_code: int,
    category_code: str,
    amount: float,
    due_date: str,
    integration_code: str,
    document_number: str,
    description: str
) -> Dict[str, Any]:
    payload = {
        "codigo_lancamento_integracao": integration_code,
        "codigo_cliente_fornecedor": int(codigo_cliente),
        "data_vencimento": due_date,
        "data_previsao": due_date, # Usar a mesma data de vencimento como previsão
        "valor_documento": float(amount),
        "codigo_categoria": category_code,
        "id_conta_corrente": int(account_code),
        "numero_documento": document_number,
        "numero_documento_fiscal": document_number, # Usar o mesmo número de documento
        "observacao": description,
    }
    return client.post(CONTAS_RECEBER_URL, "IncluirContaReceber", payload)

def parse_nfcom_xml(xml_path: str) -> Dict[str, Any]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    nfcom_data = {}

    # Extrair dados do emitente (para o cliente Omie)
    emit_cnpj = root.find('.//nfcom:emit/nfcom:CNPJ', NS).text
    emit_xNome = root.find('.//nfcom:emit/nfcom:xNome', NS).text

    # Extrair dados do destinatário (para o cliente Omie)
    dest_cnpj = root.find('.//nfcom:dest/nfcom:CNPJ', NS).text
    dest_xNome = root.find('.//nfcom:dest/nfcom:xNome', NS).text

    # Priorizar o destinatário como cliente, mas usar emitente se destinatário não tiver CNPJ
    client_cnpj = dest_cnpj if dest_cnpj else emit_cnpj
    client_xNome = dest_xNome if dest_xNome else emit_xNome

    nfcom_data['client_cnpj'] = client_cnpj
    nfcom_data['client_razao_social'] = client_xNome
    nfcom_data['client_nome_fantasia'] = client_xNome # Assumir o mesmo por enquanto
    nfcom_data['client_email'] = "contato@example.com" # Placeholder, XML não tem email do cliente

    # Data de emissão
    dhEmi_str = root.find('.//nfcom:ide/nfcom:dhEmi', NS).text
    nfcom_data['data_emissao'] = datetime.fromisoformat(dhEmi_str).strftime('%d/%m/%Y')

    # Valor total da NFCom
    vNF_str = root.find('.//nfcom:total/nfcom:vNF', NS).text
    nfcom_data['valor_total'] = float(vNF_str)

    # Data de vencimento da fatura
    dVencFat_str = root.find('.//nfcom:gFat/nfcom:dVencFat', NS).text
    nfcom_data['data_vencimento'] = datetime.strptime(dVencFat_str, '%Y-%m-%d').strftime('%d/%m/%Y')

    # Número da NFCom para usar como número de documento e código de integração
    nNF = root.find('.//nfcom:ide/nfcom:nNF', NS).text
    nfcom_data['numero_documento'] = nNF
    nfcom_data['codigo_integracao'] = f"NFCOM-{nNF}-{client_cnpj}"
    nfcom_data['description'] = f"NFCom {nNF} - {client_xNome}"

    return nfcom_data

def main():
    parser = argparse.ArgumentParser(
        description="Processa arquivos XML de NFCom e cria contas a receber na Omie."
    )
    parser.add_argument(
        "--xml-dir",
        required=True,
        help="Diretório contendo os arquivos XML de NFCom a serem processados."
    )
    parser.add_argument(
        "--config-file",
        required=True,
        help="Arquivo JSON com a lista de bases Omie e parâmetros por base."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Não envia chamadas de inclusão; apenas resolve a estrutura e mostra o que faria."
    )
    args = parser.parse_args()

    config = json.load(open(args.config_file, 'r', encoding='utf-8'))

    for base_cfg in config:
        base_name = base_cfg["base_name"]
        app_key = getenv_required(base_cfg["app_key_env"])
        app_secret = getenv_required(base_cfg["app_secret_env"])
        client = OmieClient(base_name=base_name, app_key=app_key, app_secret=app_secret, dry_run=args.dry_run)

        print(f"\nProcessando base: {base_name}")

        # Obter conta corrente e categoria (reutilizando lógica do bootstrap)
        accounts = list_accounts(client)
        categories = list_categories(client)

        target_account_name = base_cfg["target_account_name"]
        target_category_description = base_cfg["target_category_description"]

        account_info = find_account_by_name(accounts, target_account_name)
        if not account_info:
            print(f"Erro: Conta corrente '{target_account_name}' não encontrada na base {base_name}. Certifique-se de que ela foi provisionada ou existe.")
            continue
        account_code = int(account_info["nCodCC"])

        category_info = find_category_by_description(categories, target_category_description)
        if not category_info:
            print(f"Erro: Categoria '{target_category_description}' não encontrada na base {base_name}. Certifique-se de que ela foi provisionada ou existe.")
            continue
        category_code = str(category_info["codigo"])

        for xml_file in os.listdir(args.xml_dir):
            if xml_file.endswith('.xml'):
                xml_path = os.path.join(args.xml_dir, xml_file)
                print(f"  Processando XML: {xml_file}")
                try:
                    nfcom_data = parse_nfcom_xml(xml_path)

                    # 1. Garantir que o cliente existe na Omie
                    client_resp = upsert_client(
                        client=client,
                        cnpj_cpf=nfcom_data['client_cnpj'],
                        razao_social=nfcom_data['client_razao_social'],
                        nome_fantasia=nfcom_data['client_nome_fantasia'],
                        email=nfcom_data['client_email']
                    )
                    codigo_cliente = (
                        client_resp.get("codigo_cliente_omie")
                        or client_resp.get("codigo_cliente")
                        or client_resp.get("codigo_cliente_fornecedor")
                    )
                    if not codigo_cliente:
                        raise RuntimeError(f"Não foi possível obter o código do cliente para {nfcom_data['client_cnpj']}: {client_resp}")

                    # 2. Incluir conta a receber
                    receivable_resp = include_receivable(
                        client=client,
                        codigo_cliente=int(codigo_cliente),
                        account_code=account_code,
                        category_code=category_code,
                        amount=nfcom_data['valor_total'],
                        due_date=nfcom_data['data_vencimento'],
                        integration_code=nfcom_data['codigo_integracao'],
                        document_number=nfcom_data['numero_documento'],
                        description=nfcom_data['description']
                    )
                    print(f"    Conta a receber para {nfcom_data['client_razao_social']} ({nfcom_data['numero_documento']}) criada/atualizada: {receivable_resp.get('descricao_status', 'OK')}")

                except Exception as e:
                    print(f"    Erro ao processar {xml_file}: {e}")

if __name__ == "__main__":
    main()
    main()
