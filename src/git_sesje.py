"""Nagrywa prawdziwe sesje terminala do lekcji Git (src/git/sesje.json).

Uruchamia git w folderze tymczasowym: GitHub to lokalne repozytorium bare,
a ścieżki i adresy w wynikach są zamieniane na takie, jakie zobaczy uczeń.
Uruchom z katalogu repozytorium: python3 src/git_sesje.py
"""
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import build

TMP = Path(tempfile.mkdtemp(prefix="git-sesje-")).resolve()
GH = TMP / "github" / "zadania-html.git"
SZKOLA = TMP / "szkola" / "John"
DOM = TMP / "dom" / "John"
URL = "git@github.com:johndoe/zadania-html.git"
EMAIL = "john.doe@example.com"
WYNIK = Path(__file__).parent / "git" / "sesje.json"

sesje = {}
zegar = datetime(2026, 9, 10, 16, 0)


def env(home, przez_web=False):
    data = zegar.strftime("%Y-%m-%dT%H:%M:%S+02:00")
    e = dict(PATH=os.environ["PATH"], HOME=str(home), LANG="C", LC_ALL="C", TERM="dumb", COLUMNS="80",
             GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_DATE=data, GIT_COMMITTER_DATE=data)
    if przez_web:
        e.update(GIT_AUTHOR_NAME="John Doe", GIT_AUTHOR_EMAIL=EMAIL,
                 GIT_COMMITTER_NAME="GitHub", GIT_COMMITTER_EMAIL="noreply@github.com")
    return e


def zamien(tekst):
    for stare, nowe in [
        (f"file://{GH}", URL),
        (f"file://{str(GH)[:-4]}", URL[:-4]),
        (str(SZKOLA), "/c/Users/John"),
        (str(DOM), "/c/Users/John"),
        (str(TMP), "/c/Users"),
        ("To git@github.com:", "To github.com:"),
        ("From git@github.com:", "From github.com:"),
    ]:
        tekst = tekst.replace(stare, nowe)
    return tekst


