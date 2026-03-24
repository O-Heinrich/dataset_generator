from enums.datatypes import Datatype as Dt
from typing import Self, Any
from gui.timeDict import TimeDict
from enums.inputType import InputType as It
from datetime import date, time, timedelta

class ParameterDetails:
    def __init__(self, name: str, typ: It=It.STRING, required: bool=False, default: Any=None, description: str="") -> None:
        self.name: str = name
        self.typ: It = typ
        self.required: bool = required
        self.default: Any = default
        self.description: str = description

class ColumnDetails:
    def __init__(self, dt: Dt, parameters: dict[str, ParameterDetails]={}, subtypes: dict[str, Self]={}) -> None:
        self.type: Dt = dt
        self.parameters: dict[str, ParameterDetails] = parameters
        self.subtypes: dict[str, Self] = subtypes

timerounding_desc: str = "Anzahl der vollen Minuten\nauf die gerundet wird.\nMuss positiv sein und wenn\ngrößer als 60 durch 60 teilbar\nsein. 0 bedeutet keine Rundung"
othercolumn_desc: str = "Name der Spalte, von der\ndiese Spalte abhängen soll."
fk_desc: str = "Name des Schlüssels der\nanderen Tabelle. Optional wenn\ndie andere Spalte in\nderselben Tabelle ist."

