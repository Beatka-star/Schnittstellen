import requests
import xml.etree.ElementTree as ET


# Ausgabe der gefundenen Treffer
def output_xml(xml_found):
    for i, item in enumerate(xml_found, start=1):
        print(f"\n{i}. Exemplar")
        print("Signatur:", item["label"])
        print("EPN:", item["epn"])
        print("Verfügbarkeit:", ", ".join(item["availability"]))
    return


# XML analysieren und Daten extrahieren
def find_variables_xml(xml_dataset):

    root = ET.fromstring(xml_dataset)

    items = []

    for item in root.findall(".//{*}item"):

        label = item.findtext(".//{*}label")
        epn = item.get("id")

        availability = []

        # AVAILABLE
        for av in item.findall(".//{*}available"):
            service = av.get("service")
            availability.append(f"{service}: available")

        # UNAVAILABLE
        for uv in item.findall(".//{*}unavailable"):
            service = uv.get("service")
            availability.append(f"{service}: unavailable")

        items.append({
            "label": label,
            "epn": epn,
            "availability": availability
        })

    return items


# XML Daten von der SRU Schnittstelle laden
def load_xml(base_url, params):

    # HTTP Anfrage senden
    response_xml = requests.get(base_url, params=params)

    # Verbindungsfehler abfangen
    if response_xml.status_code != 200:
        print("Fehler: Anfrage fehlgeschlagen (Status:", response_xml.status_code, ")")
        return None

    # UTF-8 Zeichensatz setzen
    response_xml.encoding = "utf-8"

    # XML als Text zurückgeben
    return response_xml.text


# SRU Anfrageparameter erstellen
def build_sru_url(ppn, isil):

    base_url = f"http://daia.gbv.de/isil/{isil}"

    params = {
        "id": f"ppn:{ppn}",
        "format": "xml"
    }

    return base_url, params


# Hauptprogramm
def main():

    print("Willkommen zur Verfügbarkeitsprüfung der SLUB Göttingen")

    print("\nHinweis: ppn Ziffern dürfen nur neunstellig sein.")

    #Sigel Göttingen
    sigel_goettingen = "DE-7"
    # Auswahl des Suchfeldes
    ppn = input("Geben sie die gesuchte PPN ein:")
    if not ppn.isdigit() or len(ppn) not in (9, 10):
        print("Fehler: PPN muss 9 oder 10 Ziffern haben.")
        return
    base_url, params = build_sru_url(ppn, sigel_goettingen)

    print("\nErzeugte URL:")
    print(requests.Request("GET", base_url, params=params).prepare().url)


    # XML laden
    xml_dataset = load_xml(base_url, params)
    # Verbindungsfehler abfangen
    if xml_dataset is None:
        print("Zugriffsproblem.")
        return
    xml_found = find_variables_xml(xml_dataset)
    # Keine Exemplare
    if not xml_found:
        print("Keine Exemplare gefunden.")
        return
    #print(xml_found)
    output_xml(xml_found)



# Programmstart
if __name__ == "__main__":
    main()
