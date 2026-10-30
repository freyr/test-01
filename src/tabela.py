"""Projekt tabeli z zadania 8. Te same dane posłużą w zadaniu 9 do tabeli HTML."""

TYTUL = "Cennik laptopów - Doe John 2Fg1"
ZRODLO = "Źródło: własne (ceny przykładowe)"

# Krój, rozmiar w punktach, kolor, wyrównanie i pogrubienie każdej kolumny.
KOLUMNY = [
    ("Producent", "Arial", 12, "1F3A93", "center", True),
    ("Model", "Arial", 11, "1E7B34", "left", False),
    ("Procesor", "Times New Roman", 11, "333333", "left", False),
    ("Pamięć RAM", "Times New Roman", 11, "333333", "center", False),
    ("Dysk SSD", "Times New Roman", 11, "333333", "center", False),
    ("Cena", "Arial", 12, "8B1A1A", "right", True),
]

NAGLOWEK_TLO = "1F4E79"
NAGLOWEK_KOLOR = "FFFFFF"

# Komórka: tekst albo (tekst, colspan, rowspan). None = miejsce zajęte przez komórkę scaloną.
WIERSZE = [
    ("DDEBF7", [("Lenovo", 1, 2), "IdeaPad Slim 5", "Ryzen 5 7530U", "16 GB", "512 GB", "2 899 zł"]),
    ("DDEBF7", [None, "ThinkPad E14", "Core i5-1335U", "16 GB", "512 GB", "3 699 zł"]),
    ("FFF2CC", [("Dell", 1, 2), "Inspiron 15", "Core i5-1334U", "8 GB", "512 GB", "2 599 zł"]),
    ("FFF2CC", [None, "Latitude 5440", "Core i7-1355U", "16 GB", "1 TB", "5 199 zł"]),
    ("E2EFDA", ["HP", "Pavilion 15", "Ryzen 7 7730U", "16 GB", "1 TB", "3 299 zł"]),
    ("FCE4EC", ["Asus", "Vivobook 16", "Core i3-1315U", "8 GB", "256 GB", "1 999 zł"]),
    ("F8CBAD", ["Apple", "MacBook Air 13", ("Apple M2, 8 GB RAM, 256 GB SSD", 3, 1), None, None, "4 499 zł"]),
]

RAMKA_KOLOR = "2E75B6"
RAMKA_WEWN_PT = 0.75
RAMKA_ZEWN_PT = RAMKA_WEWN_PT * 4


def komorki():
    """Zwraca (wiersz, kolumna, tekst, colspan, rowspan) dla każdej widocznej komórki."""
    for w, (_, wiersz) in enumerate(WIERSZE):
        for k, komorka in enumerate(wiersz):
            if komorka is None:
                continue
            if isinstance(komorka, str):
                komorka = (komorka, 1, 1)
            yield (w, k) + komorka


def liczba_komorek():
    return len(KOLUMNY) + sum(1 for _ in komorki())
