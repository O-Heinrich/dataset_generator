# dataset_generator

Script zum Generieren von Beispiel-Datensätzen für relationale Datenbanken

## Setup

```console
python -m venv generator_venv
generator_venv/bin/pip install wonderwords
generator_venv/bin/pip install Faker
generator_venv/bin/pip install rstr
```

## Usage

```console
python src/dataset_gen.py
```

### Options

| Option | Beschreibung | Default Behavior |
| - | - | - |
| -p | json Datei, in welcher die Informationen über die Datenbank stehen. Siehe [Config](#config) | example.json |
| -f | Datei, in welche das Ergebnis als SQL-Befehl in Textformat geschrieben wird | .sql Datei mit zufällig generierten Namen |
| -a | SQL-Befehl wird an Datei angehangen. Wird von -o überschrieben | False - Existiert die Zieldatei bereits, so wird ein Error geworfen |
| -o | Neuer Inhalt überschreibt Inhalt der Datei, sollte die Datei bereits existieren. Überschreibt -a | False - Existiert die Zieldatei bereits, so wird ein Error geworfen |
| -n | Anzahl der zu generierenden Datensätze. Wenn in config json Datei angegeben, wird dieser Wert überschrieben | 20 |
| -e | Zeichencodierung | utf-8 |
| -l | Location wie in [https://faker.readthedocs.io/en/master/#localization](https://faker.readthedocs.io/en/master/#localization). | de_DE |
> **-l Kann für Addressen zu Fehlern führen.**

### Config

Die Konfiguration geschieht über eine json dabei, in welcher der Name der Tabelle sowie die Art der zu generierenden Daten festgelegt werden kann. Beispielhaft siehe example.json. Die json hat folgende Felder:

| Feldname | Typ | | Beschreibung |
| - | - | - | - |
| db_name | String | required | Name der Tabelle |
| columns | Map | required | Repräsentation der Spalten der Tabelle und ihrer Typen. Siehe [Columns](#columns) |
| amount | int | optional | Anzahl der für diese Tabelle zu generierenden Datensätze. Überschreibt die -n Option |

#### Columns

Das Columns Feld enthält die Namen der Spalten als Schlüssel und die Beschreibung des jeweiligen Datentyps als Wert. Zum Beispiel:

```json
"feldname1": "FIRST_NAME",
"feldname2": {
    "type": "INTEGER",
    "max": 1000
}
```

Der Datentyp kann als einzelner String angegeben werden (case-insensitive), oder als Map in welcher der Typ mit dem Schlüssel "type" vorliegt sowie weitere Parameter. Für manche Typen sind bestimmte Parameter zwangsweise notwendig. Folgende Typen werden unterstützt:

| Typ | Beschreibung | Parameter | Default | Beschreibung |
| - | - | - | - | - |
| FIRST_NAME | Vorname mit evtl Titel | unique | false | Wenn true, keine doppelten Namen werden generiert |
| | | mufm | 3 | Wenn unique true ist, limitiert Anzahl der Versuche auf mufm * n, um Endlosschleifen zu verhindern |
| LAST_NAME | Nachname | unique | false | siehe FIRST_NAME |
| | | mufm | 3 | siehe FIRST_NAME |
| FULL_NAME | Vor- und Nachname | unique | false | siehe FIRST_NAME |
| | | mufm | 3 | siehe FIRST_NAME |
| COMPANY_NAME | vollständiger Name für ein Unternehmen | unique | false | siehe FIRST_NAME |
| | | mufm | 3 | siehe FIRST_NAME |
| STREET | Straßenname, ohne Hausnummer | | | |
| STREET_HOUSENUMBER | Straßenname, mit Hausnummer | | | |
| HOUSENUMBER | Hausnummer, als String | | | |
| TOWN | Stadtname | | | |
| PLZ | Postleitzahl, als String | | | |
| MONEY | Gleitkommazahl mit 2 Nachkommastellen | min | 0 | Kleinster mögliche Wert (inklusiv) |
| | | max | | required - Höchster mögliche Wert (exclusiv), muss größer als min sein |
| FLOAT | Gleitkommazahl mit variable Anzahl Nachkommastellen | min | 0 | Siehe MONEY |
| | | max | | Siehe MONEY |
| | | acc | 100 | Angabe zu Anzahl Nachkommastellen (z. B. 100 -> 2 Nachkommastellen) |
| INTEGER | Ganzzahl | min | 0 | Siehe MONEY |
| | | max | | Siehe MONEY |
| DATE | Datum im üblichen SQL-Format (YYYY-MM-DD) | unique | false | siehe FIRST_NAME |
| | | mufm | 3 | siehe FIRST_NAME |
| TIME | Uhrzeit im üblichen SQL-Format (HH:MI:SS) | unique | false | siehe FIRST_NAME |
| | | mufm | 3 | siehe FIRST_NAME |
| DATE_TIME | Datum und Uhrzeit im üblichen SQL-Format (YYYY-MM-DD HH:MI:SS) | unique | false | siehe FIRST_NAME |
| | | mufm | 3 | siehe FIRST_NAME |
| VALUES | Zufälliger Wert aus einer Auswahl an Werten | values | | required - Array an möglichen Werten, darf nicht leer sein |
| FORMAT_STRING | String, der dem angegebenen regex matched | regex | | required - regex, dem der zufällige String matchen soll |
| RANDOM_STRING | Zufälliges englisches Wort | | | |
| PRIMARY_KEY | Integer ID, welche bei jedem Datensatz hochgezählt wird | nextkey | 0 | Erster zu verteilende ID |