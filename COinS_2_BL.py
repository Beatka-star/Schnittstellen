#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programm, das Metadaten via COinS aus dem KOBV Portal liest und die bibliographischen Angaben ausgibt.
...
authors: Beata Lakenberg, Sebastian Scherübl, Claus Werner
license: MIT License
version: 1.0
date: 2026-07-06
"""




import requests
import sys
from sys import argv
from bs4 import BeautifulSoup
from urllib.parse import parse_qs

DEBUG=True

#Seite KOBV aufrufen und die Anfrage bauen

url = "https://openurl.kobv.de/k2" #Neue URL

def kobv_abfrage (suchbegriff):
    params = {
        "index": "internal", # Suche in internen Index
        "plv": "2", #Layout Version von Seite'
        "sortCrit": "score", #Sortierung nach Relevanz
        "sortOrder": "desc", #Reihenfolge absteigend
        "hitsPerPage": "10",  # 10 Ergebnise pro Seite
        "query": suchbegriff  # hier wird die Variable eingesetzt, um die einfache Suche durchzuführen
    }
    response = requests.get(url, params=params)
    print(response.url)

    """Prüfen, ob die Verbindung funktioniert"""
try:
    response = requests.get(url)
    #print(response.status_code) #muss nicht sein, beim Test gut zu sehen
except Exception as e:
    print(f"\nFehler in der Verbindung:\n{e}")
    sys.exit(1)

if DEBUG:
    print(response.url)  # Debug-Ausgabe der tatsächlichen URL

    # Sicherstellen, dass die Antwort als UTF-8 dekodiert wird
response.encoding = response.apparent_encoding
# Menü
if __name__ == "__main__":
    suchbegriff = input("Bitte geben Sie ein Suchbegriff an: ")
    kobv_abfrage(suchbegriff)
soup = BeautifulSoup(response.content, "html.parser")
print(response.text[:2000])  #Prüft ob KOBV überhaupt sinnvolle HTML-Daten zurückschickt.
alle_coins = soup.find_all("span", class_="Z3988")
print(len(alle_coins))


#print(alle_coins[0]["title"])