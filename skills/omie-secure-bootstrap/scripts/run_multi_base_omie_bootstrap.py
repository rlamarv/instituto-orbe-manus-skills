#!/usr/bin/env python3
import argparse
import json
import os
import random
import re
import sys
import time
from datetime import date, timedelta
from typing import Any, Dict, Iterable, List, Optional

import requests

CONTAS_URL = "https://app.omie.com.br/api/v1/geral/contacorrente/"
CATEGORIAS_URL = "https://app.omie.com.br/api/v1/geral/categorias/"
CLIENTES_URL = "https://app.omie.com.br/api/v1/geral/clientes/"
CONTAS_RECEBER_URL = "https://app.omie.com.br/api/v1/financas/contareceber/"
REQUEST_TIMEOUT = 60
PAGE_SIZE = 100


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
            return {
                "codigo_status": "0",
                "descricao_status": f"DRY RUN {call}",
                "call": call,
                "payload": payload,
            }
        response = requests.post(url, json=body, timeout=REQUEST_TIMEOUT)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Base={self.base_name} call={call} status={response.status_code} body={response.text}"
            ) from exc
        return response.json()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Provisiona estrutura mínima e executa smoke test em múltiplas bases Omie sem persistir credenciais."
    )
    parser.add_argument(
        "--config-file",
        required=True,
        help="Arquivo JSON com a lista de bases Omie e parâmetros por base.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Não envia chamadas de inclusão; apenas resolve a estrutura e mostra o que faria.",
    )
    return parser.parse_args()


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)



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



def build_c_cod_cc_int(base_name: str, description: str) -> str:
    raw = f"{base_name}-{description}".upper()
    clean = re.sub(r"[^A-Z0-9]+", "", raw)
    return clean[:20] or f"CC{random.randint(1000,9999)}"



def ensure_account(client: OmieClient, base_cfg: Dict[str, Any]) -> Dict[str, Any]:
    desired_name = base_cfg["target_account_name"]
    accounts = list_accounts(client)
    found = find_account_by_name(accounts, desired_name)
    if found:
        return {
            "created": False,
            "codigo": int(found["nCodCC"]),
            "descricao": found.get("descricao"),
            "tipo": found.get("tipo_conta_corrente") or found.get("tipo"),
            "raw": found,
        }

    payload = {
        "cCodCCInt": build_c_cod_cc_int(client.base_name, desired_name),
        "tipo_conta_corrente": base_cfg.get("target_account_type", "CX"),
        "codigo_banco": base_cfg.get("target_bank_code", "999"),
        "descricao": desired_name,
        "saldo_inicial": float(base_cfg.get("target_account_initial_balance", 0)),
    }
    created = client.post(CONTAS_URL, "IncluirContaCorrente", payload)
    code = created.get("nCodCC") or created.get("codigo") or created.get("codigo_conta_corrente")
    if not code:
        refreshed = find_account_by_name(list_accounts(client), desired_name)
        if not refreshed:
            raise RuntimeError(f"Base={client.base_name} conta corrente provisionada, mas não localizada depois da criação.")
        code = refreshed.get("nCodCC")
        return {
            "created": True,
            "codigo": int(code),
            "descricao": refreshed.get("descricao"),
            "tipo": refreshed.get("tipo_conta_corrente") or refreshed.get("tipo"),
            "raw": refreshed,
        }
    return {
        "created": True,
        "codigo": int(code),
        "descricao": desired_name,
        "tipo": payload["tipo_conta_corrente"],
        "raw": created,
    }



def find_category_by_description(categories: List[Dict[str, Any]], desired_description: str) -> Optional[Dict[str, Any]]:
    desired = normalize(desired_description)
    for item in categories:
        if normalize(item.get("descricao")) == desired:
            return item
    for item in categories:
        if desired in normalize(item.get("descricao")):
            return item
    return None



def ensure_category(client: OmieClient, base_cfg: Dict[str, Any]) -> Dict[str, Any]:
    desired_description = base_cfg["target_category_description"]
    categories = list_categories(client)
    found = find_category_by_description(categories, desired_description)
    if found:
        return {
            "created": False,
            "codigo": found.get("codigo"),
            "descricao": found.get("descricao"),
            "raw": found,
        }

    payload = {
        "categoria_superior": base_cfg.get("target_category_superior", "1.01"),
        "descricao": desired_description,
        "natureza": base_cfg.get(
            "target_category_natureza",
            "Categoria provisionada via API para integração automatizada Manus/Instituto ORBE.",
        ),
    }
    created = client.post(CATEGORIAS_URL, "IncluirCategoria", payload)
    code = created.get("codigo")
    if not code:
        refreshed = find_category_by_description(list_categories(client), desired_description)
        if not refreshed:
            raise RuntimeError(f"Base={client.base_name} categoria provisionada, mas não localizada depois da criação.")
        return {
            "created": True,
            "codigo": refreshed.get("codigo"),
            "descricao": refreshed.get("descricao"),
            "raw": refreshed,
        }
    return {
        "created": True,
        "codigo": code,
        "descricao": desired_description,
        "raw": created,
    }



