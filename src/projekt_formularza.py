"""Zadanie 10: rysunek projektu formularza, tak jak ołówkiem na kartce A4 (zasoby/projekt_formularza_doe.png).

Uruchom: uvx --with pillow python src/projekt_formularza.py
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

random.seed(7)
SZER, WYS = 1240, 1754
OLOWEK = (70, 70, 78)
SZARY = (130, 130, 140)
FONT = "/System/Library/Fonts/Noteworthy.ttc"

img = Image.new("RGB", (SZER, WYS), (252, 251, 246))
d = ImageDraw.Draw(img)


def f(rozmiar, gruby=False):
    return ImageFont.truetype(FONT, rozmiar, index=1 if gruby else 0)


def linia(x1, y1, x2, y2, kolor=OLOWEK, w=2):
    # Linia z lekkim drżeniem ręki.
    kroki = max(2, int(max(abs(x2 - x1), abs(y2 - y1)) / 40))
    pkt = [(x1 + (x2 - x1) * i / kroki + random.uniform(-1.2, 1.2), y1 + (y2 - y1) * i / kroki + random.uniform(-1.2, 1.2)) for i in range(kroki + 1)]
    d.line(pkt, fill=kolor, width=w)


def prostokat(x1, y1, x2, y2, w=2):
    linia(x1, y1, x2, y1, w=w)
    linia(x2, y1, x2, y2, w=w)
    linia(x2, y2, x1, y2, w=w)
    linia(x1, y2, x1, y1, w=w)


def tekst(x, y, t, r=24, gruby=False, kolor=OLOWEK):
    d.text((x, y), t, font=f(r, gruby), fill=kolor)


def pole(x, y, etykieta, szer=150, uwaga=None):
    tekst(x, y, etykieta)
    prostokat(x + 135, y + 4, x + 135 + szer, y + 34)
    if uwaga:
        tekst(x + 140, y + 6, uwaga, 18, kolor=SZARY)


def lista(x, y, etykieta, opcja, uwaga):
    tekst(x, y, etykieta, gruby=True)
    prostokat(x, y + 36, x + 190, y + 70)
    tekst(x + 8, y + 38, opcja, 22)
    d.polygon([(x + 165, y + 48), (x + 181, y + 48), (x + 173, y + 60)], outline=OLOWEK)
    tekst(x + 200, y + 42, uwaga, 18, kolor=SZARY)


def kolko(x, y, pelne=False):
    d.ellipse((x, y, x + 16, y + 16), outline=OLOWEK, width=2, fill=OLOWEK if pelne else None)


def kwadrat(x, y, pelny=False):
    prostokat(x, y, x + 16, y + 16)
    if pelny:
        linia(x + 2, y + 9, x + 7, y + 15)
        linia(x + 7, y + 15, x + 16, y - 2)


def pionowo(x, y, pytanie, opcje, znak):
    tekst(x, y, pytanie, gruby=True)
    for i, o in enumerate(opcje):
        znak(x + 4, y + 50 + i * 42)
        tekst(x + 32, y + 42 + i * 42, o, 22)


def poziomo(x, y, pytanie, opcje, znak, zaznaczona=None, odstep=None):
    tekst(x, y, pytanie, gruby=True)
    x += int(d.textlength(pytanie, font=f(24, True))) + 20
    for i, o in enumerate(opcje):
        znak(x, y + 10, i == zaznaczona)
        tekst(x + 24, y + 2, o, 22)
        x += odstep or int(d.textlength(o, font=f(22))) + 50


# Nagłówek kartki.
tekst(70, 40, "Doe John 2F g1", 26, True)
tekst(950, 40, "30.10.2026", 26)
tekst(170, 110, "Formularz zapisu na Kółko Robotyki", 46, True)
linia(170, 175, 170 + int(d.textlength("Formularz zapisu na Kółko Robotyki", font=f(46, True))), 175, w=3)
tekst(70, 200, "Kolor tła: #E8F4FD", 26, True)
tekst(420, 205, "(jasnoniebieski)", 22, kolor=SZARY)

# Siatka tabeli: 3 kolumny, 6 wierszy.
X = [70, 455, 760, 1170]
Y = [260, 600, 830, 950, 1030, 1200, 1310]
for y in Y:
    linia(X[0], y, X[3], y)
for x in (X[0], X[3]):
    linia(x, Y[0], x, Y[-1])
for x in X[1:3]:
    linia(x, Y[0], x, Y[2])
    linia(x, Y[5], x, Y[6])

# Wiersz 1.
tekst(85, 270, "Twoje dane", gruby=True)
pole(85, 320, "Imię")
pole(85, 375, "Szkoła", uwaga="ZSE Gdańsk")
pole(85, 430, "Login", uwaga="max 12 znaków")
pole(85, 485, "Hasło", uwaga="• • • • •")
pole(85, 540, "E-mail")
lista(470, 270, "Klasa", "klasa 2", "5 opcji")
lista(470, 375, "Ulubiony język", "", "4 opcje")
lista(470, 480, "Godzina zajęć", "15:30", "3 opcje")
tekst(470, 560, "domyślnie: klasa 2 i 15:30", 18, kolor=SZARY)
pionowo(775, 270, "Co chcesz budować?", ["Roboty jeżdżące", "Drony", "Ramiona robotyczne", "Inteligentny dom"], lambda x, y: kwadrat(x, y))

# Wiersz 2.
pionowo(85, 610, "Czy umiesz programować?", ["Tak", "Trochę", "Nie"], lambda x, y: kolko(x, y))
pionowo(470, 610, "Co masz w domu?", ["Komputer", "Arduino", "Drukarka 3D"], lambda x, y: kwadrat(x, y))
tekst(775, 610, "Nowe pola HTML5", gruby=True)
for i, (etykieta, rysunek) in enumerate([("Data ur.", "dd.mm.rrrr"), ("Godzina", "--:--"), ("Kolor", ""), ("Zapał", ""), ("Wypełnienie", "")]):
    y = 650 + i * 36
    tekst(775, y, etykieta, 20)
    if i < 2:
        prostokat(915, y + 2, 1080, y + 30)
        tekst(925, y + 4, rysunek, 18, kolor=SZARY)
    elif i == 2:
        prostokat(915, y + 2, 965, y + 30)
        d.rectangle((920, y + 7, 960, y + 25), fill=(46, 117, 182))
    elif i == 3:
        linia(915, y + 16, 1080, y + 16)
        kolko(990, y + 8, True)
    else:
        prostokat(915, y + 6, 1080, y + 24)
        d.rectangle((917, y + 8, 1048, y + 22), fill=SZARY)

# Wiersze 3-5.
poziomo(85, 845, "Skąd wiesz o kółku?", ["Od nauczyciela", "Od kolegi", "Z gazetki", "Z internetu"], lambda x, y, p: kolko(x, y, p), 0)
poziomo(85, 890, "Znajomość elektroniki:", ["1", "2", "3", "4", "5"], lambda x, y, p: kolko(x, y, p), odstep=70)
poziomo(85, 975, "Dni:", ["pon.", "wt.", "śr.", "czw.", "pt."], lambda x, y, p: kwadrat(x, y, p), 0, odstep=110)
tekst(85, 1040, "Napisz, jakiego robota chcesz zbudować:", gruby=True)
prostokat(85, 1080, 1150, 1185)
tekst(95, 1085, "TEXTAREA, 4 wiersze", 18, kolor=SZARY)

# Wiersz 6: przyciski.
for x, napis in [(85, "Powitanie"), (260, "Zmień tło"), (510, "CZYŚĆ"), (850, "WYŚLIJ")]:
    prostokat(x, 1230, x + 150, 1280)
    tekst(x + 18, 1236, napis, 24, napis.isupper())
tekst(85, 1285, "BUTTON + akcja", 16, kolor=SZARY)
tekst(510, 1285, "reset", 16, kolor=SZARY)
tekst(850, 1285, "submit: mailto, temat: Doe", 16, kolor=SZARY)

# Legenda.
tekst(70, 1360, "Legenda:", 24, True)
kolko(200, 1372)
tekst(225, 1362, "radio", 22)
kwadrat(330, 1372)
tekst(355, 1362, "checkbox", 22)
kolko(500, 1372, True)
kwadrat(530, 1372, True)
tekst(560, 1362, "zaznaczone domyślnie", 22)

cel = Path(__file__).parent / "zasoby" / "projekt_formularza_doe.png"
img.save(cel, optimize=True)
print(cel)
