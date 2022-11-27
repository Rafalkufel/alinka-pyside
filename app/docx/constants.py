from enum import Enum


class Reason(str, Enum):
    NIESLYSZACE = "nieslyszace"
    SLABOSLYSZACE = "slaboslyszace"
    NIEWIDZACE = "niewidzące"
    SLABOWIDZACE = "slabowidzace"
    RUCHOWA = "ruchowa"
    LEKKIE = "lekkie"
    UMIARKOWANE = "umiarkowane"
    ZNACZNE = "znaczne"
    GLEBOKIE = "glebokie"
    AUTYZM = "autyzm"
    SPRZEZONA = "sprzezona"
    NIEDOSTOSOWANIE = "niedostosowanie"
    ZAGROZENIE_NIEDOSTOSOWANIEM = "zagrozenie_niedostosowaniem"
    UNIEMOZLIWIAJACY = "uniemozliwiajacy"
    ZNACZNIE_UTRUDNIAJACY = "znacznie_utrudniajacy"

    @classmethod
    def individual_reasons(cls):
        return [cls.UNIEMOZLIWIAJACY.value, cls.ZNACZNIE_UTRUDNIAJACY.value]

    @classmethod
    def intelectual_reasons(cls):
        return [cls.LEKKIE.value, cls.UMIARKOWANE.value, cls.ZNACZNE.value]

    @classmethod
    def perception_deficites_reasons(cls):
        return [cls.NIESLYSZACE.value, cls.SLABOSLYSZACE.value, cls.NIEWIDZACE.value, cls.SLABOWIDZACE.value]

    @classmethod
    def social_maladjustment_reasons(cls):
        return [cls.NIEDOSTOSOWANIE.value, cls.ZAGROZENIE_NIEDOSTOSOWANIEM.value]

    @classmethod
    def special_reasons(cls):
        return [
            *cls.intelectual_reasons() * cls.perception_deficites_reasons(),
            *cls.social_maladjustment_reasons(),
            cls.RUCHOWA.value,
            cls.AUTYZM.value,
        ]

    @classmethod
    def multiple_disability_reasons(cls):
        return [*cls.intelectual_reasons(), *cls.perception_deficites_reasons(), cls.RUCHOWA, cls.AUTYZM]

    @property
    def reason_description_nominative_short(self):
        mapper = {
            self.LEKKIE: "niepełnosprawność",
            self.UMIARKOWANE: "niepełnosprawność",
            self.ZNACZNE: "niepełnosprawność",
            self.NIESLYSZACE: "niesłyszenie",
            self.SLABOSLYSZACE: "słabosłyszenie",
            self.NIEWIDZACE: "niewidzenie",
            self.SLABOWIDZACE: "słabowididzenie",
            self.RUCHOWA: "niepełnosprawność ruchowa",
            self.GLEBOKIE: "niepełnosprawność",
            self.AUTYZM: "autyzm",
            self.SPRZEZONA: "niepełnosprawność sprzężona",
            self.NIEDOSTOSOWANIE: "niedostosowanie społeczne",
            self.ZAGROZENIE_NIEDOSTOSOWANIEM: "zagrożenie niedostosowaniem społecznym",
            self.UNIEMOZLIWIAJACY: "stan zdrowia",
            self.ZNACZNIE_UTRUDNIAJACY: "stan zdrowia",
        }
        return mapper[self]

    @property
    def reason_description_genetive_short(self):
        mapper = {
            self.LEKKIE: "niepełnosprawności",
            self.UMIARKOWANE: "niepełnosprawności",
            self.ZNACZNE: "niepełnosprawności",
            self.NIESLYSZACE: "niesłyszenia",
            self.SLABOSLYSZACE: "słabosłyszenia",
            self.NIEWIDZACE: "niewidzenia",
            self.SLABOWIDZACE: "słabowididzenia",
            self.RUCHOWA: "niepełnosprawności ruchowej",
            self.GLEBOKIE: "niepełnosprawności",
            self.AUTYZM: "autyzmu",
            self.SPRZEZONA: "niepełnosprawności",
            self.NIEDOSTOSOWANIE: "niedostosowania społecznego",
            self.ZAGROZENIE_NIEDOSTOSOWANIEM: "zagrożenia niedostosowaniem społecznym",
            self.UNIEMOZLIWIAJACY: "stanu zdrowia",
            self.ZNACZNIE_UTRUDNIAJACY: "stanu zdrowia",
        }
        return mapper[self]

    @property
    def reason_description_nominative_long(self):
        mapper = {
            self.LEKKIE: "niepełnosprawność intelektualna w stopniu lekkim",
            self.UMIARKOWANE: "niepełnosprawność intelektualna w stopniu umiarkowanym",
            self.ZNACZNE: "niepełnosprawnosć intelektualna w stopniu znacznym",
            self.NIESLYSZACE: "niesłyszenie",
            self.SLABOSLYSZACE: "słabosłyszenie",
            self.NIEWIDZACE: "niewidzenie",
            self.SLABOWIDZACE: "słabowididzenie",
            self.RUCHOWA: "niepełnosprawność ruchowa",
            self.GLEBOKIE: "niepełnosprawność intelektualna w stopniu głębokim",
            self.AUTYZM: "autyzm",
            self.SPRZEZONA: "niepełnosprawność sprzężona",
            self.NIEDOSTOSOWANIE: "niedostosowanie społeczne",
            self.ZAGROZENIE_NIEDOSTOSOWANIEM: "zagrożenie niedostosowaniem społecznym",
            self.UNIEMOZLIWIAJACY: "stan zdrowia uniemożliwiający uczęszczanie do szkoły",
            self.ZNACZNIE_UTRUDNIAJACY: "stan zdrowia znacznie utrudniający uczęszczanie do szkoły",
        }
        return mapper[self]

    @property
    def reason_description_genetive_long(self):
        mapper = {
            self.LEKKIE: "niepełnosprawności intelektualnej w stopniu lekkim",
            self.UMIARKOWANE: "niepełnosprawności intelektualnej w stopniu umiarkowanym",
            self.ZNACZNE: "niepełnosprawności intelektualnej w stopniu znacznym",
            self.NIESLYSZACE: "niesłyszenia",
            self.SLABOSLYSZACE: "słabosłyszenia",
            self.NIEWIDZACE: "niewidzenia",
            self.SLABOWIDZACE: "słabowididzenia",
            self.RUCHOWA: "niepełnosprawności ruchowej",
            self.GLEBOKIE: "niepełnosprawności intelektualnej w stopniu głębokim",
            self.AUTYZM: "autyzmu",
            self.SPRZEZONA: "niepełnosprawności sprzężonej",
            self.NIEDOSTOSOWANIE: "niedostosowania społecznego",
            self.ZAGROZENIE_NIEDOSTOSOWANIEM: "zagrożenia niedostosowaniem społecznym",
            self.UNIEMOZLIWIAJACY: "stanu zdrowia uniemozliwiajacego uczęszczanie do szkoły",
            self.ZNACZNIE_UTRUDNIAJACY: "stanu zdrowia znacznie utrudniajacego uczęszczanie do szkoły",
        }
        return mapper[self]

    @property
    def reason_description_accusative_long(self):
        mapper = {
            self.LEKKIE: "niepełnosprawność intelektualną w stopniu lekkim",
            self.UMIARKOWANE: "niepełnosprawność intelektualną w stopniu umiarkowanym",
            self.ZNACZNE: "niepełnosprawność intelektualną w stopniu znacznym",
            self.NIESLYSZACE: "niesłyszenie",
            self.SLABOSLYSZACE: "słabosłyszenie",
            self.NIEWIDZACE: "niewidzenie",
            self.SLABOWIDZACE: "słabowididzenie",
            self.RUCHOWA: "niepełnosprawność ruchową",
            self.GLEBOKIE: "niepełnosprawność intelektualną w stopniu głębokim",
            self.AUTYZM: "autyzm",
            self.SPRZEZONA: "niepełnosprawność sprzężoną",
            self.NIEDOSTOSOWANIE: "niedostosowanie społeczne",
            self.ZAGROZENIE_NIEDOSTOSOWANIEM: "zagrożenie niedostosowaniem społecznym",
            self.UNIEMOZLIWIAJACY: "stan zdrowia uniemozliwiajacy uczęszczanie do szkoły",
            self.ZNACZNIE_UTRUDNIAJACY: "stan zdrowia znacznie utrudniajacy uczęszczanie do szkoły",
        }
        return mapper[self]


