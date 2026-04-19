import os
import requests
from dotenv import load_dotenv

DEFAULT_BASE_URL = os.getenv("ACTIVE_SOFT_BASE_URL", "https://example.invalid")
API_VERSION = os.getenv("ACTIVE_SOFT_API_VERSION", "v0")


def _load_env() -> None:
    if os.path.exists(".env"):
        load_dotenv(dotenv_path=".env")
    else:
        load_dotenv()


def _get_headers() -> dict:
    _load_env()
    token = os.getenv("ACTIVE_SOFT_CUSTOMER", "")
    if not token:
        raise ValueError("Missing ACTIVE_SOFT_CUSTOMER in environment.")
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }


def _get(path: str):
    response = requests.get(f"{DEFAULT_BASE_URL}{path}", headers=_get_headers(), timeout=30)
    response.raise_for_status()
    return response.json()


def listar_alunos():
    return _get(f"/api/{API_VERSION}/acesso/alunos/")


def listar_enturmacao():
    return _get(f"/api/{API_VERSION}/acesso/enturmacao/")


def listar_vinculos_aluno_responsavel():
    return _get(f"/api/{API_VERSION}/acesso/vinculo_aluno_responsavel_liberado/")


def listar_responsaveis():
    return _get(f"/api/{API_VERSION}/lista_responsaveis/")
