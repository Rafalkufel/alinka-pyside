from datetime import date, datetime, time

child_data = {
    "first_name": "Wiktor",
    "last_name": "Rzeźniczak",
    "pesel": "12121244441",
    "birth_date": "2012-12-24",
    "birth_place": "Pachy Wielkie",
    "city": "Poznań",
    "postal_code": "61-854",
    "address": "Mostowa 38",
    "klass": "3b",
    "profession": "murarz",
    "student": True,
}

school_data = {
    "school_type": "Szkoła podstawowa",
    "school_name": "Szkoła Podstawowa nr 4 w Grodzisku Wlkp.",
    "postal_code": "62-222",
    "city": "Grodzisk Wlkp.",
    "address": "ul. Jasna 33",
}

applicants_data = [
    {
        "first_name": "Tomasz",
        "last_name": "Rzeźniczak",
        "city": "Studnia",
        "postal_code": "55-789",
        "address": "Wielka 4/6",
    },
    {
        "first_name": "Adelajda",
        "last_name": "Słoneczko",
        "city": "Sadowisko",
        "postal_code": "15-671",
        "address": "Odnowy Stare, ul. Zamkowa 15/6a",
    },
]

meeting_data = {
    "date": "2019-07-15",
    "time": "16:00",
    "members": [
        {"name": "Antoni Stąsz-Lebieź", "function": "przewodniczący zespołu"},
        {"name": "mgr Leonia Witek-Konuś", "function": "psycholog, tyflopedagog"},
        {"name": "mgr Eleonora Roseveelt", "function": "socjoterapeuta, tyflopedagog"},
    ],
}

support_center_data = {
    "name_nominative": "Poradnia Psychologiczno - Pedagogiczna w Poznaniu",
    "name_genetive": "Poradni Psychologiczno - Pedagogicznej w Poznaniu",
    "institute_name": "Zespół Orzekający przy Poradni Psychologiczno-Pedagogicznej w Poznaniu",
    "city": "Poznań",
    "postal_code": "12-345",
    "address": "ul. Zbąszyńska 11",
    "kurator": "Poznaniu, ul Kościuszki 38, 64-400 Poznań",
}

common_data = {
    "address_child_checkbox": False,
    "addres_first_parent_checkbox": False,
    "issue": "specjalne",
    "period": "nauki w klasach I - III",
    "reasons": ["umiarkowane"],
    "activity_form": "indywidualne",
    "no": "42",
    "child": child_data,
    "school": school_data,
    "applicants": applicants_data,
    "meeting_data": meeting_data,
    "support_center": support_center_data,
    "application_date": "2019-07-01",
}


decision_data = {
    "id": 1,
    "created_at": datetime(2023, 4, 19, 19, 21, 9),
    "modified_at": datetime(2023, 4, 19, 19, 21, 9),
    "child_first_name": "Oliwier",
    "child_last_name": "Gierach",
    "child_address": "ul. Słowianska 10",
    "child_city": "Marki",
    "child_postal_code": "48-315",
    "child_pesel": "21302081908",
    "child_birth_date": date(2020, 3, 5),
    "child_birth_place": "Stargard Szczeciński",
    "child_student": False,
    "klass": "7",
    "profession": "rzeźnik",
    "school_parent_organisation": "Zespół Liceów Medycznych",
    "school_type": "szkoła ponadpodstawowa",
    "school_name": "Technikum Mechaniczne ",
    "school_address": "aleja Fiołkowa 25",
    "school_city": "Grudziądz",
    "school_postal_code": "40-999",
    "address_child_checkbox": False,
    "address_first_parent_checkbox": True,
    "first_parent_first_name": "Emil",
    "first_parent_last_name": "Uroda",
    "first_parent_address": "plac Floriana 83/87",
    "first_parent_city": "Żary",
    "first_parent_postal_code": "14-867",
    "second_parent_first_name": "Mateusz",
    "second_parent_last_name": "Bacia",
    "second_parent_address": "pl. Jarzębinowa 84/32",
    "second_parent_city": "Ostrów Mazowiecka",
    "second_parent_postal_code": "30-602",
    "support_center_name_nominative": "Miejska Poradnia Psychologiczno - Pedagogiczna w Wejherowo",
    "support_center_name_genetive": "Powiatowej Poradni Psychologiczno - Pedagogicznej w Ząbki",
    "support_center_institute_name": "Zespół Orzekający przy Powiatowej Poradni Psychologiczno - Pedagogicznej w Ząbki",
    "support_center_kurator": "Gdańsku, plac Wiśniowa 65/54, 66-804 Bielsko-Biała",
    "support_center_address": "pl. Słoneczna 620",
    "support_center_city": "Żywiec",
    "support_center_postal_code": "82-637",
    "issue": "indywidualne",
    "period": "04/19/2023 - 09/10/2023",
    "reasons": ["znacznie_utrudniajacy"],
    "activity_form": "indywidualne",
    "no": "PPP.2023.AC.224",
    "application_date": date(2023, 4, 5),
    "meeting_date": date(2023, 4, 19),
    "meeting_time": time(8, 15),
    "meeting_members": [
        {"name": "Julian Oleksa", "function": "logopeda, pedagog"},
        {"name": "Natan Kulisz", "function": "tyflopedagog, logopeda"},
        {"name": "Kaja Nesterowicz", "function": "tyflopedagog, psycholog"},
    ],
}
