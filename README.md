# dataset_generator

Dies ist ein Script zum Generieren von Beispiel-Datensätzen für relationale Datenbanken. Es nimmt eine json
Konfigurationsdatei entgegen und schreibt einen SQL-Befehl in eine Datei. Die json kann über eine GUI konfiguriert
werden.

## Setup

Es wird vorausgesetzt, dass Python sowie Python venv installiert ist.

```console
python -m venv generator_venv
generator_venv/bin/pip install wonderwords
generator_venv/bin/pip install Faker==40.4.0
generator_venv/bin/pip install rstr
generator_venv/bin/pip install mypy==1.18.2
generator_venv/bin/pip install tkcalendar
generator_venv/bin/pip install tkTimePicker
generator_venv/bin/pip install tkinter-tooltip
generator_venv/bin/pip install parameterized
generator_venv/bin/pip install coverage
```

### Powershell

```powershell
./install.ps1
```

### Linux

```bash
python -m venv ./generator_venv
sudo apt install python3-tk
./install.sh
```

Gehe anschließend in den Ordner generator_venv/lib/python{version}/site-packages und erstelle dort eine Datei (mit beliebigem namen) mit der Endung .pth und schreibe in diese Datei den absoluten Pfad zum src Ordner. (TODO: include in scripts)

## Usage

### GUI-Version

```console
./generator_venv/bin/activate
python src/gui_gen.py
```

Unter Powershell:

```powershell
./start.ps1
```

Unter Linux:

```bash
source generator_venv/bin/activate
python src/gui_gen.py
```

### Sonst

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

#### Options

Folgende Optionen können an den Befehl angehangen werden:

