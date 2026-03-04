# dataset_generator

Dies ist ein Script zum Generieren von Beispiel-Datensätzen für relationale Datenbanken. Es nimmt eine json Konfigurationsdatei entgegen und schreibt einen SQL-Befehl in eine Datei.

## Setup

Es wird vorausgesetzt, dass Python sowie Python venv installiert ist.

```console
python -m venv generator_venv
generator_venv/bin/pip install wonderwords
generator_venv/bin/pip install Faker
generator_venv/bin/pip install rstr
generator_venv/bin/pip install mypy==1.18.2
```

### Linux

```bash
python3 -m venv generator_venv
source generator_venv/bin/activate
generator_venv/bin/pip install wonderwords
generator_venv/bin/pip install Faker
generator_venv/bin/pip install rstr
generator_venv/bin/pip install mypy==1.18.2
```

### Powershell

```powershell
python -m venv generator_venv
./generator_venv/bin/Activate.ps1
generator_venv/bin/pip install wonderwords
generator_venv/bin/pip install Faker
generator_venv/bin/pip install rstr
generator_venv/bin/pip install mypy==1.18.2
```

## Usage

Wenn noch nicht geschehen muss die virtuelle environment aktiviert werden:

```console
./generator_venv/bin/activate
```

Unter Powershell:

```powershell
./generator_venv/bin/Activate.ps1
```

Unter Linux:

