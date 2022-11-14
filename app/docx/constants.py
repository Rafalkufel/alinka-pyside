from enum import Enum


class Reasons(Enum):
    NIESLYSZACE = "niesłyszące"
    SLABOSLYSZACE = "słabosłyszące"
    NIEWIDZACE = "niewidzące"
    SLABOWIDZACE = "słabowidzące"
    RUCHOWA = "ruchowa"
    LEKKIE = "lekkie"
    UMIARKOWANE = "umiarkowane"
    ZNACZNE = "znaczne"
    AUTYZM = "autyzm"
    SPRZEZONA = "sprzezona"
    NIEDOSTOSOWANIE = "niedostosowanie"
    ZAGROZENIE_NIEDOSTOSOWANIEM = "zagrożenie_niedostosowaniem"
    UNIEMOZLIWIAJACY = "uniemozliwiajacy"
    ZNACZNIE_UTRUDNIAJACY = "znacznie_utrudniajacy"


class Issues(Enum):
    SPECJALNE = "specjalne"
    INDYWIDUALNE = "indywidualne"
    INDYWIDUALNE_ROCZNE = "indywidualne_roczne"
    OPINIA = "opinia"
    REWALIDACYJNE = "rewalidacyjne"


class DocumentsTypes(Enum):
    SPECJALNE = "specjalne"
    INDYWIDUALNE = "indywidualne"
    INDYWIDUALNE_ROCZNE = "indywidualne_roczne"
    OPINIA = "opinia"
    REWALIDACYJNE = "rewalidacyjne"
    PROTOKOL = "protokol"
    ZARZADZANIE = "zarzadzenie"
    ZAWIADOMIENIE = "zawiadomienie"


class ActivityForm(Enum):
    INDYWIDUALNE = "indywidualne"
    GRUPOWE = "grupowe"