| Option | Beschreibung | Default Behavior |
| - | - | - |
| -p | json Datei, in welcher die Informationen über die Datenbank stehen. Siehe [Config](#config) | example.json |
| -f | Datei, in welche das Ergebnis als SQL-Befehl in Textformat geschrieben wird | .sql Datei mit zufällig generierten Namen |
| -a | SQL-Befehl wird an Datei angehangen. Wird von -o überschrieben | False - Existiert die Zieldatei bereits, so schlägt die Generierung fehl |
| -o | Neuer Inhalt überschreibt Inhalt der Datei, sollte die Datei bereits existieren. Überschreibt -a | False - Existiert die Zieldatei bereits, so schlägt die Generierung fehl |
| -n | Anzahl der zu generierenden Datensätze. Wenn in config json Datei angegeben, wird dieser Wert überschrieben | 20 |
| -e | Zeichencodierung für die zu erstellende Datei | utf-8 |
| -d | Spezieller SQL-Dialekt - Unterstützte Werte: PostgreSQL (p) - case insensitive, Abkürzung in Klammern | |
| --oneline | Keine Zeilenumbrüche innerhalb eines INSERT statements | False |
| -l | Location wie in [https://faker.readthedocs.io/en/master/#localization](https://faker.readthedocs.io/en/master/#localization). | de_DE |
> **-l Kann für Addressen zu Fehlern führen.**

#### Config

Die Konfiguration geschieht dabei über eine json Datei, in welcher der Name der Tabelle sowie die Art der zu
generierenden Daten festgelegt werden kann. Beispielhaft siehe example.json. Die json hat folgende Felder:

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

##### Columns

Das Columns Feld enthält die Namen der Spalten als Schlüssel und die Beschreibung des jeweiligen Datentyps als Wert.
Zum Beispiel:

```json
"feldname1": "FIRST_NAME",
"feldname2": {
    "type": "INTEGER",
    "max": 1000
}
```

Der Datentyp kann als einzelner String angegeben werden (case-insensitive), oder als Map in welcher der Typ mit dem
Schlüssel "type" vorliegt sowie weitere Parameter. Für manche Typen sind bestimmte Parameter zwangsweise notwendig.
Folgende Typen werden unterstützt:

| Typ                | Beschreibung                                                                                        | Parameter     | Default    | Beschreibung                                                                                                                                                                                                                                                                                                               |
|--------------------|-----------------------------------------------------------------------------------------------------|---------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PRIMARY_KEY        | Integer ID, welche bei jedem Datensatz hochgezählt wird                                             | nextkey       | 0          | Erster zu verteilende ID                                                                                                                                                                                                                                                                                                   |
| FOREIGN_KEY        | Integer ID, welche garantiert ein valider Wert des zugehörigen PRIMARY_KEY ist                      | column        |            | required - Name der Tabelle und Spalte, auf die dieser Fremdschlüssel verweist, im Format "tabellenname.spaltenname"; Es darf keine zirkuläre Referenz durch Fremdschlüssel entstehen                                                                                                                                      |
| FIRST_NAME         | Vorname                                                                                             | titles        | {}         | Mapping von möglichen Titeln zu entsprechenden Wahrscheinlichkeiten von 0 bis 1. Die Titel werden zufällig als Prefix angehängt                                                                                                                                                                                            |
|                    |                                                                                                     | minTitles     | 0          | Minimale Anzahl an Titeln, welche generiert werden; Darf nicht größer sein als das gegebene Mapping                                                                                                                                                                                                                        |
|                    |                                                                                                     | maxTitles     | Infinite   | Maximale Anzahl an Titeln, welche generiert werden; Darf nicht kleiner sein als minTitles                                                                                                                                                                                                                                  |
|                    |                                                                                                     | preserveOrder | true       | Gibt an, ob die Reihenfolge der Titel dieselbe wie im gegebenen Mapping sein muss                                                                                                                                                                                                                                          |
| LAST_NAME          | Nachname                                                                                            | titles        | {}         | Siehe FIRST_NAME                                                                                                                                                                                                                                                                                                           |
|                    |                                                                                                     | minTitles     | 0          | Siehe FIRST_NAME                                                                                                                                                                                                                                                                                                           |
|                    |                                                                                                     | maxTitles     | Infinite   | Siehe FIRST_NAME                                                                                                                                                                                                                                                                                                           |
|                    |                                                                                                     | preserveOrder | True       | siehe FIRST_NAME                                                                                                                                                                                                                                                                                                           |
| FULL_NAME          | Vor- und Nachname                                                                                   | titles        | {}         | siehe FIRST_NAME                                                                                                                                                                                                                                                                                                           |
|                    |                                                                                                     | minTitles     | 0          | Siehe FIRST_NAME                                                                                                                                                                                                                                                                                                           |
|                    |                                                                                                     | maxTitles     | Infinite   | Siehe FIRST_NAME                                                                                                                                                                                                                                                                                                           |
|                    |                                                                                                     | preserveOrder | True       | siehe FIRST_NAME                                                                                                                                                                                                                                                                                                           |
| COMPANY_NAME       | vollständiger Name für ein Unternehmen                                                              |               |            |                                                                                                                                                                                                                                                                                                                            |
| STREET             | Straßenname, ohne Hausnummer                                                                        |               |            |                                                                                                                                                                                                                                                                                                                            |
| STREET_HOUSENUMBER | Straßenname, mit Hausnummer                                                                         |               |            |                                                                                                                                                                                                                                                                                                                            |
| HOUSENUMBER        | Hausnummer, als String                                                                              |               |            |                                                                                                                                                                                                                                                                                                                            |
| TOWN               | Stadtname                                                                                           |               |            |                                                                                                                                                                                                                                                                                                                            |
| PLZ                | Postleitzahl, als String                                                                            |               |            |                                                                                                                                                                                                                                                                                                                            |
| MONEY              | Gleitkommazahl mit 2 Nachkommastellen                                                               | min           | 0          | Kleinster mögliche Wert (inklusiv)                                                                                                                                                                                                                                                                                         |
|                    |                                                                                                     | max           |            | required - Höchster mögliche Wert (exclusiv), muss größer als min sein                                                                                                                                                                                                                                                     |
| FLOAT              | Gleitkommazahl mit variable Anzahl Nachkommastellen                                                 | min           | 0          | Siehe MONEY                                                                                                                                                                                                                                                                                                                |
|                    |                                                                                                     | max           |            | Siehe MONEY                                                                                                                                                                                                                                                                                                                |
|                    |                                                                                                     | acc           | 100        | Angabe zu Anzahl Nachkommastellen (z. B. 100 -> 2 Nachkommastellen)                                                                                                                                                                                                                                                        |
| INTEGER            | Ganzzahl                                                                                            | min           | 0          | Siehe MONEY                                                                                                                                                                                                                                                                                                                |
|                    |                                                                                                     | max           |            | Siehe MONEY                                                                                                                                                                                                                                                                                                                |
| DATE               | Datum im üblichen SQL-Format (YYYY-MM-DD)                                                           | start         | "-99y"     | Frühestes mögliches Datum (inklusiv). Mögliche String Formate: <ul><li>"now" oder "today"</li><li>Datum im Format wie "1970-01-01" (inklusive führende nullen)</li><li>+ oder -, gefolgt von einer Zahl und d, w oder y für (day, week, year) um Abstand zum jetzigen Zeitpunkt anzugeben. Z. B. "+3y", "-5d"...</li></ul> |
|                    |                                                                                                     | end           | "now"      | Spätestes mögliches Datum (exklusiv). Format siehe start                                                                                                                                                                                                                                                                   |
| TIME               | Uhrzeit im üblichen SQL-Format (HH:MI:SS)                                                           | startTime     | "00:00:00" | Früheste mögliche Uhrzeit (inklusiv) im format "HH:MI:SS"                                                                                                                                                                                                                                                                  |
|                    |                                                                                                     | endTime       | "23:59:59" | Späteste mögliche Uhrzeit (exklusiv) entweder im Format "HH:MI:SS"                                                                                                                                                                                                                                                         |
|                    |                                                                                                     | timeRounding  | 0          | Anzahl der vollen Minuten auf die gerundet wird; Muss positiv sein und wenn größer als 60 durch 60 teilbar sein; 0 bedeutet keine Rundung                                                                                                                                                                                  |
| DATE_TIME          | Datum und Uhrzeit im üblichen SQL-Format (YYYY-MM-DD HH:MI:SS)                                      | start         | "-99y"     | siehe DATE                                                                                                                                                                                                                                                                                                                 |
|                    |                                                                                                     | end           | "now"      | siehe DATE                                                                                                                                                                                                                                                                                                                 |
|                    |                                                                                                     | startTime     | "00:00:00" | siehe TIME                                                                                                                                                                                                                                                                                                                 |
|                    |                                                                                                     | endTime       | "23:59:59" | siehe TIME                                                                                                                                                                                                                                                                                                                 |
|                    |                                                                                                     | timeRounding  | 0          | siehe TIME                                                                                                                                                                                                                                                                                                                 |
| VALUES             | Zufälliger Wert aus einer Auswahl an Werten                                                         | values        |            | required wenn import nicht gegeben - Array an möglichen Werten; darf nicht leer sein; Wiederholte Werte erhöht die Wahrscheinlichkeit entsprechend                                                                                                                                                                         |
|                    |                                                                                                     | import        |            | required wenn values nicht gegeben - zu importierende Dateien in Form eines Strings (Dateiname), eines Arrays (Liste von Dateinamen) oder eines Mappings (Dateiname zu Seperator, leerer Seperator wird zu sep)                                                                                                            |
|                    |                                                                                                     | sep           | newline    | Seperator für Werte aus importierten Dateien                                                                                                                                                                                                                                                                               |
| CYCLING_VALUES     | Geht Werte in der gegebenen zyklisch Reihenfolge durch                                              | values        |            | required wenn import nicht gegeben - Array der Werte, welche durchlaufen werden; darf nicht leer sein                                                                                                                                                                                                                      |
|                    |                                                                                                     | import        |            | siehe VALUES                                                                                                                                                                                                                                                                                                               |
|                    |                                                                                                     | sep           | newline    | siehe VALUES                                                                                                                                                                                                                                                                                                               |
| SHUFFLED_VALUES    | Zufälliger Wert aus einer Auswahl von Werten; wird erst Werte wiederholen, wenn alle gewählt wurden | values        |            | siehe VALUES                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                                                                                                                                      
|                    |                                                                                                     | import        |            | siehe VALUES                                                                                                                                                                                                                                                                                                               |
|                    |                                                                                                     | sep           | newline    | siehe VALUES                                                                                                                                                                                                                                                                                                               |
| FORMAT_STRING      | String, der dem angegebenen regex matched                                                           | regex         |            | required - regex, dem der zufällige String matchen soll                                                                                                                                                                                                                                                                    |
| RANDOM_STRING      | Zufälliges englisches Wort                                                                          |               |            |                                                                                                                                                                                                                                                                                                                            |
| COUNTING           | Integer, welcher bei jedem Datensatz hochgezählt wird                                               | nextkey       | 0          | Erster Wert                                                                                                                                                                                                                                                                                                                |

Für logisch innerhalb eines Datensatzes voneinander abhängige Spalten können die folgenden Typen verwendet werden.
Diese benötigen immer den Parameter "column", welcher der Name der Spalte ist, von dem der Wert abhängen soll:

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

Parameter, welche für den anderen Typen verfügbar sind, sind auch für diese Typen, soweit sinnvoll, verfügbar. Soll die
Spalte von einer Spalte aus einer anderen Tabelle abhängen, so muss

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

| Typ                 | referenzierter Typ | Beschreibung                                                                         | Parameter   | Default | Beschreibung                                                                                                                                                                                                                                  |
|---------------------|--------------------|--------------------------------------------------------------------------------------|-------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| LOWERTHAN_INTEGER   | INTEGER            | Ganzzahl, welche kleiner als der Wert in der verknüpften Spalte ist                  | diff        | 0       | Wert, um welchen der generierte Wert mindestens kleiner sein muss                                                                                                                                                                             |
|                     |                    |                                                                                      | maxdiff     |         | Wert, um welchen der generierte Wert höchstens kleiner sein darf                                                                                                                                                                              |
| HIGHERTHAN_INTEGER  | INTEGER            | Ganzzahl, welche größer oder gleich dem Wert in der verknüpften Spalte ist           | diff        | 0       | Wert, um welchen der generierte Wert mindestens größer sein muss                                                                                                                                                                              |
|                     |                    |                                                                                      | maxdiff     |         | Wert, um welchen der generierte Wert höchstens größer sein darf                                                                                                                                                                               |
| LOWERTHAN_FLOAT     | FLOAT              | Gleitkommazahl, welche kleiner als der Wert in der verknüpften Spalte ist            | diff        | 0       | siehe LOWERTHAN_INTEGER                                                                                                                                                                                                                       |
|                     |                    |                                                                                      | maxdiff     |         | siehe LOWERTHAN_INTEGER                                                                                                                                                                                                                       |
| HIGHERTHAN_FLOAT    | FLOAT              | Gleitkommazahl, welche größer oder gleich dem Wert in der verknüpften Spalte ist     | diff        | 0       | siehe HIGHERTHAN_INTEGER                                                                                                                                                                                                                      |
|                     |                    |                                                                                      | maxdiff     |         | siehe HIGHERTHAN_INTEGER                                                                                                                                                                                                                      |
| LOWERTHAN_DATE      | DATE, DATE_TIME    | Datum, welches vor oder gleich dem Datum der verknüpften Spalte ist                  | timeDiff    | {}      | Mapping, welches angibt um wieviel das generierte Datum mindestens kleiner sein muss. Die Schlüssel können eine beliebige Kombination aus "days", "weeks", "hours", "minutes" oder "seconds" sein und die Werte der entsprechende Unterschied |
|                     |                    |                                                                                      | timeMaxdiff |         | Mapping, welches angibt um wieviel das generierte Datum maximal kleiner sein darf, siehe timeDiff                                                                                                                                             |
| HIGHERTHAN_DATE     | DATE, DATE_TIME    | Datum, welches nach oder gleich dem Datum der verknüpften Spalte ist                 | timeDiff    | {}      | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
|                     |                    |                                                                                      | timeMaxdiff |         | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
| LOWERTHAN_TIME      | TIME, DATE_TIME    | Uhrzeit, welche vor oder gleich der Uhrzeit der verknüpften Spalte ist               | timeDiff    | {}      | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
|                     |                    |                                                                                      | timeMaxdiff |         | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
| HIGHERTHAN_TIME     | TIME, DATE_TIME    | Uhrzeit, welche nach vor oder gleich der Uhrzeit der verknüpften Spalte ist          | timeDiff    | {}      | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
|                     |                    |                                                                                      | timeMaxdiff |         | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
| LOWERTHAN_DATETIME  | DATE_TIME, DATE    | Datum mit Uhrzeit, welches vor oder gleich dem Zeitpunkt der verknüpften Spalte ist  | timeDiff    | {}      | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
|                     |                    |                                                                                      | timeMaxdiff |         | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
| HIGHERTHAN_DATETIME | DATE_TIME, DATE    | Datum mit Uhrzeit, welches nach oder gleich dem Zeitpunkt der verknüpften Spalte ist | timeDiff    | {}      | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |
|                     |                    |                                                                                      | timeMaxdiff |         | siehe LOWERTHAN_DATE                                                                                                                                                                                                                          |

## Code

Der Code liegt im src Ordner und ist dort weiter unterteilt. Die auf der obersten Ebene liegenden Dateien sind die
ausführbaren Dateien dataset_gen.py und gui_gen.py sowie die typeCheck.py, welche striktere Typisierung sicherstellt.
Der Programmcode ist außerdem in backend und frontend (gui) unterteilt. Der enums Ordner enthält Enumerationstypen und
der exceptions Ordner verwendetet custom Exceptions, welche jeweils sowohl vom frontend als auch vom backend verwendet
werden könnten.

### dataset_gen.py

Die dataset_gen.py dient zur Nutzung ohne GUI, also mittels einer .json Konfigurationsdatei. Es hängt in keiner Form
vom frontend ab und nutzt lediglich die API des backends.

### gui_gen.py

Die gui_gen.py ruft lediglich das frontend auf, dient also zum Öffnen des Programms via GUI.

### typeCheck.py

Dient zur strikten Typisierung und prüft diese mittels mypy und schließt das Programm vorzeitig bei Fehlern.

### deprecated.py

Enthält einen decorator, um funktionen als deprecated zu markieren und eine Warnung auszugeben, wenn die Funktion noch
verwendet wird.

### backend

Die grobe Struktur des backends besteht aus dem TableModel, welches eine Datenbanktabelle repräsentiert, während die
Spalten durch Column dargestellt werden. Die Zufallsgeneration von Daten mittels Faker, wonderwords und xeger passiert in
addressGenerator, nameGenerator und numbersGenerator. Die Logik, inklusive der Erstellung der TableModel, passiert in
backend_api.py, welche zudem die Schnittstelle, welche vom frontend bzw. dataset_gen.py genutzt wird, bereitstellt. Für
Details siehe die jeweiligen Klassen/Dateien.

### gui

Die GUI ist mit tkinter gebaut und benutzt als Geometry Manager teilweise grid und teilweise pack. Auf der obersten
Ebene ist App, welche zudem in gui_gen.py verwendet wird. Darin verschachtelt sind die Frames TableFrame und
ColumnFrame, welche je Tabellen und ihre Spalten darstellen. In columnDetails.py sind alle verfügbaren Datentypen und
ihre Parameter hinterlegt. Zudem stehen mit ColumnEntry, DatetimeEntry, LabelWithExtras, ListEntry und TimeDictEntry
custom Widgets bereit. Für Details siehe die jeweiligen Klassen/Dateien.

