# dataset_generator

Dies ist ein Script zum Generieren von Beispiel-Datensätzen für relationale Datenbanken. Es nimmt eine json Konfigurationsdatei entgegen und schreibt einen SQL-Befehl in eine Datei.

## Setup

Es wird vorrausgesetzt, dass Python sowie Python venv installiert ist.

```console
python -m venv generator_venv
generator_venv/bin/pip install wonderwords
generator_venv/bin/pip install Faker
generator_venv/bin/pip install rstr
```

### Linux

```bash
python3 -m venv generator_venv
source generator_venv/bin/activate
generator_venv/bin/pip install wonderwords
generator_venv/bin/pip install Faker
generator_venv/bin/pip install rstr
```

### Powershell

```powershell
python -m venv generator_venv
./generator_venv/bin/Activate.ps1
generator_venv/bin/pip install wonderwords
generator_venv/bin/pip install Faker
generator_venv/bin/pip install rstr
```

## Usage

Wenn noch nicht geschehen muss die virtuelle environment aktiviert werden:

```console
./generator_venv/bin/activate
```

Beziehungsweise unter Powershell:

```powershell
./generator_venv/bin/Activate.ps1
```

Das script kann mit folgendem Befehl ausgeführt werden:

```console
python src/dataset_gen.py
```

### Options

Folgende Optionen können an den Befehl angehangen werden:

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

Die Konfiguration geschieht dabei über eine json Datei, in welcher der Name der Tabelle sowie die Art der zu generierenden Daten festgelegt werden kann. Beispielhaft siehe example.json. Die json hat folgende Felder:

| Feldname | Typ | | Beschreibung |
| - | - | - | - |
| db_name | String | required | Name der Tabelle |
| columns | Map | required | Repräsentation der Spalten der Tabelle und ihrer Typen. Siehe [Columns](#columns) |
| amount | int | optional | Anzahl der für diese Tabelle zu generierenden Datensätze. Überschreibt die -n Option |

Zum Beispiel:

```json
{
    "db_name": "tabelle",
    "columns": {
        "feldname1": "FULL_NAME",
        "feldname2": {
            "type": "INTEGER",
            "max": 10000
        }
    },
    "amount": 1000
}
```

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
| PRIMARY_KEY | Integer ID, welche bei jedem Datensatz hochgezählt wird | nextkey | 0 | Erster zu verteilende ID |
| FIRST_NAME | Vorname mit evtl Titel | | | |
| LAST_NAME | Nachname | | | |
| FULL_NAME | Vor- und Nachname | | | |
| COMPANY_NAME | vollständiger Name für ein Unternehmen | | | |
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
| DATE | Datum im üblichen SQL-Format (YYYY-MM-DD) | start | "-99y" | Frühestes mögliches Datum (inklusiv). Mögliche String Formate: <ul><li>"now" oder "today"</li><li>Datum im Format wie "1970-01-01" (inklusive führende nullen)</li><li>+ oder -, gefolgt von einer Zahl und d, w oder y für (day, week, year) um Abstand zum jetzigen Zeitpunkt anzugeben. Z. B. "+3y", "-5d"...</li></ul> |
| | | end | "now" | Spätestes mögliches Datum (exklusiv). Format siehe start |
| TIME | Uhrzeit im üblichen SQL-Format (HH:MI:SS) | | | |
| DATE_TIME | Datum und Uhrzeit im üblichen SQL-Format (YYYY-MM-DD HH:MI:SS) | | | |
| VALUES | Zufälliger Wert aus einer Auswahl an Werten | values | | required - Array an möglichen Werten, darf nicht leer sein. Wiederholte Werte erhöht die Wahrscheinlichkeit entsprechend |
| FORMAT_STRING | String, der dem angegebenen regex matched | regex | | required - regex, dem der zufällige String matchen soll |
| RANDOM_STRING | Zufälliges englisches Wort | | | |

Für logisch voneinander abhängige Spalten können die folgenden Typen verwendet werden. Die Benennung dieser Typen ist egal, und es wird immer eine map als Wert benötigt, welche immer den Typen ("type") und eine Liste der Spaltennamen ("names") enthält. Zum Beispiel:

```json
"xxx": {
    "type": "ASCENDING",
    "names": ["feld1", "feld2", "feld3"]
}
```

| Typ | Beschreibung | Parameter | Default | Beschreibung |
| - | - | - | - | - |
| ASCENDING | Generiert zufällige Werte und garantiert, dass diese aufsteigend (nicht strikt aufsteigend) sind | alltype | | required - Typ, von welchem die einzelnen Felder sind. Alle Felder erhalten denselben Typ. Zurzeit unterstützt: "DATE" |
| | | reverse | false | Wenn true, werden die Felder absteigend statt aufsteigend generiert |
| | | start | "-99y" | siehe Date |
| | | end | "now" | siehe Date |