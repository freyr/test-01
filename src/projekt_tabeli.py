"""Zadanie 8: zapisuje projekt tabeli jako plik Word (zasoby/doe_2F_g1.docx).

Uruchom: uvx --with python-docx python src/projekt_tabeli.py
"""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import tabela

WYROWNANIE = {"left": WD_ALIGN_PARAGRAPH.LEFT, "center": WD_ALIGN_PARAGRAPH.CENTER, "right": WD_ALIGN_PARAGRAPH.RIGHT}
SZEROKOSCI = [2.6, 3.4, 3.4, 2.6, 2.4, 2.6]


def ramki(tab):
    # Grubość w ósmych częściach punktu, tak jak zapisuje ją Word.
    zewn, wewn = int(tabela.RAMKA_ZEWN_PT * 8), int(tabela.RAMKA_WEWN_PT * 8)
    granice = OxmlElement("w:tblBorders")
    for nazwa in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{nazwa}")
        wewnetrzna = nazwa.startswith("inside")
        el.set(qn("w:val"), "single" if wewnetrzna else "double")
        el.set(qn("w:sz"), str(wewn if wewnetrzna else zewn))
        el.set(qn("w:color"), tabela.RAMKA_KOLOR)
        granice.append(el)
    tab._tbl.tblPr.append(granice)


def tlo(tc, kolor):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), kolor)
    tc.get_or_add_tcPr().append(shd)


def wpisz(komorka, tekst, kroj, rozmiar, kolor, wyrownanie, pogrubienie):
    for nadmiar in komorka.paragraphs[1:]:
        nadmiar._p.getparent().remove(nadmiar._p)
    akapit = komorka.paragraphs[0]
    akapit.alignment = WYROWNANIE[wyrownanie]
    run = akapit.add_run(tekst)
    run.font.name = kroj
    run.font.size = Pt(rozmiar)
    run.font.color.rgb = RGBColor.from_string(kolor)
    run.bold = pogrubienie
    komorka.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def main():
    doc = Document()
    for sekcja in doc.sections:
        sekcja.left_margin = sekcja.right_margin = Cm(2)

    info = doc.add_paragraph()
    info.add_run("Projekt tabeli - zadanie 8. Autor: John Doe, klasa 2F, grupa 1").italic = True

    tytul = doc.add_paragraph()
    tytul.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = tytul.add_run(tabela.TYTUL)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = "Arial"

    tab = doc.add_table(rows=len(tabela.WIERSZE) + 1, cols=len(tabela.KOLUMNY))
    tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    ramki(tab)
    tab.autofit = False
    for k, szer in enumerate(SZEROKOSCI):
        tab.columns[k].width = Cm(szer)
        for wiersz in tab.rows:
            wiersz.cells[k].width = Cm(szer)

    for k, (nazwa, kroj, *_ ) in enumerate(tabela.KOLUMNY):
        komorka = tab.cell(0, k)
        tlo(komorka._tc, tabela.NAGLOWEK_TLO)
        wpisz(komorka, nazwa, "Arial", 12, tabela.NAGLOWEK_KOLOR, "center", True)

    for w, k, tekst, colspan, rowspan in tabela.komorki():
        komorka = tab.cell(w + 1, k)
        if colspan > 1 or rowspan > 1:
            komorka = komorka.merge(tab.cell(w + rowspan, k + colspan - 1))
        _, kroj, rozmiar, kolor, wyrownanie, pogrubienie = tabela.KOLUMNY[k]
        if colspan > 1:
            wyrownanie = "center"
        wpisz(komorka, tekst, kroj, rozmiar, kolor, wyrownanie, pogrubienie)

    # Kolor także dla ukrytych części komórek scalonych w pionie.
    for w, (kolor_tla, _) in enumerate(tabela.WIERSZE):
        for tc in tab.rows[w + 1]._tr.tc_lst:
            if tc.get_or_add_tcPr().find(qn("w:shd")) is None:
                tlo(tc, kolor_tla)

    zrodlo = doc.add_paragraph()
    run = zrodlo.add_run(tabela.ZRODLO)
    run.italic = True
    run.underline = True
    run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
    run.font.size = Pt(24)

    cel = Path(__file__).parent / "zasoby" / "doe_2F_g1.docx"
    doc.save(cel)
    print(cel, "komórki:", tabela.liczba_komorek())


if __name__ == "__main__":
    main()