def sh(polecenie, cwd, home, przez_web=False):
    global zegar
    zegar += timedelta(minutes=1)
    r = subprocess.run(["bash", "-c", polecenie], cwd=cwd, env=env(home, przez_web),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Postęp (--progress) nadpisuje linię znakiem \r: zostaje tylko jej ostatni stan.
    out = r.stdout.decode("utf-8")
    return "\n".join(l.rstrip("\r").split("\r")[-1].rstrip() for l in out.split("\n"))


class Sesja:
    """Kolejne polecenia w jednym oknie terminala."""

    def __init__(self, nazwa, home, cwd=None):
        self.kroki = sesje.setdefault(nazwa, [])
        self.home, self.cwd = home, cwd or home

    def sciezka(self):
        s = "~" + str(self.cwd)[len(str(self.home)):]
        if (self.cwd / ".git").exists():
            galaz = sh("git branch --show-current", self.cwd, self.home).strip()
            s += f" ({galaz})"
        return s

    def __call__(self, pokazane, naprawde=None, obetnij=None, diff=False, wynik=None):
        krok = dict(prompt=self.sciezka(), cmd=pokazane)
        if pokazane.startswith("cd "):
            self.cwd = (self.cwd / pokazane[3:].replace("~", str(self.home))).resolve()
            out = ""
        else:
            out = wynik if wynik is not None else zamien(sh(naprawde or pokazane, self.cwd, self.home))
        linie = out.rstrip("\n").split("\n") if out.strip() else []
        if obetnij and len(linie) > obetnij:
            linie = linie[:obetnij] + ["…"]
        krok["out"] = "\n".join(linie)
        if diff:
            krok["diff"] = True
        self.kroki.append(krok)

    def uwaga(self, tekst):
        self.kroki.append(dict(uwaga=tekst))


def zadanie(nr, folder):
    """Zapisuje do folderu pliki strony po zadaniu nr."""
    (folder / "index.html").write_text(build.renderuj(nr), encoding="utf-8")
    for nazwa, tresc in build.podstrony(nr).items():
        (folder / nazwa).write_text(tresc, encoding="utf-8")
    for nazwa in build.zasoby(nr):
        shutil.copy(build.ZASOBY / nazwa, folder / nazwa)


def konfiguruj(home):
    for k, v in [("user.name", "John Doe"), ("user.email", EMAIL), ("pull.rebase", "true")]:
        sh(f'git config --global {k} "{v}"', home, home)


def main():
    global zegar
    for home in (SZKOLA, DOM):
        for f in ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos"]:
            (home / f).mkdir(parents=True)

    # Repozytorium na GitHubie: zadania 1-3 wgrane przez stronę WWW (Upload files, edycja pliku).
    GH.parent.mkdir()
    sh(f"git init -q --bare -b main {GH}", TMP, TMP)
    web = TMP / "web"
    sh(f"git clone -q file://{GH} {web}", TMP, TMP)
    (web / "README.md").write_text("# zadania-html\n", encoding="utf-8")
    for data, opis, nr in [((9, 10, 16, 2), "Initial commit", None), ((9, 15, 17, 40), "Add files via upload", 1),
                           ((9, 22, 18, 5), "Update index.html", 2), ((9, 29, 16, 50), "Add files via upload", 3)]:
        zegar = datetime(2026, *data)
        if nr:
            zadanie(nr, web)
        sh(f'git add -A && git commit -q -m "{opis}"', web, TMP, przez_web=True)
    sh("git push -q origin main", web, TMP)

    # Lekcja 3: wiersz poleceń.
    zegar = datetime(2026, 10, 1, 17, 0)
    t = Sesja("terminal", SZKOLA)
    t("pwd")
    t("ls", "ls -C")
    t("cd Documents")
    t("pwd")
    t("mkdir informatyka")
    t("ls", "ls -C")
    t("cd informatyka")
    t("pwd")
    t("cd ..")
    t("pwd")
    t("cd ~")

    # Lekcja 4: konfiguracja.
    k = Sesja("konfiguracja", SZKOLA)
    k("git --version", wynik="git version 2.51.0.windows.1")
    k('git config --global user.name "John Doe"')
    k(f'git config --global user.email "{EMAIL}"')
    k("git config --global pull.rebase true")
    k("git config --global --list")
    konfiguruj(DOM)

    # Lekcja 5: klucz SSH.
    s = Sesja("ssh", SZKOLA)
    klucz = SZKOLA / ".ssh" / "id_ed25519"
    klucz.parent.mkdir()
    out = zamien(sh(f'ssh-keygen -q -t ed25519 -C "{EMAIL}" -f {klucz} -N "" && ssh-keygen -l -f {klucz}.pub && ssh-keygen -lv -f {klucz}.pub | tail -n +2', SZKOLA, SZKOLA)).split("\n")
    s(f'ssh-keygen -t ed25519 -C "{EMAIL}"', wynik="\n".join([
        "Generating public/private ed25519 key pair.",
        "Enter file in which to save the key (/c/Users/John/.ssh/id_ed25519):",
        "Created directory '/c/Users/John/.ssh'.",
        "Enter passphrase (empty for no passphrase):",
        "Enter same passphrase again:",
        "Your identification has been saved in /c/Users/John/.ssh/id_ed25519",
        "Your public key has been saved in /c/Users/John/.ssh/id_ed25519.pub",
        "The key fingerprint is:",
        out[0].split(" ", 1)[1].rsplit(" (", 1)[0],
        "The key's randomart image is:",
        *[l for l in out[1:] if l.strip()],
    ]))
    s("ls ~/.ssh", "ls -C ~/.ssh")
    s("cat ~/.ssh/id_ed25519.pub")
    s("ssh -T git@github.com", wynik="\n".join([
        "The authenticity of host 'github.com (140.82.121.3)' can't be established.",
        "ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.",
        "This key is not known by any other names.",
        "Are you sure you want to continue connecting (yes/no/[fingerprint])? yes",
        "Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.",
        "Hi johndoe! You've successfully authenticated, but GitHub does not provide shell access.",
    ]))

    # Komputer w domu klonuje repozytorium wcześniej (potrzebne w lekcji 8).
    zegar = datetime(2026, 10, 4, 19, 0)
    sh(f"git clone -q file://{GH} zadania-html", DOM, DOM)

    # Lekcja 6: klonowanie i stan.
    zegar = datetime(2026, 10, 6, 17, 0)
    c = Sesja("klon", SZKOLA)
    c(f"git clone {URL}", f"git clone --progress file://{GH}")
    c("cd zadania-html")
    c("ls", "ls -C")
    c("git status")
    c("git log --oneline", "git log --oneline --decorate")
    c("git log -1")
    c("git remote -v")

    # Lekcja 7: zadanie 4 (zmiana pliku) i zadanie 5 (nowe pliki).
    repo = SZKOLA / "zadania-html"
    z = Sesja("zmiana", SZKOLA, repo)
    z.uwaga("Edytujesz index.html (zadanie 4) i zapisujesz plik.")
    zadanie(4, repo)
    z("git status")
    z("git diff", obetnij=22, diff=True)
    z("git add index.html")
    z("git status")
    z('git commit -m "Zadanie 4: wyliczenia i numerowania"')
    z("git log --oneline", "git log --oneline --decorate")

    n = Sesja("nowe_pliki", SZKOLA, repo)
    n.uwaga("Zadanie 5: zmieniasz index.html i kopiujesz do folderu 5 obrazków .gif.")
    zadanie(5, repo)
    n("git status")
    n("git add .")
    n("git status")
    n('git commit -m "Zadanie 5: animowane grafiki"')

    # Lekcja 8: push, pull w domu, odrzucony push.
    p = Sesja("push", SZKOLA, repo)
    p("git push", "git push --progress")
    p("git status")
    p("git log --oneline", "git log --oneline --decorate")

    zegar = datetime(2026, 10, 12, 18, 0)
    dom = DOM / "zadania-html"
    d = Sesja("dom", DOM, dom)
    d.uwaga("Komputer w domu. Repozytorium jest sklonowane od tygodnia.")
    d("git log --oneline", "git log --oneline --decorate")
    d("git pull", "git pull --progress")
    d("git log --oneline", "git log --oneline --decorate")
    d.uwaga("Dopisujesz opis do README.md.")
    (dom / "README.md").write_text("# zadania-html\n\nZadania HTML z informatyki - John Doe, klasa 2F, grupa 1.\n\nStrona: https://johndoe.github.io/zadania-html/\n", encoding="utf-8")
    d("git add README.md")
    d('git commit -m "Opis repozytorium w README"')
    d("git push", "git push --progress")

    zegar = datetime(2026, 10, 13, 17, 0)
    o = Sesja("odrzucony", SZKOLA, repo)
    o.uwaga("Następnego dnia w szkole. Robisz zadanie 6, ale zapominasz o git pull.")
    zadanie(6, repo)
    o("git add .")
    o('git commit -m "Zadanie 6: linki i podstrony"')
    o("git push", "git push --progress")
    o("git pull", "git pull --progress")
    o("git push", "git push --progress")
    o("git log --oneline", "git log --oneline --decorate")

    WYNIK.parent.mkdir(exist_ok=True)
    WYNIK.write_text(json.dumps(sesje, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    shutil.rmtree(TMP)
    print(WYNIK)


if __name__ == "__main__":
    main()
