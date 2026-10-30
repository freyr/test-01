"""Zadanie 7: zamiana przestarzałych znaczników HTML na style CSS."""
import re

ROZMIARY = {"1": "10px", "2": "13px", "3": "16px", "4": "18px", "5": "24px", "6": "32px", "7": "48px"}


def popraw(kod):
    kod = kod.replace("<html>", '<html lang="pl">', 1)
    kod = re.sub(r'<body bgcolor="([^"]+)">', r'<body style="background-color: \1;">', kod)
    kod = re.sub(
        r'<font color="([^"]+)" size="(\d)" face="([^"]+)">',
        lambda m: f'<span style="color: {m[1]}; font-size: {ROZMIARY[m[2]]}; font-family: \'{m[3]}\';">',
        kod,
    )
    kod = kod.replace("</font>", "</span>")
    kod = re.sub(r'<(p|h\d) align="(\w+)">', r'<\1 style="text-align: \2;">', kod)
    kod = re.sub(r"<center><(\w+)>(.*?)</\1></center>", r'<\1 style="text-align: center;">\2</\1>', kod)
    kod = re.sub(
        r'<img src="([^"]+)" align="(\w+)" border="(\d+)"',
        r'<img src="\1" style="float: \2; border: \3px solid #336699; margin: 4px;"',
        kod,
    )
    kod = re.sub(r'<a name="(\w+)"></a>', r'<span id="\1"></span>', kod)
    kod = re.sub(r'<ul type="(\w+)">', r'<ul style="list-style-type: \1;">', kod)
    kod = re.sub(
        r'<hr size="(\d+)" width="([^"]+)" color="([^"]+)">',
        r'<hr style="height: \1px; width: \2; background-color: \3; border: none;">',
        kod,
    )
    return kod
