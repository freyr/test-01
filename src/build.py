"""Buduje docs/: osobny folder strony dla każdego zadania oraz strony z wyjaśnieniami.

Uruchom z katalogu repozytorium: python3 src/build.py
"""
import difflib
import html
import json
import re
import shutil
from pathlib import Path

import tabela_html
from popraw_html import popraw

SRC = Path(__file__).parent
DOCS = SRC.parent / "docs"
ZASOBY = SRC / "zasoby"

ZADANIA = {
    1: ("Pierwsza strona i publikacja na GitHub", "Imię 7 razy, nazwisko w nagłówkach H6-H1, emotikony. Strona trafia na GitHub Pages."),
    2: ("Akapity i formatowanie tekstu", "Dane ucznia, akapity z wyrównaniem, pogrubienie, kursywa, indeksy."),
    3: ("Dowcipy w ramkach, meta i tło", "Fieldset z legendą, nagłówki, komentarz, meta, tło, linie, znaki specjalne."),
    4: ("Wyliczenia i numerowania", "Listy ul i ol, różne znaki i numeracje, lista zagnieżdżona."),
    5: ("Animowane grafiki", "Pięć obrazków przy dowcipach z wyrównaniem, ramką, wymiarami i tekstem alt."),
    6: ("Linki i podstrony", "Menu na górze, w środku i na dole, kotwice, cztery podstrony."),
    7: ("Walidacja i poprawa kodu", "Sprawdzenie w validator.w3.org, zamiana starych znaczników na CSS."),
    8: ("Projekt tabeli w Word", "Projekt tabeli z co najmniej 30 komórkami, scaleniami, kolorami i ramką. Plik .docx, nie HTML."),
    9: ("Tabela w HTML", "Tabela z projektu na stronie tabela_doe.html: szkielet, style CSS, scalanie komórek."),
    10: ("Projekt formularza na kartce", "Rysunek formularza ołówkiem na kartce A4: pola tekstowe, listy, radio, checkbox, przyciski."),
    11: ("Formularz w HTML", "Formularz z projektu na stronie formularz_doe.html, zbudowany w 8 etapach."),
}
OSTATNIE = max(ZADANIA)


ETAPY_FORMULARZA = [
    ("Formularz i tabela", "Znaczniki <code>&lt;form&gt;</code> i <code>&lt;table&gt;</code>. Tabela rozkłada pola równo na stronie. Szerokość i wysokość komórek są zaplanowane od razu, w komórkach są na razie napisy zastępcze."),
    ("Wysyłanie formularza", "<code>action=\"mailto:…?subject=Doe\"</code> wysyła dane e-mailem, temat to nazwisko. Wpisz adres nauczyciela z instrukcji."),
    ("Tło, tytuł i pola tekstowe", "Tło w kodzie szesnastkowym, duży tytuł i pięć pól <code>&lt;input&gt;</code>: puste, z tekstem (<code>value</code>), z limitem (<code>maxlength</code>), hasło (<code>type=\"password\"</code>) i drugie puste. Etykiety mają stałą szerokość, więc pola stoją w jednej linii pionowej."),
    ("Listy rozwijalne", "Trzy <code>&lt;select&gt;</code>: 5 opcji z domyślną, 4 opcje bez domyślnej, 3 opcje z domyślną. Opcję domyślną ustawia <code>selected</code>."),
    ("Pola wyboru checkbox", "Trzy grupy <code>type=\"checkbox\"</code>: 4 pionowo, 3 pionowo, 5 poziomo z jednym zaznaczonym (<code>checked</code>). Pionowo, gdy po każdym polu jest <code>&lt;br&gt;</code>."),
    ("Przyciski opcji radio", "Trzy grupy <code>type=\"radio\"</code>: 3 pionowo, 4 poziomo z jedną zaznaczoną, 5 poziomo. Przyciski z tym samym <code>name</code> tworzą grupę: można wybrać tylko jeden."),
    ("Pola HTML5 i textarea", "Data, godzina, kolor, suwak (<code>range</code>) i pasek postępu (<code>&lt;progress&gt;</code>). Pod spodem duże pole <code>&lt;textarea&gt;</code> na dłuższy tekst."),
    ("Przyciski", "Dwa <code>&lt;button&gt;</code> z akcją <code>onclick</code>, <code>reset</code> z napisem CZYŚĆ i <code>submit</code> z napisem WYŚLIJ."),
]


def renderuj(nr, szablon="strona.tpl.html"):
    """Zwraca kod pliku po zadaniu (albo etapie) nr: linie @a| i @a-b| z szablonu."""
    wynik = []
    for linia in (SRC / szablon).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^@(\d+)(?:-(\d+))?\|(.*)$", linia)
        if not m:
            wynik.append(linia)
            continue
        od, do = int(m[1]), int(m[2] or 99)
        if od <= nr <= do:
            wynik.append(m[3])
    kod = "\n".join(wynik) + "\n"
    return popraw(kod) if nr >= 7 and szablon == "strona.tpl.html" else kod


