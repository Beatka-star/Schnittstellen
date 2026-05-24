"""
! /usr/bin/python3
Programm, mit dem man über die SRU Schnittstelle im
GBV nach Titelstichwörtern, Autoren und ISBN recherchieren kann
(Kombinationen der Suchfelder war  nicht erforderlich).
Ausgabe: ISBN, Autor, Titel, Schlagworte
Quelle: https://verbundwiki.gbv.de/display/VZG/SRU

Version 1.0, Autoren: Beata Lakeberg, Sebastian Scherübl, Claus Werner"""

# Fehlermeldungen
FEHLER_UNGUELTIGE_AUSWAHL = "Bitte 1,2 oder 3 auswählen."

import xml.etree.ElementTree as ET

import requests

BASE_URL = "https://sru.k10plus.de/gvk"

def gbv_abfrage(query_type, search_term, max_records=10):
    """
    query_type: 'tit', 'prs', oder 'isbn'
    """
    index_map = {
        "tit": "pica.tit",  # Titelstichwort
        "prs": "pica.prs",  # Autor/Person
        "isbn": "pica.isb",  # ISBN
    }

    params = {
        "version": "1.1",
        "operation": "searchRetrieve",
        "query": f"{index_map[query_type]}={search_term}",
        "maximumRecords": max_records,
        "recordSchema": "marcxml",
    }
    response = requests.get(BASE_URL, params=params)
    print(response.text)  # ausgabe von xml datei ist nicht notwendig aber sehr hilfreich beim testen, daher bleibt es zuerst
    parse_results(response.text)

def parse_results(xml_text):
    # Namespace entfernen
    xml_text = xml_text.replace(' xmlns="http://www.loc.gov/MARC21/slim"', '')

    # XML einlesen
    root = ET.fromstring(xml_text)

    # Alle Datensätze durchgehen
    for record in root.findall(".//record"):
        # wenn erster gefunden wird, dann wird ausgegeben
        isbn = record.find(".//datafield[@tag='020']/subfield[@code='a']")
        autor = record.find(".//datafield[@tag='100']/subfield[@code='a']")
        herausgeber = record.find(".//datafield[@tag='245']/subfield[@code='c']")
        titel = record.find(".//datafield[@tag='245']/subfield[@code='a']")
        untertitel = record.find(".//datafield[@tag='245']/subfield[@code='b']")
        #Ausgabe der Ergebnisse
        print("ISBN:      ", isbn.text if isbn is not None else "nicht vorhanden")
        print("Autor:     ", autor.text if autor is not None else "-")
        print("Herausgeber:", herausgeber.text if herausgeber is not None else "-") #es ist nicht perfekt aber manchmal bei Sammelbänden werden die Herausgeber in Feld 100 nicht genannt
        print("Titel:     ", titel.text if titel is not None else "nicht vorhanden")
        print("Untertitel:", untertitel.text if untertitel is not None else "-")

        # hier werden alle Schlagworte aus den Feldern 650 und 689 ausgesucht und ausgegeben
        schlagworte=[]
        for sw in record.findall(".//datafield[@tag='650']/subfield[@code='a']"):
            schlagworte.append(sw.text)
        for sw in record.findall(".//datafield[@tag='689']/subfield[@code='a']"):
            schlagworte.append(sw.text)

        if schlagworte:
            print("Schlagworte:   ", "/". join(schlagworte))
        else:
            print("Schlagworte nicht vorhanden")
        print("---")

# Menü
choice = input("Suche nach:\n(1) Titelstichwort\n(2) Autor\n(3) ISBN: ")
if choice > "3":
    print (FEHLER_UNGUELTIGE_AUSWAHL)
else:
    term = input("Suchbegriff: ")
    if choice == "1":
        gbv_abfrage("tit",term)
    elif choice == "2":
        gbv_abfrage("prs",term)
    elif choice == "3":
        gbv_abfrage("isbn",term)