def build_valid_cnpj() -> str:
    base = [9, 9] + [random.randint(0, 9) for _ in range(6)] + [0, 0, 0, 1]

    def dv(nums: List[int], weights: List[int]) -> int:
        total = sum(n * w for n, w in zip(nums, weights))
        rem = total % 11
        return 0 if rem < 2 else 11 - rem

    d1 = dv(base, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    d2 = dv(base + [d1], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(x) for x in base + [d1, d2])



def upsert_test_client(client: OmieClient, base_cfg: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "cnpj_cpf": build_valid_cnpj(),
        "razao_social": base_cfg.get("test_client_name", f"Cliente Teste Manus {client.base_name}"),
        "nome_fantasia": base_cfg.get("test_client_name", f"Cliente Teste Manus {client.base_name}"),
        "email": base_cfg.get("test_client_email", "omie-teste@institutoorbe.invalid"),
        "observacao": "Registro de teste transitório criado por automação multi-base Manus.",
    }
    return client.post(CLIENTES_URL, "UpsertClienteCpfCnpj", payload)



def build_integration_code(base_name: str) -> str:
    stem = re.sub(r"[^A-Z0-9]", "", base_name.upper())[:6] or "OMIE"
    return f"{stem}{date.today().strftime('%y%m%d')}{random.randint(1000,9999)}"[:20]



def include_receivable(
    client: OmieClient,
    codigo_cliente: int,
    account_code: int,
    category_code: str,
    amount: float,
    integration_code: str,
) -> Dict[str, Any]:
    due_date = (date.today() + timedelta(days=7)).strftime("%d/%m/%Y")
    payload = {
        "codigo_lancamento_integracao": integration_code,
        "codigo_cliente_fornecedor": int(codigo_cliente),
        "data_vencimento": due_date,
        "data_previsao": due_date,
        "valor_documento": float(amount),
        "codigo_categoria": category_code,
        "id_conta_corrente": int(account_code),
        "numero_documento": integration_code,
        "numero_documento_fiscal": integration_code,
        "observacao": "Conta a receber de teste transitório em automação multi-base Manus/Instituto ORBE",
    }
    return client.post(CONTAS_RECEBER_URL, "IncluirContaReceber", payload)



def run_for_base(base_cfg: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    base_name = base_cfg["base_name"]
    app_key = getenv_required(base_cfg["app_key_env"])
    app_secret = getenv_required(base_cfg["app_secret_env"])
    client = OmieClient(base_name=base_name, app_key=app_key, app_secret=app_secret, dry_run=dry_run)

    account_info = ensure_account(client, base_cfg)
    category_info = ensure_category(client, base_cfg)
    client_resp = upsert_test_client(client, base_cfg)
    codigo_cliente = (
        client_resp.get("codigo_cliente_omie")
        or client_resp.get("codigo_cliente")
        or client_resp.get("codigo_cliente_fornecedor")
    )
    if not codigo_cliente:
        raise RuntimeError(f"Base={base_name} não retornou código de cliente na resposta: {client_resp}")
    integration_code = build_integration_code(base_name)
    receivable_resp = include_receivable(
        client=client,
        codigo_cliente=int(codigo_cliente),
        account_code=int(account_info["codigo"]),
        category_code=str(category_info["codigo"]),
        amount=float(base_cfg.get("amount", 1.23)),
        integration_code=integration_code,
    )
    return {
        "base_name": base_name,
        "account": {
            "created": account_info["created"],
            "codigo": account_info["codigo"],
            "descricao": account_info["descricao"],
            "tipo": account_info["tipo"],
        },
        "category": {
            "created": category_info["created"],
            "codigo": category_info["codigo"],
            "descricao": category_info["descricao"],
        },
        "client": {
            "codigo_cliente_omie": codigo_cliente,
            "descricao_status": client_resp.get("descricao_status"),
        },
        "receivable": {
            "codigo_lancamento_omie": receivable_resp.get("codigo_lancamento_omie"),
            "codigo_lancamento_integracao": receivable_resp.get("codigo_lancamento_integracao", integration_code),
            "descricao_status": receivable_resp.get("descricao_status"),
        },
    }



def main() -> None:
    args = parse_args()
    config = load_config(args.config_file)
    bases = config.get("bases", [])
    if not bases:
        raise RuntimeError("O arquivo de configuração deve conter a chave 'bases' com pelo menos uma base Omie.")

    results = []
    for base_cfg in bases:
        time.sleep(float(config.get("sleep_between_bases_seconds", 0.2)))
        results.append(run_for_base(base_cfg, dry_run=args.dry_run))

    json.dump({"results": results}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
