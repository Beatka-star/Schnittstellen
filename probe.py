#! /usr/bin/python3

# cmdline.py -- Programmierbeispiel zum Auswerten der Kommandozeilenparameter
# Vers. 1.0, Autor: Stefan Lohrum lohrum@zib.de, Lizenz: CC-BY-SA

# Standard Bibliotheken importieren
import sys

# Fehlermeldungen
FEHLER_LAENGE = "ISBN 10 ist falsch. muss 10 Zeichen haben"
FEHLER_PARAMETER = "Bitte nur ein ISBN angeben"
FEHLER_ALLGEMEIN = "isbn ist falsch"

print(sys.argv, file=sys.stderr)

# Anzehl von Kommadozailenparamether prüfen

if len(sys.argv) != 2:
    print(FEHLER_PARAMETER, file=sys.stderr)

# Übernahme der ISBN-10 über Kommandozeile
isbn10_input = sys.argv[1]



#prufung ob nur numerische Zeichen
for c in isbn10_input[:-1]:
    if c not in "1234567890-":
        print(FEHLER_ALLGEMEIN, file=sys.stderr)
#else:
 #   print(isbn_10)

for c in isbn10_input[-1]:
    if c not in "1234567890Xx-":
        print(FEHLER_ALLGEMEIN, file=sys.stderr)
#else:
 #       print(isbn_10)

# isbn-cleaning
isbn_10 = isbn10_input.replace("-", "").replace("x", "X")
print(isbn_10)

# Länge prüfen
if len(isbn_10) != 10:
    print(FEHLER_LAENGE, file=sys.stderr)

#isbn 13 erstellen
isbn_13=str("978")+str(isbn_10)
print(isbn_13)