allTypes: dict[str, ColumnDetails] = {
    "Primärschlüssel": ColumnDetails(Dt.PRIMARY_KEY, {"Nächste ID": ParameterDetails("nextkey", typ=It.INTEGER, default=0, description="Erster generierter Schlüssel")}),
    "Fremdschlüssel": ColumnDetails(Dt.FOREIGN_KEY, {"Primärschlüssel Spalte": ParameterDetails("column", typ=It.TABLE_KEY, required=True, description="Schlüsselspalte, auf auf\nwelche verwiesen werden soll")}),
    "Vorname": ColumnDetails(Dt.FIRST_NAME),
    "Nachname": ColumnDetails(Dt.LAST_NAME),
    "Voller Name": ColumnDetails(Dt.FULL_NAME),
    "Firmenname": ColumnDetails(Dt.COMPANY_NAME),
    "Straße": ColumnDetails(Dt.STREET),
    "Hausnummer": ColumnDetails(Dt.HOUSENUMBER),
    "Straße und Hausnummer": ColumnDetails(Dt.STREET_HOUSENUMBER),
    "Stadt": ColumnDetails(Dt.TOWN),
    "Postleitzahl": ColumnDetails(Dt.PLZ),
    "Geld": ColumnDetails(Dt.MONEY, {
        "Minimum": ParameterDetails("min", typ=It.FLOAT, default=0),
        "Maximum": ParameterDetails("max", typ=It.FLOAT, required=True)
    }),
    "Ganzzahl": ColumnDetails(Dt.INTEGER, {
        "Minimum": ParameterDetails("min", typ=It.INTEGER, default=0),
        "Maximum": ParameterDetails("max", typ=It.INTEGER, required=True)
    }, subtypes={
        "Kleinere Ganzzahl": ColumnDetails(Dt.LOWERTHAN_INTEGER, {
            "Andere Spalte": ParameterDetails("column", typ=It.TABLE_COLUMN, required=True, description=othercolumn_desc),
            "Fremdschlüssel": ParameterDetails("fk", typ=It.TABLE_KEY, description=fk_desc),
            "Minimaler Unterschied": ParameterDetails("diff", typ=It.INTEGER, default=0),
            "Maximaler Unterschied": ParameterDetails("maxdiff", typ=It.INTEGER)
        }),
        "Größere Ganzzahl": ColumnDetails(Dt.HIGHERTHAN_INTEGER, {
            "Andere Spalte": ParameterDetails("column", typ=It.TABLE_COLUMN, required=True, description=othercolumn_desc),
            "Fremdschlüssel": ParameterDetails("fk", typ=It.TABLE_KEY, description=fk_desc),
            "Minimaler Unterschied": ParameterDetails("diff", typ=It.INTEGER, default=0),
            "Maximaler Unterschied": ParameterDetails("maxdiff", typ=It.INTEGER)
        })
    }),
    "Kommazahl": ColumnDetails(Dt.FLOAT, {
        "Minimum": ParameterDetails("min", typ=It.FLOAT, default=0),
        "Maximum": ParameterDetails("max", typ=It.FLOAT, required=True),
        "Genauigkeit": ParameterDetails("acc", typ=It.FLOAT, default=100, description="Angabe zu Anzahl Nachkommastellen\n(z. B. 100 -> 2 Nachkommastellen)")
    }, subtypes={
        "Kleinere Ganzzahl": ColumnDetails(Dt.LOWERTHAN_FLOAT, {
            "Andere Spalte": ParameterDetails("column", typ=It.TABLE_COLUMN, required=True, description=othercolumn_desc),
            "Fremdschlüssel": ParameterDetails("fk", typ=It.TABLE_KEY, description=fk_desc),
            "Minimaler Unterschied": ParameterDetails("diff", typ=It.FLOAT, default=0),
            "Maximaler Unterschied": ParameterDetails("maxdiff", typ=It.FLOAT)
        }),
        "Größere Ganzzahl": ColumnDetails(Dt.HIGHERTHAN_FLOAT, {
            "Andere Spalte": ParameterDetails("column", typ=It.TABLE_COLUMN, required=True, description=othercolumn_desc),
            "Fremdschlüssel": ParameterDetails("fk", typ=It.TABLE_KEY, description=fk_desc),
            "Minimaler Unterschied": ParameterDetails("diff", typ=It.FLOAT, default=0),
            "Maximaler Unterschied": ParameterDetails("maxdiff", typ=It.FLOAT)
        })
    }),
    "Datum": ColumnDetails(Dt.DATE, {
        "Startdatum": ParameterDetails("start", typ=It.DATE, default=date.today() - timedelta(days=36525)),
        "Enddatum": ParameterDetails("end", typ=It.DATE, default=date.today())
    }, subtypes={
        "Früheres Datum": ColumnDetails(Dt.LOWERTHAN_INTEGER, {
            "Andere Spalte": ParameterDetails("column", typ=It.TABLE_COLUMN, required=True, description=othercolumn_desc),
            "Fremdschlüssel": ParameterDetails("fk", typ=It.TABLE_KEY, description=fk_desc),
            "Minimaler Unterschied": ParameterDetails("timeDiff", typ=It.TIMEDICT, default=TimeDict()),
            "Maximaler Unterschied": ParameterDetails("timeMaxdiff", typ=It.TIMEDICT)
        }),
        "Späteres Datum": ColumnDetails(Dt.HIGHERTHAN_INTEGER, {
            "Andere Spalte": ParameterDetails("column", typ=It.TABLE_COLUMN, required=True, description=othercolumn_desc),
            "Fremdschlüssel": ParameterDetails("fk", typ=It.TABLE_KEY, description=fk_desc),
            "Minimaler Unterschied": ParameterDetails("timeDiff", typ=It.TIMEDICT, default=TimeDict()),
            "Maximaler Unterschied": ParameterDetails("timeMaxdiff", typ=It.TIMEDICT)
        })
    }),
    "Uhrzeit": ColumnDetails(Dt.TIME, {
        "Startzeit": ParameterDetails("startTime", typ=It.TIME, default=time(hour=0, minute=0)),
        "Endzeit": ParameterDetails("endTime", typ=It.TIME, default=time(hour=23, minute=59)),
        "Rundung": ParameterDetails("timeRounding", typ=It.INTEGER, default=0, description=timerounding_desc)
    }),
    "Datum und Uhrzeit": ColumnDetails(Dt.DATE_TIME, {
        "Startdatum": ParameterDetails("start", typ=It.DATE, default=date.today() - timedelta(days=36525)),
        "Enddatum": ParameterDetails("end", typ=It.DATE, default=date.today()),
        "Startzeit": ParameterDetails("startTime", typ=It.TIME, default=time(hour=0, minute=0)),
        "Endzeit": ParameterDetails("endTime", typ=It.TIME, default=time(hour=23, minute=59)),
        "Rundung": ParameterDetails("timeRounding", typ=It.INTEGER, default=0, description=timerounding_desc)
    }),
    "Werteliste": ColumnDetails(Dt.VALUES, {"Mögliche Werte": ParameterDetails("values", typ=It.LIST_STRING, required=True)}),
    "Regex": ColumnDetails(Dt.FORMAT_STRING, {"Regex": ParameterDetails("regex", required=True, description="Regulärer Ausdruck, welchem\nder generierte String matchen soll")}),
    "Wort": ColumnDetails(Dt.RANDOM_STRING)
}