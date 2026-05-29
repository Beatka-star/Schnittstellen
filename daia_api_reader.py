import requests
import xml.etree.ElementTree as ET


# Ausgabe der Ergebnisse (Lesbare Darstellung im Terminal)
def output_xml(xml_found):

    # jedes gefundene Exemplar einzeln ausgeben
    for i, item in enumerate(xml_found, start=1):

        print(f"\n{i}. Exemplar")

        # Signatur / Bibliothekssignatur
        print("Signatur:", item["label"])

        # interne ID (EPN = Exemplar-Nummer)
        print("EPN:", item["epn"])

        # Verfügbarkeit als Liste ausgeben
        print("Verfügbarkeit:", ", ".join(item["availability"]))

    return


# XML analysieren und relevante Daten herausziehen
def find_variables_xml(xml_dataset):

    # XML-String in Baumstruktur umwandeln
    root = ET.fromstring(xml_dataset)

    # Ergebnisliste für alle Exemplare
    items = []

    # alle items durchlaufen
    for item in root.findall(".//{*}item"):

        # Signatur
        label = item.findtext(".//{*}label")

        # eindeutige ID
        epn = item.get("id")

        # Liste für Verfügbarkeitsinfos
        availability = []

        # available
        for av in item.findall(".//{*}available"):
            service = av.get("service")  # loan, presentation, interloan
            availability.append(f"{service}: available")

        # unavailable
        for uv in item.findall(".//{*}unavailable"):
            service = uv.get("service")
            availability.append(f"{service}: unavailable")

        # alles pro Exemplar speichern
        items.append({
            "label": label,
            "epn": epn,
            "availability": availability
        })

    return items


# API Anfrage durchführen und XML holen
def load_xml(base_url, params):

    # Request an DAIA-Server
    response_xml = requests.get(base_url, params=params)

    # Problem mit Server abfangen
    if response_xml.status_code != 200:
        print("Fehler: Anfrage fehlgeschlagen (Status:", response_xml.status_code, ")")
        return None

    # Encoding setzen z.B. wegen Umlauten
    response_xml.encoding = "utf-8"

    # XML als Text zurückgeben
    return response_xml.text


# URL und Parameter für DAIA Anfrage bauen
def build_sru_url(ppn, isil):

    # Basis-URL der DAIA Schnittstelle
    base_url = f"http://daia.gbv.de/isil/{isil}"

    # Parameter für die Anfrage
    params = {
        "id": f"ppn:{ppn}",
        "format": "xml"
    }

    return base_url, params


# Hauptprogramm
def main():

    print("Willkommen zur Verfügbarkeitsprüfung der SLUB Göttingen")

    print("\nHinweis: PPN muss 9 oder 10 Ziffern haben.")

    # ISIL
    sigel_goettingen = "DE-7"

    # Eingabe
    ppn = input("Geben sie die gesuchte PPN ein:")

    # nur Zahlen und richtige Länge erlauben
    if not ppn.isdigit() or len(ppn) not in (9, 10):
        print("Fehler: PPN muss 9 oder 10 Ziffern haben.")
        return

    # URL und Parameter erstellen
    base_url, params = build_sru_url(ppn, sigel_goettingen)

    print("\nErzeugte URL:")
    print(requests.Request("GET", base_url, params=params).prepare().url)

    # XML von Server laden
    xml_dataset = load_xml(base_url, params)

    # wenn Anfrage fehlgeschlagen ist, abbrechen
    if xml_dataset is None:
        print("Zugriffsproblem.")
        return

    # XML auswerten
    xml_found = find_variables_xml(xml_dataset)

    # keine Exemplare gefunden
    if not xml_found:
        print("Keine Exemplare gefunden.")
        return

    # Ergebnisse ausgeben
    output_xml(xml_found)


# Programmstart
if __name__ == "__main__":
    main()