def etapy(nr):
    """Zadania 9 i 11 mają etapy: (plik, [(tytuł, opis, kod), ...])."""
    if nr == 9:
        return "tabela_doe.html", [(t, o, tabela_html.strona(e)) for e, (t, o) in enumerate(tabela_html.ETAPY, 1)]
    if nr == 11:
        return "formularz_doe.html", [(t, o, renderuj(e, "formularz.tpl.html")) for e, (t, o) in enumerate(ETAPY_FORMULARZA, 1)]
    return None


def podstrony(nr):
    pliki = {}
    if nr < 6:
        return pliki
    for plik in sorted((SRC / "podstrony").glob("*.html")):
        if plik.name == "walidacja_doe.html" and nr < 7:
            continue
        kod = plik.read_text(encoding="utf-8")
        if plik.name == "walidacja_doe.html":
            wynik = json.loads((ZASOBY / "walidacja_wynik.json").read_text())
            kod = kod.replace("{BLEDY}", str(wynik["bledy"])).replace("{OSTRZEZENIA}", str(wynik["ostrzezenia"]))
        pliki[plik.name] = popraw(kod) if nr >= 7 else kod
    for n in (9, 11):
        if nr >= n:
            plik, lista = etapy(n)
            pliki[plik] = lista[-1][2]
    return pliki


def zasoby(nr):
    nazwy = []
    if nr >= 5:
        nazwy += [f"grafika{i}.gif" for i in range(1, 6)]
    if nr >= 6:
        nazwy += ["poczta.gif", "plik_doe.zip"]
    if nr >= 7:
        nazwy += ["blad_poczatek_doe.jpg", "blad_koniec_doe.jpg", "html5_ok.png"]
    if nr >= 8:
        nazwy += ["doe_2F_g1.docx"]
    if nr >= 10:
        nazwy += ["projekt_formularza_doe.png"]
    return nazwy


def diff_html(stary, nowy):
    wiersze = []
    for linia in difflib.unified_diff(stary.splitlines(), nowy.splitlines(), lineterm="", n=2):
        if linia.startswith(("---", "+++")):
            continue
        if linia.startswith("@@"):
            m = re.search(r"\+(\d+)", linia)
            wiersze.append(f'<span class="d-hunk">… od linii {m[1]} …</span>')
            continue
        klasa = {"+": "d-add", "-": "d-del"}.get(linia[:1], "d-ctx")
        wiersze.append(f'<span class="{klasa}">{html.escape(linia) or "&nbsp;"}</span>')
    return '<pre class="diff">' + "".join(wiersze) + "</pre>"


def nawigacja(nr):
    lewa = f'<a href="zadanie{nr - 1}.html">← Zadanie {nr - 1}</a>' if nr > 1 else "<span></span>"
    prawa = f'<a href="zadanie{nr + 1}.html">Zadanie {nr + 1} →</a>' if nr < OSTATNIE else "<span></span>"
    return f'<nav class="nav">{lewa}<a href="../index.html">Wszystkie zadania</a>{prawa}</nav>'


def sekcja_etapow(nr, plik, lista, poprzedni_plik):
    czesci = [f"<h2>Etapy budowy pliku {plik}</h2>",
              f"<p>Każdy etap pokazuje zmiany względem poprzedniego. Etap 1 porównuje plik z wersją z zadania {nr - 1}.</p>"]
    stary = poprzedni_plik
    for e, (tytul, opis, kod) in enumerate(lista, 1):
        czesci.append(f"<h3>Etap {e}: {tytul}</h3><p>{opis}</p>")
        czesci.append(f'<p><a href="etapy/zadanie{nr}_etap{e}.html">Otwórz stronę po etapie {e} ↗</a></p>')
        czesci.append(diff_html(stary, kod))
        stary = kod
    return "\n".join(czesci)


