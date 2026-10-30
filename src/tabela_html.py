"""Zadanie 9: tabela z projektu (tabela.py) jako tabela_doe.html, w trzech etapach z instrukcji."""
import tabela

# Punkty z Worda na piksele (1 pt = 4/3 px).
PX = {11: 15, 12: 16, 14: 19}
RAMKA = f"border: 1px solid #{tabela.RAMKA_KOLOR};"

ETAPY = [
    ("Szkielet tabeli",
     "Sama struktura: <code>&lt;table&gt;</code>, <code>&lt;caption&gt;</code>, <code>&lt;thead&gt;</code>, "
     "<code>&lt;tbody&gt;</code>, wiersze <code>&lt;tr&gt;</code> i komórki. Atrybut <code>border=\"1\"</code> "
     "rysuje tymczasową ramkę. Komórki, które później zostaną scalone, są na razie puste."),
    ("Formatowanie stylami CSS",
     "Każdy wiersz dostaje kolor tła, każda komórka kolor, krój, rozmiar i wyrównanie tekstu. "
     "Tabela dostaje podwójną ramkę 4px, komórki ramkę 1px: zewnętrzna jest 4 razy grubsza. "
     "Atrybut <code>border</code> znika, bo ramkę rysuje teraz CSS."),
    ("Scalanie komórek",
     "Puste komórki znikają. <code>rowspan=\"2\"</code> łączy komórkę z komórką pod nią (Lenovo, Dell), "
     "<code>colspan=\"3\"</code> łączy trzy komórki w wierszu (Apple)."),
]


def styl_komorki(k):
    _, kroj, rozmiar, kolor, wyrownanie, pogrubienie = tabela.KOLUMNY[k]
    styl = f"{RAMKA} padding: 4px 8px; color: #{kolor}; font-family: '{kroj}'; font-size: {PX[rozmiar]}px; text-align: {wyrownanie};"
    return styl + (" font-weight: bold;" if pogrubienie else "")


def strona(etap):
    st = etap >= 2
    w = []
    a = w.append
    a("<!DOCTYPE html>")
    a('<html lang="pl">')
    a("\t<head>")
    a('\t\t<meta charset="UTF-8">')
    a('\t\t<meta name="author" content="John Doe">')
    a("\t\t<title>Tabela - John Doe</title>")
    a("\t</head>")
    a("\t<!-- Autor: Doe John, szkoła: ZSE Gdańsk, klasa: 2F grupa 1 -->")
    a('\t<body style="background-color: #CCFFCC;">')
    a("\t\t<h1>Tabela - John Doe</h1>")
    if st:
        a(f'\t\t<table style="border: {int(tabela.RAMKA_ZEWN_PT / tabela.RAMKA_WEWN_PT)}px double #{tabela.RAMKA_KOLOR}; border-collapse: collapse; background-color: #FFFFFF;">')
        a(f"\t\t\t<caption style=\"font-family: 'Arial'; font-size: {PX[14]}px; font-weight: bold; padding: 8px;\">{tabela.TYTUL}</caption>")
    else:
        a('\t\t<table border="1">')
        a(f"\t\t\t<caption>{tabela.TYTUL}</caption>")
    a("\t\t\t<thead>")
    a(f'\t\t\t\t<tr style="background-color: #{tabela.NAGLOWEK_TLO}; color: #{tabela.NAGLOWEK_KOLOR};">' if st else "\t\t\t\t<tr>")
    for nazwa, *_ in tabela.KOLUMNY:
        th = f"<th style=\"{RAMKA} padding: 6px 8px; font-family: 'Arial'; font-size: {PX[12]}px;\">" if st else "<th>"
        a(f"\t\t\t\t\t{th}{nazwa}</th>")
    a("\t\t\t\t</tr>")
    a("\t\t\t</thead>")
    a("\t\t\t<tbody>")
    for kolor_tla, wiersz in tabela.WIERSZE:
        a(f'\t\t\t\t<tr style="background-color: #{kolor_tla};">' if st else "\t\t\t\t<tr>")
        for k, komorka in enumerate(wiersz):
            if komorka is None and etap >= 3:
                continue
            tekst, colspan, rowspan = ("", 1, 1) if komorka is None else (komorka, 1, 1) if isinstance(komorka, str) else komorka
            atr = ""
            if etap >= 3:
                atr += f' rowspan="{rowspan}"' if rowspan > 1 else ""
                atr += f' colspan="{colspan}"' if colspan > 1 else ""
            if st:
                styl = styl_komorki(k)
                if colspan > 1 and etap >= 3:
                    styl = styl.replace("text-align: left", "text-align: center")
                atr += f' style="{styl}"'
            a(f"\t\t\t\t\t<td{atr}>{tekst}</td>")
        a("\t\t\t\t</tr>")
    a("\t\t\t</tbody>")
    a("\t\t</table>")
    if st:
        a(f'\t\t<p style="color: #FF0000; font-style: italic; text-decoration: underline; font-size: 32px;">{tabela.ZRODLO}</p>')
    else:
        a(f"\t\t<p>{tabela.ZRODLO}</p>")
    a('\t\t<p><a href="index.html">wróć</a></p>')
    a("\t</body>")
    a("</html>")
    return "\n".join(w) + "\n"
