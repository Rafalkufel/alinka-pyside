import argparse
import os

from docx.constants import ActivityForm, DocumentsTypes, Issue, Reason
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
    help=f"List of issue type. Possible values: {', '.join(Issue._value2member_map_.keys())}. Eg. --type specjalne.",
    type=DocumentsTypes,
)
args = parser.parse_args()
match args.document_type:
    case DocumentsTypes.SPECJALNE:
        document_data = {
            **common_data,
            "issue": Issue.SPECJALNE,
            "period": "pierwszy etap edukacyjny",
            "reasons": [Reason.NIESLYSZACE, Reason.LEKKIE],
        }
    case DocumentsTypes.INDYWIDUALNE:
        document_data = {
            **common_data,
            "issue": Issue.INDYWIDUALNE,
            "period": "styczeń 2018 - listopad 2019",
            "reasons": [Reason.ZNACZNIE_UTRUDNIAJACY],
        }
    case DocumentsTypes.INDYWIDUALNE_ROCZNE:
        document_data = {
            **common_data,
            "issue": Issue.INDYWIDUALNE_ROCZNE,
            "period": "styczeń 2018 - listopad 2019",
            "reasons": [Reason.UNIEMOZLIWIAJACY],
        }
    case DocumentsTypes.REWALIDACYJNE:
        document_data = {
            **common_data,
            "issue": Issue.REWALIDACYJNE,
            "period": "5-ciu lat.",
            "activity_form": ActivityForm.INDYWIDUALNE,
        }
    case DocumentsTypes.OPINIA:
        document_data = {
            **common_data,
            "issue": Issue.OPINIA,
            "period": "do rozpoczęcia spełniania obowiązku szkolnego",
        }
    case _:
        raise Exception("Invalid document type.")

Documents(
    documents=[args.document_type, DocumentsTypes.ZARZADZANIE, DocumentsTypes.ZAWIADOMIENIE, DocumentsTypes.PROTOKOL],
    document_data=document_data,
    destination_path=DESTINATION_PATH,
).create()
print(f"{GREEN}Dokumenty zostały utworzone.")