def strona_opisu(nr, kod, poprzedni, nowe_pliki, etapy_html="", glowny="index.html", kod_glowny=None):
    tytul, _ = ZADANIA[nr]
    opis = (SRC / "opisy" / f"zadanie{nr}.html").read_text(encoding="utf-8")
    if poprzedni is None:
        zmiany = "<p>To pierwsze zadanie, więc cały kod jest nowy. Zobacz pełny kod poniżej.</p>"
    elif poprzedni == kod:
        zmiany = f"<p>Plik <code>index.html</code> jest taki sam jak po zadaniu {nr - 1}.</p>"
    else:
        zmiany = (
            f"<p>Porównanie <code>index.html</code> z zadaniem {nr - 1}. "
            '<span class="d-add-t">Zielone linie (+)</span> są dodane, '
            '<span class="d-del-t">czerwone linie (−)</span> są usunięte lub zmienione.</p>'
            + diff_html(poprzedni, kod)
        )
    if nowe_pliki:
        zmiany += "<h3>Nowe pliki w folderze</h3><ul>" + "".join(f"<li><code>{p}</code></li>" for p in nowe_pliki) + "</ul>"
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zadanie {nr} - wyjaśnienie</title>
<link rel="stylesheet" href="styl.css">
</head>
<body>
<main>
{nawigacja(nr)}
<p class="eyebrow">Zadanie {nr} z {OSTATNIE}</p>
<h1>{tytul}</h1>
<p><a class="btn" href="../zadanie{nr}/{glowny}">Otwórz stronę po zadaniu {nr} ↗</a></p>
{opis}
<h2>Co się zmieniło w kodzie</h2>
{zmiany}
{etapy_html}
<h2>Pełny kod {glowny} po zadaniu {nr}</h2>
<details><summary>Pokaż kod</summary><pre class="code">{html.escape(kod_glowny or kod)}</pre></details>
{nawigacja(nr)}
</main>
</body>
</html>
"""


def strona_glowna():
    karty = "".join(
        f"""<li class="card"><span class="num">{nr}</span><div><h2>{t}</h2><p>{o}</p>
<p class="links"><a href="opis/zadanie{nr}.html">Wyjaśnienie i zmiany</a> · <a href="zadanie{nr}/index.html">Strona po zadaniu</a></p></div></li>"""
        for nr, (t, o) in ZADANIA.items()
    )
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zadania HTML 1-{OSTATNIE}</title>
<link rel="stylesheet" href="opis/styl.css">
</head>
<body>
<main>
<p class="eyebrow">Instrukcja HTML, ZSE Gdańsk · przykładowy uczeń: John Doe, nr 7, ur. 14 marca 2009</p>
<h1>Zadania HTML 1-{OSTATNIE} krok po kroku</h1>
<p>Każde zadanie rozbudowuje stronę z poprzedniego zadania. Dla każdego zadania są dwie rzeczy:</p>
<ul>
<li><b>Wyjaśnienie i zmiany</b>: co zadanie wymaga, jak to zrobiono i które linie kodu doszły.</li>
<li><b>Strona po zadaniu</b>: gotowa strona, tak jak wygląda po tym kroku.</li>
</ul>
<p>Dane ucznia są fałszywe. Wpisz swoje dane i swój numer z dziennika: od niego zależą wielkości i kolejność.</p>
<ol class="cards">{karty}</ol>
</main>
</body>
</html>
"""


def main():
    for stary in ["index.html", "opis"] + [f"zadanie{i}" for i in ZADANIA]:
        sciezka = DOCS / stary
        if sciezka.is_dir():
            shutil.rmtree(sciezka)
    for plik in DOCS.glob("*"):
        if plik.is_file():
            plik.unlink()
    (DOCS / "opis").mkdir(parents=True)
    shutil.copy(SRC / "styl.css", DOCS / "opis" / "styl.css")
    shutil.copy(ZASOBY / "projekt_tabeli_podglad.png", DOCS / "opis" / "projekt_tabeli_podglad.png")

    poprzedni, poprzednie_pliki, poprzednie_podstrony = None, set(), {}
    for nr in ZADANIA:
        folder = DOCS / f"zadanie{nr}"
        folder.mkdir()
        kod = renderuj(nr)
        (folder / "index.html").write_text(kod, encoding="utf-8")
        for nazwa, tresc in podstrony(nr).items():
            (folder / nazwa).write_text(tresc, encoding="utf-8")
        for nazwa in zasoby(nr):
            shutil.copy(ZASOBY / nazwa, folder / nazwa)
        pliki = {p.name for p in folder.iterdir()}
        nowe = sorted(pliki - poprzednie_pliki - {"index.html"})
        dodatki = {}
        if etapy(nr):
            plik, lista = etapy(nr)
            (DOCS / "opis" / "etapy").mkdir(exist_ok=True)
            for e, (_, _, kod_etapu) in enumerate(lista, 1):
                kopia = kod_etapu.replace('href="index.html"', f'href="../../zadanie{nr}/index.html"')
                (DOCS / "opis" / "etapy" / f"zadanie{nr}_etap{e}.html").write_text(kopia, encoding="utf-8")
            dodatki = dict(etapy_html=sekcja_etapow(nr, plik, lista, poprzednie_podstrony[plik]), glowny=plik, kod_glowny=lista[-1][2])
        (DOCS / "opis" / f"zadanie{nr}.html").write_text(strona_opisu(nr, kod, poprzedni, nowe, **dodatki), encoding="utf-8")
        poprzedni, poprzednie_pliki, poprzednie_podstrony = kod, pliki, podstrony(nr)

    (DOCS / "index.html").write_text(strona_glowna(), encoding="utf-8")


if __name__ == "__main__":
    main()
