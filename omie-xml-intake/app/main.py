import os

from app.omie_uploader import process_xlsx_to_omie
from app.xml_to_xlsx import process_xmls


def run_pipeline():
    xlsx_path = process_xmls(
        input_dir=os.getenv("XML_INPUT_DIR", "input"),
        output_dir=os.getenv("XLSX_OUTPUT_DIR", "output"),
    )
    return process_xlsx_to_omie(xlsx_path)


if __name__ == "__main__":
    run_pipeline()