class Issue(Enum):
    SPECJALNE = "specjalne"
    INDYWIDUALNE = "indywidualne"
    INDYWIDUALNE_ROCZNE = "indywidualne_roczne"
    OPINIA = "opinia"
    REWALIDACYJNE = "rewalidacyjne"

    @property
    def issue_description_nominative(self):
        mapper = {
            self.SPECJALNE: "kształcenie specjalne",
            self.INDYWIDUALNE: "indywidualne nauczanie",
            self.INDYWIDUALNE_ROCZNE: "indywidualne roczne przygotowanie przedszkolne",
            self.OPINIA: "wczesnege wspomaganie rozwoju",
            self.REWALIDACYJNE: "zajęcia rewalidacyjno - wychowawcze",
        }
        return mapper[self]

    @property
    def issue_description_genetive(self):
        mapper = {
            self.SPECJALNE: "kształcenia specjalnego",
            self.INDYWIDUALNE: "indywidualnego nauczania",
            self.INDYWIDUALNE_ROCZNE: "indywidualnego rocznego przygotowania przedszkolnego",
            self.OPINIA: "wczesnego wspomagania rozwoju",
            self.REWALIDACYJNE: "zajęć rewalidacyjno - wychowawczych",
        }
        return mapper[self]

    @property
    def issue_type_nominative_short(self):
        if self == self.OPINIA:
            return "opinia"
        else:
            return "orzeczenie"

    @property
    def issue_type_genetive_short(self):
        if self == self.OPINIA:
            return "opinii"
        else:
            return "orzeczenia"

    @property
    def issue_type_nominative_long(self):
        return f"{self.issue_type_nominative_short} o potrzebie {self.issue_description_genetive}"

    @property
    def issue_type_genetive_long(self):
        return f"{self.issue_type_genetive_short} o potrzebie {self.issue_description_genetive}"


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
    ZESPOLOWE = "zespolowe"