```bash
source generator_venv/bin/activate
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
| -d | Spezieller SQL-Dialekt - Unterstützte Werte: PostgreSQL (p) - case insensitive, Abkürzung in Klammern | |
| -l | Location wie in [https://faker.readthedocs.io/en/master/#localization](https://faker.readthedocs.io/en/master/#localization). | de_DE |
> **-l Kann für Addressen zu Fehlern führen.**

### Config

Die Konfiguration geschieht dabei über eine json Datei, in welcher der Name der Tabelle sowie die Art der zu generierenden Daten festgelegt werden kann. Beispielhaft siehe example.json. Die json hat folgende Felder:

| Feldname | Typ | | Beschreibung |
| - | - | - | - |
| table | String | required | Name der Tabelle |
| columns | Map | required | Repräsentation der Spalten der Tabelle und ihrer Typen. Siehe [Columns](#columns) |
| amount | int | optional | Anzahl der für diese Tabelle zu generierenden Datensätze. Überschreibt die -n Option |

Zum Beispiel:

```json
{
    "table": "tabelle",
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

Alternativ kann eine Liste von Tabellen angegeben werden, um Daten für mehrere Tabellen zu generieren:

```json
[
    {
        "table": "tabelle",
        "columns": {
            "id": "PRIMARY_KEY",
            "feld": "FIRST_NAME"
        },
        "amount": 1000
    },
    {
        "table": "tabelle2",
        "columns": {
            "id": "PRIMARY_KEY",
            "feld": "LAST_NAME"
        }
    }
]
```

Die Tabellennamen dürfen sich hier nicht wiederholen.

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
| FOREIGN_KEY | Integer ID, welche garantiert ein valider Wert des zugehörigen PRIMARY_KEY ist | column | | required - Name der Tabelle und Spalte, auf die dieser Fremdschlüssel verweist, im Format "tabellenname.spaltenname"; Die andere Tabelle muss zuvor definiert worden sein |
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
| TIME | Uhrzeit im üblichen SQL-Format (HH:MI:SS) | startTime | "00:00:00" | Früheste mögliche Uhrzeit (inklusiv) im format "HH:MI:SS" |
| | | endTime | "23:59:59" | Späteste mögliche Uhrzeit (exklusiv) entweder im Format "HH:MI:SS" |
| | | timeRounding | 0 | Anzahl der vollen Minuten auf die gerundet wird. Muss positiv sein und wenn größer als 60 durch 60 teilbar sein. 0 bedeutet keine Rundung |
| DATE_TIME | Datum und Uhrzeit im üblichen SQL-Format (YYYY-MM-DD HH:MI:SS) | start | "-99y" | siehe DATE |
| | | end | "now" | siehe DATE |
| | | startTime | "00:00:00" | siehe TIME |
| | | endTime | "23:59:59" | siehe TIME |
| | | timeRounding | 0 | siehe TIME |
| VALUES | Zufälliger Wert aus einer Auswahl an Werten | values | | required - Array an möglichen Werten, darf nicht leer sein. Wiederholte Werte erhöht die Wahrscheinlichkeit entsprechend |
| FORMAT_STRING | String, der dem angegebenen regex matched | regex | | required - regex, dem der zufällige String matchen soll |
| RANDOM_STRING | Zufälliges englisches Wort | | | |

Für logisch innerhalb einres Datensatzes voneinander abhängige Spalten können die folgenden Typen verwendet werden. Diese benötigen immer den Parameter "column", welcher der Name der Spalte ist, von dem der Wert abhängen soll:

```json
"someint": {
    "type": "INTEGER",
    "max": 100
},
"lowerint": {
    "type": "LOWERTHAN_INTEGER",
    "column": "someint",
    "max": 100
}
```

Parameter, welche für den anderen Typen verfügbar sind, sind auch für diese Typen, soweit sinnvoll, verfügbar. Soll die Spalte von einer Spalte aus einer anderen Tabelle abhängen, so muss
- ein FOREIGN_KEY vorhanden sein
- der Parameter fk vorhanden sein, welcher equivalent zum "column" Parameter des FOREIGN_KEY ist
- der column Parameter die Form "andereTabelle.andereSpalte" haben

```json
[
    {
        "table": "table1",
        "columns": {
            "id": "PRIMARY_KEY",
            "someint": {
                "type": "INTEGER",
                "max": 100
            }
        }
    },
    {
        "table": "table2",
        "columns": {
            "foreignkey": {
                "type": "FOREIGN_KEY",
                "column": "table1.id"
            },
            "lowerint": {
                "type": "LOWERTHAN_INTEGER",
                "column": "table1.someint",
                "fk": "table1.id",
                "max": 100
            }
        }
    }
]
```

Folgende Typen werden unterstützt:

| Typ | referenzierter Typ | Beschreibung | Parameter | Default | Beschreibung |
| - | - | - | - | - | - |
| LOWERTHAN_INTEGER | INTEGER | Ganzzahl, welche kleiner als der Wert in der verknüpften Spalte ist | diff | 0 | Wert, um welchen der generierte Wert mindestens kleiner sein muss |
| | | maxdiff | | Wert, um welchen der generierte Wert höchstens kleiner sein darf |
| HIGHERTHAN_INTEGER | INTEGER | Ganzzahl, welche größer oder gleich dem Wert in der verknüpften Spalte ist | diff | 0 | Wert, um welchen der generierte Wert mindestens größer sein muss |
| | | maxdiff | | Wert, um welchen der generierte Wert höchstens größer sein darf |
| LOWERTHAN_FLOAT | FLOAT | Gleitkommazahl, welche kleiner als der Wert in der verknüpften Spalte ist | diff | 0 | siehe LOWERTHAN_INTEGER |
| | | maxdiff | | siehe LOWERTHAN_INTEGER |
| HIGHERTHAN_FLOAT | FLOAT | Gleitkommazahl, welche größer oder gleich dem Wert in der verknüpften Spalte ist | diff | 0 | siehe HIGHERTHAN_INTEGER |
| | | maxdiff | | siehe HIGHERTHAN_INTEGER |
| LOWERTHAN_DATE | DATE | Datum, welches vor oder gleich dem Datum der verknüpften Spalte ist | timeDiff | {} |  Mapping, welches angibt um wieviel das generierte Datum mindestens kleiner sein muss. Die Schlüssel können eine beliebige Kombination aus "days", "weeks", "hours", "minutes" oder "seconds" sein und die Werte der entsprechende Unterschied |
| | | timeMaxdiff | | Mapping, welches angibt um wieviel das generierte Datum maximal kleiner sein darf, siehe timeDiff |
| HIGHERTHAN_DATE | DATE | Datum, welches nach oder gleich dem Datum der verknüpften Spalte ist | timeDiff | {} | siehe LOWERTHAN_DATE |
| | | timeMaxdiff | | siehe LOWERTHAN_DATE |