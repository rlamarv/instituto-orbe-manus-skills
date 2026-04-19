import os
from datetime import datetime
from dotenv import load_dotenv

from app.activesoft_client import listar_alunos, listar_responsaveis, listar_vinculos_aluno_responsavel
from app.logging_utils import get_logger, log_section, log_status
from app.omie_uploader import MIN_INTERVAL_SECONDS, OMIE_CLIENTES_URL, RateLimiter, _omie_request


def _normalize_document(value: str) -> str:
    return "".join(c for c in str(value or "") if c.isdigit())


def _format_caracteristicas(alunos, alunos_map, max_count: int = 11):
    caracteristicas = []
    for idx, aluno in enumerate(alunos[:max_count], start=1):
        aluno_id = aluno.get("id_aluno")
        aluno_full = alunos_map.get(aluno_id, {})
        nome = aluno.get("nome_aluno") or aluno_full.get("nome", "")
        matricula = aluno_full.get("matricula", "")
        caracteristicas.append({"campo": f"Aluno {idx}", "conteudo": " | ".join([v for v in [nome, matricula, str(aluno_id or "")] if v])})
    return caracteristicas


def _build_map(items, key):
    return {item.get(key): item for item in items if item.get(key) is not None}


def _group_vinculos_por_responsavel(vinculos):
    grouped = {}
    for vinculo in vinculos:
        rid = vinculo.get("id_responsavel")
        if rid is not None:
            grouped.setdefault(rid, []).append(vinculo)
    return grouped


def _build_payload(responsavel, alunos_vinculados, alunos_map):
    payload = {
        "cnpj_cpf": _normalize_document(responsavel.get("cpf_cnpj")),
        "razao_social": responsavel.get("nome", ""),
        "nome_fantasia": responsavel.get("nome", ""),
        "email": responsavel.get("email", ""),
        "telefone1_ddd": "",
        "telefone1_numero": "",
        "caracteristicas": _format_caracteristicas(alunos_vinculados, alunos_map),
        "observacao": f"Sincronizado via origem externa em {datetime.now().isoformat(timespec='seconds')}",
    }
    telefone = "".join(c for c in str(responsavel.get("celular", "")).strip() if c.isdigit())
    if len(telefone) >= 10:
        payload["telefone1_ddd"] = telefone[:2]
        payload["telefone1_numero"] = telefone[2:]
    return payload


def process_activesoft_to_omie(prefix: str = "CUSTOMER"):
    load_dotenv()
    logger = get_logger("activesoft_to_omie")
    rate_limiter = RateLimiter(MIN_INTERVAL_SECONDS)
    alunos = listar_alunos()
    responsaveis = listar_responsaveis()
    vinculos = listar_vinculos_aluno_responsavel()
    if isinstance(alunos, dict) and "results" in alunos:
        alunos = alunos["results"]
    if isinstance(responsaveis, dict) and "results" in responsaveis:
        responsaveis = responsaveis["results"]
    if isinstance(vinculos, dict) and "results" in vinculos:
        vinculos = vinculos["results"]
    alunos_map = _build_map(alunos, "id_aluno")
    responsavel_map = _build_map(responsaveis, "id")
    vinculos_por_responsavel = _group_vinculos_por_responsavel(vinculos)
    log_section(logger, "Sincronização ActiveSoft → Omie")
    log_status(logger, "ok", f"Responsáveis vinculados: {len(vinculos_por_responsavel)}")
    results = []
    for rid, alunos_vinculados in vinculos_por_responsavel.items():
        responsavel = responsavel_map.get(rid)
        if not responsavel:
            continue
        payload = _build_payload(responsavel, alunos_vinculados, alunos_map)
        if os.getenv("ACTIVESOFT_PAYLOAD_LOG", "false").lower() == "true":
            logger.warning("Payload logging habilitado apenas para ambiente controlado.")
            logger.info("Payload: %s", payload)
        result = _omie_request(OMIE_CLIENTES_URL, "UpsertClienteCpfCnpj", payload, rate_limiter, prefix)
        results.append(result)
    log_status(logger, "ok", f"Registros enviados: {len(results)}")
    return results
