#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programm, das Metadaten via COinS aus dem KOBV Portal liest und die bibliographischen Angaben ausgibt.
...
authors: Beata Lakenberg, Sebastian Scherübl, Claus Werner
license: MIT License
version: 1.0
date: 2026-07-12
"""




import requests
import sys
from sys import argv
from bs4 import BeautifulSoup
from urllib.parse import parse_qs

DEBUG=True


"""Liest COinS-Metadaten von einer KOBV-Titelseite aus. Der Link zur Titelseite wird von Nutzer angegeben. 
Zwar wird hier, wie gewünscht, die KOBV.Abfrage gemacht, der Programm funktioniert aber auch mit Links zu anderen Katalogen, 
die COinS haben (z.B. BVB)."""

"""
...
Hinweis: KOBV, GBV und WorldCat verwenden Bot-Schutz (Anubis),der ohne JavaScript nicht umgehbar ist. Das Programm wurde 
erfolgreich mit Katalog von BVB und Wikipedia getestet (88 COinS gefunden).
"""

def kobv_abfrage (kataloglink):

    #User-Agent Header. Damit schickt der Brawser die Erkennung, dass es kein Bot ist

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "de-DE,de;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    #Prüfen, ob die Verbindung funktioniert:
    try:
        response = requests.get(url=kataloglink, headers=headers)
    except Exception as e:
         print(f"\nFehler in der Verbindung:\n{e}")
         sys.exit(1)
    #Wenn die Fehlermeldung kommt, kann es an folgenden liegen: Server ist nicht erreichbar; kein Internet;URL ist falsch geschrieben

    # Statuscode prüfen, wenn Fehlermeldung kommt, kann es an folgenden liegen: Seite nicht gefunden (404); Zugriff verweigert (403); Serverfehler (500)
    if response.status_code != 200:
        print("Anfrage fehlgeschlagen! Statuscode:", response.status_code)
        sys.exit(1)

    if DEBUG:
        print("URL:", response.url)
        print("Statuscode:", response.status_code)

    # Sicherstellen, dass die Antwort als UTF-8 dekodiert wird
    response.encoding = response.apparent_encoding

    #Rückgabe einen HTML-Inhalt
    return response.content

def parse_results (html_inhalt):
    #liest COinS-Metadaten aus der HTML aus.
    soup = BeautifulSoup(html_inhalt, "html.parser") #BeautifulSoup macht HTML durchsuchbar

    if DEBUG:
        print(html_inhalt[:2000])  #Prüft ob KOBV überhaupt sinnvolle HTML-Daten zurückschickt.

    alle_coins = soup.find_all("span", class_="Z3988") #Findet alle Elemente, die Name "span" und Klasse "Z3988" haben
    print("Gefundene COinS: ", len(alle_coins)) #Gibt alle gefundene COinS aus

    for coins in alle_coins:
        daten = parse_qs(coins["title"]) #nacht aus einen URL-String ein Dictionary und gibt Listen zurück (auch wenn die Liste 1 Wert enthält).
        #für Autorangaben werden mehrere Keys überprüft
        autor=daten.get("rft.au", [None])[0] #Liesst erstes Element aus der Liste
        if not autor:
            nachname=daten.get("rft.aulast", ["-"])[0]
            vorname = daten.get("rft.aufirst", ["-"])[0]
            autor=nachname+" "+vorname

        #Seitenangaben bei Zeitschriftenartikel müssen getrennt ausgelesen werden
        spage=daten.get("rft.spage", ["-"])[0]
        epage=daten.get("rft.epage", ["-"])[0]
        seitenangaben=spage+" - "+epage

        #Ausgabe
        print("Autor:in:", autor)
        print("Herausgeber:in", daten.get("rft.aucorp",["-"])[0])
        print("Artikeltitel:", daten.get("rft.atitle", ["-"])[0])
        print("Titel:", daten.get("rft.title", ["-"])[0])
        #print("Zeitschrifttitel:", daten.get("rft.title", ["-"])[0])
        print("Seitenangaben:", seitenangaben)
        #print("Monographietitel:", daten.get("rft.btitle", ["-"])[0])
        print("ISBN: ", daten.get("rft.isbn", ["-"])[0])
        print("ISSN: ", daten.get("rft.issn", ["-"])[0])
        print("Seitenzahl:", daten.get("rft.pages", ["-"])[0])
        print("---")

# Menü
if __name__ == "__main__":
    kataloglink = input("Bitte geben Sie einen Link zum Exemplar an: ")
    html_inhalt=kobv_abfrage(kataloglink)
    parse_results(html_inhalt)


