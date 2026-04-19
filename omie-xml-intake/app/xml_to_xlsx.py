import glob
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from openpyxl import Workbook


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def _find_child_by_tag(elem, tag_name):
    for child in list(elem):
        if _strip_ns(child.tag) == tag_name:
            return child
    return None


def _find_path(elem, path):
    current = elem
    for tag_name in path:
        if current is None:
            return None
        current = _find_child_by_tag(current, tag_name)
    return current


def _find_text(elem, path):
    node = _find_path(elem, path)
    return "" if node is None else (node.text or "").strip()


def _flatten_element(elem, prefix, out, skip_tags=None):
    tag = _strip_ns(elem.tag)
    if skip_tags and tag in skip_tags:
        return
    key_prefix = f"{prefix}{tag}"
    for attr_name, attr_val in elem.attrib.items():
        out[f"{key_prefix}.@{attr_name}"] = attr_val
    children = list(elem)
    if children:
        for child in children:
            _flatten_element(child, f"{key_prefix}.", out, skip_tags=skip_tags)
    else:
        text = (elem.text or "").strip()
        if text:
            out[key_prefix] = text


def _extract_rows_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    base_fields = {}
    _flatten_element(root, "", base_fields, skip_tags={"det"})
    det_elements = [e for e in root.iter() if _strip_ns(e.tag) == "det"]
    if not det_elements:
        return [base_fields]
    rows = []
    for det in det_elements:
        det_fields = {}
        _flatten_element(det, "", det_fields)
        row = dict(base_fields)
        row.update(det_fields)
        rows.append(row)
    return rows


def _extract_summary_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    inf = _find_path(root, ["NFCom", "infNFCom"])
    emit = _find_path(inf, ["emit"]) if inf is not None else None
    dest = _find_path(inf, ["dest"]) if inf is not None else None
    ide = _find_path(inf, ["ide"]) if inf is not None else None
    total = _find_path(inf, ["total"]) if inf is not None else None
    gfat = _find_path(inf, ["gFat"]) if inf is not None else None
    ender_dest = _find_path(dest, ["enderDest"]) if dest is not None else None
    return {
        "nfcom_id": inf.attrib.get("Id", "") if inf is not None else "",
        "numero_nf": _find_text(ide, ["nNF"]),
        "data_emissao": _find_text(ide, ["dhEmi"]),
        "emitente_cnpj": _find_text(emit, ["CNPJ"]),
        "emitente_nome": _find_text(emit, ["xNome"]),
        "destinatario_cnpj": _find_text(dest, ["CNPJ"]),
        "destinatario_nome": _find_text(dest, ["xNome"]),
        "destinatario_xLgr": _find_text(ender_dest, ["xLgr"]),
        "destinatario_nro": _find_text(ender_dest, ["nro"]),
        "destinatario_xCpl": _find_text(ender_dest, ["xCpl"]),
        "destinatario_xBairro": _find_text(ender_dest, ["xBairro"]),
        "destinatario_cMun": _find_text(ender_dest, ["cMun"]),
        "destinatario_xMun": _find_text(ender_dest, ["xMun"]),
        "destinatario_CEP": _find_text(ender_dest, ["CEP"]),
        "destinatario_UF": _find_text(ender_dest, ["UF"]),
        "valor_total_nf": _find_text(total, ["vNF"]),
        "competencia": _find_text(gfat, ["CompetFat"]),
        "vencimento": _find_text(gfat, ["dVencFat"]),
    }


def process_xmls(input_dir=None, output_dir=None):
    input_dir = input_dir or os.getenv("XML_INPUT_DIR", "input")
    output_dir = output_dir or os.getenv("XLSX_OUTPUT_DIR", "output")
    xml_files = sorted(glob.glob(os.path.join(input_dir, "**", "*.xml"), recursive=True))
    if not xml_files:
        raise FileNotFoundError(f"Nenhum XML encontrado em {input_dir}")
    detalhe_rows = []
    resumo_rows = []
    for xml_path in xml_files:
        detalhe_rows.extend(_extract_rows_from_xml(xml_path))
        resumo_rows.append(_extract_summary_from_xml(xml_path))
    detalhe_columns = sorted({key for row in detalhe_rows for key in row.keys()})
    resumo_columns = [
        "nfcom_id", "numero_nf", "data_emissao", "emitente_cnpj", "emitente_nome",
        "destinatario_cnpj", "destinatario_nome", "destinatario_xLgr", "destinatario_nro",
        "destinatario_xCpl", "destinatario_xBairro", "destinatario_cMun", "destinatario_xMun",
        "destinatario_CEP", "destinatario_UF", "valor_total_nf", "competencia", "vencimento",
    ]
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"contas_a_receber_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    wb = Workbook()
    ws_resumo = wb.active
    ws_resumo.title = "contas_a_receber"
    ws_resumo.append(resumo_columns)
    for row in resumo_rows:
        ws_resumo.append([row.get(col, "") for col in resumo_columns])
    ws_detalhe = wb.create_sheet("detalhes_xml")
    ws_detalhe.append(detalhe_columns)
    for row in detalhe_rows:
        ws_detalhe.append([row.get(col, "") for col in detalhe_columns])
    wb.save(output_path)
    return output_path


if __name__ == "__main__":
    print(process_xmls())
