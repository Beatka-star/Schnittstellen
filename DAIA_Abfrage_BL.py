"""
! /usr/bin/python3
Programm, der anhand PPN die Verfügbarkeit aller Exemplare
für die SUB Göttingen ausgibt
ISIL:SUB Göttingen DE-7

Version 1.0, Autoren: Beata Lakeberg, Sebastian Scherübl, Claus Werner
"""
import xml.etree.ElementTree as ET

import requests


BASE_URL = "https://daia.gbv.de/isil/DE-7"


def daia_abfrage(ppn):
    params = {
        "id": f"ppn:{ppn}",
        "format": "xml",
    }

    response = requests.get(BASE_URL, params=params)

    print(response.text)  # für Testzwecke, später kann man löschen; zum testen ppns 225564580   1618460277

    parse_results(response.text)


def parse_results(xml_text):
    root = ET.fromstring(xml_text)

    # root.tag
    # "daia"
    for document in root:
        for item in document:
            for info in item:
                info.tag = info.tag.replace("{http://ws.gbv.de/daia/}", "")
                info.tag = info.tag.replace("label", "")
                if info.text:
                    print(info.text)
                if info.attrib.get('service'):
                    print(f"{info.attrib.get('service')}: {info.tag}")


# Menü
ppn = input("Bitte geben Sie PPN-ID an: ")
daia_abfrage(ppn)
