import argparse
import os

from docx.constants import ActivityForm, DocumentsTypes, Issues, Reasons
from docx.generate_document import Documents
from tests.fixtures import common_data

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINATION_PATH = os.path.join(BASE_PATH, "dokumenty")

GREEN = "\033[32m"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--type",
    "-t",
    dest="document_type",
    default="specjalne",
    help=f"List of issue type. Possible values: {', '.join(Issues._value2member_map_.keys())}. Eg. --type specjalne.",
    type=DocumentsTypes,
)
args = parser.parse_args()

match args.document_type:
    case DocumentsTypes.SPECJALNE:
        document_data = {
            **common_data,
            "period": "pierwszy etap edukacyjny",
            "reason": Reasons.NIESLYSZACE,
            "second_reason": Reasons.LEKKIE,
        }
    case DocumentsTypes.INDYWIDUALNE:
        document_data = {
            **common_data,
            "period": "styczeń 2018 - listopad 2019",
            "reason": Reasons.ZNACZNIE_UTRUDNIAJACY,
        }
    case DocumentsTypes.INDYWIDUALNE_ROCZNE:
        document_data = {**common_data, "period": "styczeń 2018 - listopad 2019", "reason": Reasons.UNIEMOZLIWIAJACY}
    case DocumentsTypes.REWALIDACYJNE:
        document_data = {**common_data, "period": "5-ciu lat.", "activity_form": ActivityForm.INDYWIDUALNE}
    case DocumentsTypes.OPINIA:
        document_data = {**common_data, "period": "do rozpoczęcia spełniania obowiązku szkolnego"}
    case _:
        raise Exception("Invalid document type.")

Documents(
    documents=[args.document_type, DocumentsTypes.ZARZADZANIE, DocumentsTypes.ZAWIADOMIENIE, DocumentsTypes.PROTOKOL],
    document_data=document_data,
    destination_path=DESTINATION_PATH,
).create()
print(f"{GREEN}Dokumenty zostały utworzone.")
