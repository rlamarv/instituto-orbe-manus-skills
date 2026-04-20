import argparse
import json
import os
import random
from datetime import date, timedelta

import requests

CLIENTES_URL = "https://app.omie.com.br/api/v1/geral/clientes/"
CONTAS_URL = "https://app.omie.com.br/api/v1/financas/contareceber/"


def omie_post(url: str, call: str, payload: dict) -> dict:
    body = {
        "call": call,
        "app_key": os.environ["OMIE_APP_KEY"],
        "app_secret": os.environ["OMIE_APP_SECRET"],
        "param": [payload],
    }
    response = requests.post(url, json=body, timeout=60)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        detail = response.text
        raise RuntimeError(f"Erro Omie em {call}: status={response.status_code} body={detail}") from exc
    return response.json()


def build_valid_cnpj() -> str:
    base = [9, 9] + [random.randint(0, 9) for _ in range(6)] + [0, 0, 0, 1]

    def dv(nums, weights):
        total = sum(n * w for n, w in zip(nums, weights))
        rem = total % 11
        return 0 if rem < 2 else 11 - rem

    d1 = dv(base, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    d2 = dv(base + [d1], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(x) for x in base + [d1, d2])



def upsert_test_client(test_name: str) -> dict:
    payload = {
        "cnpj_cpf": build_valid_cnpj(),
        "razao_social": test_name,
        "nome_fantasia": test_name,
        "email": "omie-teste@institutoorbe.invalid",
        "observacao": "Registro de teste transitório criado por Manus para validação de integração.",
    }
    return omie_post(CLIENTES_URL, "UpsertClienteCpfCnpj", payload)



def include_receivable(codigo_cliente: int, integration_code: str, account_code: int, category_code: str, amount: float) -> dict:
    due_date = (date.today() + timedelta(days=7)).strftime("%d/%m/%Y")
    payload = {
        "codigo_lancamento_integracao": integration_code,
        "codigo_cliente_fornecedor": int(codigo_cliente),
        "data_vencimento": due_date,
        "data_previsao": due_date,
        "valor_documento": amount,
        "codigo_categoria": category_code,
        "id_conta_corrente": int(account_code),
        "numero_documento": integration_code,
        "numero_documento_fiscal": integration_code,
        "observacao": "Conta a receber de teste transitório Manus/Instituto ORBE",
    }
    return omie_post(CONTAS_URL, "IncluirContaReceber", payload)



def parse_args():
    parser = argparse.ArgumentParser(description="Executa um smoke test real na Omie sem persistir credenciais.")
    parser.add_argument("--account-code", type=int, required=True, help="Código da conta corrente Omie.")
    parser.add_argument("--category-code", required=True, help="Código da categoria de receita Omie.")
    parser.add_argument("--amount", type=float, default=1.23, help="Valor do título de teste.")
    parser.add_argument("--prefix", default="MANUS-ORBE-TEST", help="Prefixo do código de integração.")
    return parser.parse_args()



def main():
    args = parse_args()
    test_name = f"Cliente Teste Manus ORBE {date.today().isoformat()}"
    integration_code = f"MORBE{date.today().strftime('%y%m%d')}{random.randint(1000, 9999)}"
    client_resp = upsert_test_client(test_name)
    codigo_cliente = client_resp.get("codigo_cliente_omie") or client_resp.get("codigo_cliente") or client_resp.get("codigo_cliente_fornecedor")
    if not codigo_cliente:
        raise RuntimeError(f"Não foi possível obter o código do cliente a partir da resposta: {client_resp}")
    receivable_resp = include_receivable(codigo_cliente, integration_code, args.account_code, args.category_code, args.amount)
    print(json.dumps({
        "test_name": test_name,
        "integration_code": integration_code,
        "account_code": args.account_code,
        "category_code": args.category_code,
        "client_response": client_resp,
        "receivable_response": receivable_resp,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
