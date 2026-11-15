<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.7 Datenpunkte

## 4.7 DataPoints

### Überblick

| Eigenschaft             | Wert                                                       |
| ----------------------- | ---------------------------------------------------------- |
| **Capability-ID**       | `ruml:datapoints`                                          |
| **Scope**               | Root-Level (`payload.data` des `ruml:datapoints`-Eintrags) |
| **Standard `required`** | `false`                                                    |
| **Rolle**               | `data`                                                     |

DataPoints definieren die strukturierten Daten, die für Entscheidungen in der Rulemap benötigt
werden. Sie beschreiben das **Schema** der Daten (Name, Typ, Validierung) sowie einen
**Binding-Hint**, der angibt, wie die Daten bezogen werden sollen.

### Grundprinzip: Schema-First

RUML folgt dem Schema-First-Prinzip:

- **In der RUML-Datei:** Nur die Datendefinition (Was wird benötigt?)
- **Zur Laufzeit:** Die tatsächlichen Werte werden vom Tool bereitgestellt

### Einbettung über die `ruml:datapoints`-Capability

DataPoints werden im `data`-Objekt der `ruml:datapoints`-Capability im Root-`capabilities`-Array
definiert. Wiederverwendbare strukturierte Typen werden daneben in einem optionalen `sets`-Objekt
deklariert (siehe [4.7.4](#474-sets-wiederverwendbare-strukturierte-typen)):

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "sets": {
          "set_person": {/* ... */},
          "set_beschaeftigung": {/* ... */}
        },
        "data": {
          "dp_annual_income": {/* ... */},
          "dp_credit_score": {/* ... */}
        }
      }
    }
  ],
  "metadata": {/* ... */},
  "rulemap": {/* ... */}
}
```

**Hinweis:** Bei Map-Strukturen wie `data` dient der Object-Key (z.B. `"dp_annual_income"`) als
eindeutiger Identifikator. Ein separates `id`-Feld ist daher nicht erforderlich (siehe
[Kapitel 3.2.6](../03-data-model/3-2-data-types-and-formats.md) – Designprinzip "Key = ID").

**Hinweis zur Nutzung durch andere Capabilities:** DataPoints definieren ausschließlich das
Datenschema und die Beschaffung. Die gesammelten Daten stehen anderen Capabilities als Grundlage zur
Verfügung — z.B. `ruml:query` für Berechnungen und Auswertungen (siehe
[Kapitel 4.8](4-8-ruml-query.md)) oder `ruml:ai-query` für KI-gestützte Entscheidungen (siehe
[Kapitel 4.9](4-9-ruml-ai-query.md)).

### Grundstruktur

```jsonc
"dp_annual_income": {
  "name": "Jahreseinkommen",
  "description": "Brutto-Jahreseinkommen des Antragstellers",
  "type": "currency",
  "unit": "EUR",
  "validation": {
    "required": true,
    "min": 0,
    "max": 10000000
  },
  "binding": {
    "type": "input"
  }
}
```

### Pflichtfelder

| **Feld**  | **Typ** | **Beschreibung**                                                                              |
| --------- | ------- | --------------------------------------------------------------------------------------------- |
| `name`    | String  | MUSS einen Anzeigenamen enthalten ([`DP-01`](../08-validation/index.md#rule-dp-01))                                              |
| `type`    | Enum    | MUSS einen der definierten Datentypen angeben (siehe [4.7.1](#471-datentypen)) ([`DP-01`](../08-validation/index.md#rule-dp-01)) |
| `binding` | Object  | MUSS angeben, wie die Daten bezogen werden (siehe [4.7.2](#472-binding-typen)) ([`DP-01`](../08-validation/index.md#rule-dp-01)) |

**Hinweis:** Der Object-Key dient als eindeutige ID des DataPoints. Er MUSS dem Muster
`[a-z_][a-z0-9_]*` entsprechen ([`DP-02`](../08-validation/index.md#rule-dp-02)).

### Optionale Felder

| **Feld**      | **Typ** | **Beschreibung**                                                                                                                                                                                                                                                                                 |
| ------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `description` | String  | DARF eine ausführliche Beschreibung enthalten ([`DP-03`](../08-validation/index.md#rule-dp-03))                                                                                                                                                                                                                                     |
| `unit`        | String  | **MUSS** bei `type: "currency"` vorhanden sein; DARF bei `type: "number"` und `type: "percentage"` vorhanden sein (z.B. `"EUR"`, `"kg"`, `"%"`) ([`DP-03`](../08-validation/index.md#rule-dp-03), [`DP-05`](../08-validation/index.md#rule-dp-05)). DARF bei anderen Typen NICHT verwendet werden ([`DP-04`](../08-validation/index.md#rule-dp-04)).                                                      |
| `format`      | String  | DARF den Typ bei `location` (siehe [Location-Typ](#location-typ)), `identifier` (siehe [Identifier-Typ](#identifier-typ)) oder `address` (siehe [Address-Typ](#address-typ)) verfeinern ([`DP-03`](../08-validation/index.md#rule-dp-03)). DARF bei anderen Typen NICHT verwendet werden ([`DP-04`](../08-validation/index.md#rule-dp-04)).                            |
| `options`     | Array   | **MUSS** bei `type: "enum"` vorhanden und nicht leer sein — die erlaubten Werte (siehe [Enum-Typ](#enum-typ)) ([`DP-06`](../08-validation/index.md#rule-dp-06)). DARF bei anderen Typen NICHT verwendet werden ([`DP-04`](../08-validation/index.md#rule-dp-04)).                                                                                                      |
| `validation`  | Object  | DARF Validierungsregeln enthalten (siehe [4.7.3](#473-validierung)) ([`DP-03`](../08-validation/index.md#rule-dp-03))                                                                                                                                                                                                               |
| `sensitive`   | Boolean | DARF angeben, ob es sich um sensible Daten handelt. Standard: `false` ([`DP-03`](../08-validation/index.md#rule-dp-03))                                                                                                                                                                                                             |
| `set`         | String  | **MUSS** bei `type: "object"` vorhanden sein — die ID des Set-Typs in `sets` (siehe [4.7.4](#474-sets-wiederverwendbare-strukturierte-typen)) ([`DP-07`](../08-validation/index.md#rule-dp-07)). DARF bei anderen Typen NICHT verwendet werden ([`DP-04`](../08-validation/index.md#rule-dp-04)).                                                                      |
| `cardinality` | Object  | DARF bei `type: "object"` vorhanden sein — `{ "min": Integer, "max": Integer }` für Wiederholung; `min` MUSS mindestens 0 und `max` mindestens 1 sein ([`DP-08`](../08-validation/index.md#rule-dp-08)). Ohne Angabe = eine Instanz; `max > 1` = Liste von Instanzen. DARF bei anderen Typen NICHT verwendet werden ([`DP-04`](../08-validation/index.md#rule-dp-04)). |

### 4.7.1 Datentypen

Das Feld `type` eines DataPoints definiert den erwarteten Datentyp. RUML unterscheidet zwischen
primitiven und spezialisierten Datentypen.

### Primitive Typen

| **Typ**    | **Beschreibung**                | **Beispielwert**         |
| ---------- | ------------------------------- | ------------------------ |
| `string`   | Text                            | `"Max Mustermann"`       |
| `number`   | Zahl (Integer oder Dezimal)     | `50000`, `3.14`          |
| `boolean`  | Wahrheitswert                   | `true`, `false`          |
| `date`     | Datum ohne Zeitangabe           | `"2024-01-01"`           |
| `datetime` | Datum mit Zeitangabe            | `"2024-01-01T10:00:00Z"` |
| `time`     | Uhrzeit ohne Datum              | `"14:30:00"`             |
| `integer`  | Ganzzahl (positiv oder negativ) | `42`, `-7`               |

### Spezialisierte Typen

| **Typ**      | **Beschreibung**                              | **Format**                                                                                                                         | **Beispielwert**                                      |
| ------------ | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `currency`   | Währungsbetrag                                | Zahl, Einheit über `unit`                                                                                                          | `50000` (mit `"unit": "EUR"`)                         |
| `percentage` | Prozentsatz                                   | Zahl zwischen 0 und 100                                                                                                            | `32.5`                                                |
| `duration`   | Zeitdauer                                     | ISO 8601 Duration                                                                                                                  | `"P2Y3M"` (2 Jahre, 3 Monate)                         |
| `email`      | E-Mail-Adresse                                | RFC 5322                                                                                                                           | `"max@example.com"`                                   |
| `phone`      | Telefonnummer                                 | E.164                                                                                                                              | `"+491234567890"`                                     |
| `location`   | Geografischer Ort                             | Siehe Location-Formate                                                                                                             | `"DE"`, `"DE-BY"`, `"80331"`                          |
| `identifier` | Offizielle Kennung                            | String mit `format`-Hint                                                                                                           | `"DE123456789"` (USt-ID)                              |
| `iban`       | Bankverbindung                                | ISO 13616                                                                                                                          | `"DE89370400440532013000"`                            |
| `count`      | Anzahl/Menge                                  | Nicht-negative Ganzzahl                                                                                                            | `3`                                                   |
| `url`        | URL/URI                                       | RFC 3986                                                                                                                           | `"https://example.com/bescheid/123"`                  |
| `address`    | Strukturierte Postadresse                     | Siehe Address-Formate                                                                                                              | `{"street": "Musterstr. 1", ...}`                     |
| `enum`       | Auswahl aus Werteliste                        | Wert aus `options`                                                                                                                 | `"married"`                                           |
| `object`     | Instanz eines wiederverwendbaren **Set**-Typs | Referenziert ein `set`; kann über `cardinality` wiederholt werden (siehe [4.7.4](#474-sets-wiederverwendbare-strukturierte-typen)) | `{ "dp_vorname": "Eva", "dp_nachname": "Schneider" }` |

### Location-Typ

Der Typ `location` ermöglicht die Angabe geografischer Orte auf verschiedenen Ebenen. Das optionale
Feld `format`spezifiziert die erwartete Granularität:

| **Format**     | **Beschreibung**                   | **Beispielwert**          |
| -------------- | ---------------------------------- | ------------------------- |
| `country`      | Land (ISO 3166-1 alpha-2)          | `"DE"`, `"AT"`, `"CH"`    |
| `region`       | Land mit Unterteilung (ISO 3166-2) | `"DE-BY"`, `"AT-9"`       |
| `union`        | Staatenverbund                     | `"EU"`, `"EFTA"`, `"EWR"` |
| `postal`       | Postleitzahl                       | `"80331"`, `"1010"`       |
| `municipality` | Gemeindeschlüssel                  | `"09162000"` (München)    |
| `coordinates`  | GPS-Koordinaten                    | `"48.1351,11.5820"`       |

**Beispiel:**

```jsonc
"dp_residence": {
  "name": "Wohnsitz",
  "description": "Land des Hauptwohnsitzes",
  "type": "location",
  "format": "country",
  "validation": {
    "required": true,
    "enum": ["DE", "AT", "CH"]
  },
  "binding": {
    "type": "input"
  }
}
```

```jsonc
"dp_jurisdiction": {
  "name": "Rechtsraum",
  "description": "Anwendbarer Rechtsraum",
  "type": "location",
  "format": "union",
  "validation": {
    "enum": ["EU", "EWR", "EFTA"]
  },
  "binding": {
    "type": "input"
  }
}
```

### Address-Typ

Der Typ `address` ermöglicht die Angabe strukturierter Postadressen. Das optionale Feld `format`
spezifiziert den erwarteten Detailgrad:

| **Feld**     | **Typ** | **Beschreibung**               |
| ------------ | ------- | ------------------------------ |
| `street`     | String  | Straße und Hausnummer          |
| `postalCode` | String  | Postleitzahl                   |
| `city`       | String  | Ort                            |
| `region`     | String  | Bundesland/Kanton (ISO 3166-2) |
| `country`    | String  | Land (ISO 3166-1 alpha-2)      |

**Beispiel:**

```jsonc
"dp_residence_address": {
  "name": "Wohnadresse",
  "description": "Hauptwohnsitz des Antragstellers",
  "type": "address",
  "validation": {
    "required": true
  },
  "binding": {
    "type": "input"
  }
}
```

### Identifier-Typ

Der Typ `identifier` wird für offizielle Kennungen verwendet. Das Feld `format` SOLLTE die Art der
Kennung spezifizieren:

| **Format**       | **Beschreibung**            | **Beispielwert** |
| ---------------- | --------------------------- | ---------------- |
| `taxId`          | Steueridentifikationsnummer | `"12345678901"`  |
| `vatId`          | Umsatzsteuer-ID             | `"DE123456789"`  |
| `socialSecurity` | Sozialversicherungsnummer   | `"12345678A123"` |
| `passport`       | Reisepassnummer             | `"C01X00T47"`    |
| `nationalId`     | Personalausweisnummer       | `"L01X00T47"`    |
| `commercial`     | Handelsregisternummer       | `"HRB 12345"`    |
| `custom`         | Benutzerdefiniert           | Beliebig         |

**Beispiel:**

```jsonc
"dp_tax_id": {
  "name": "Steuer-ID",
  "description": "Deutsche Steueridentifikationsnummer",
  "type": "identifier",
  "format": "taxId",
  "validation": {
    "required": true,
    "pattern": "^[0-9]{11}$"
  },
  "binding": {
    "type": "input"
  }
}
```

### Enum-Typ

Der Typ `enum` ermöglicht die Auswahl aus einer vordefinierten Werteliste. Das Feld `options` MUSS
die erlaubten Werte definieren:

```jsonc
"dp_marital_status": {
  "name": "Familienstand",
  "type": "enum",
  "options": [
    {
      "value": "single",
      "label": "Ledig"
    },
    {
      "value": "married",
      "label": "Verheiratet"
    },
    {
      "value": "divorced",
      "label": "Geschieden"
    },
    {
      "value": "widowed",
      "label": "Verwitwet"
    }
  ],
  "binding": {
    "type": "input"
  }
}
```

**Hinweis:** Das `options`-Array MUSS mindestens einen Eintrag haben. Jeder Eintrag MUSS ein
`value`-Feld enthalten und SOLLTE ein `label`-Feld für die Anzeige enthalten ([`DP-06`](../08-validation/index.md#rule-dp-06)).

### Hinweise zur Verwendung

**Currency:**

- Der Typ `currency` MUSS zusammen mit dem Feld `unit` verwendet werden ([`DP-05`](../08-validation/index.md#rule-dp-05))
- Die Einheit SOLLTE dem ISO 4217 Währungscode entsprechen (z.B. `"EUR"`, `"USD"`, `"CHF"`)

```jsonc
"dp_loan_amount": {
  "name": "Kreditsumme",
  "type": "currency",
  "unit": "EUR",
  "binding": {
    "type": "input"
  }
}
```

**Duration:**

- Zeitdauern MÜSSEN im ISO 8601 Duration Format angegeben werden
- Format: `P[n]Y[n]M[n]DT[n]H[n]M[n]S`

| **Beispiel** | **Bedeutung**              |
| ------------ | -------------------------- |
| `"P1Y"`      | 1 Jahr                     |
| `"P6M"`      | 6 Monate                   |
| `"P30D"`     | 30 Tage                    |
| `"PT24H"`    | 24 Stunden                 |
| `"P2Y3M15D"` | 2 Jahre, 3 Monate, 15 Tage |

**Date und DateTime:**

- `date` MUSS dem Format `YYYY-MM-DD` entsprechen
- `datetime` MUSS dem ISO 8601 Format entsprechen und SOLLTE eine Zeitzone enthalten

**Time:**

- Uhrzeiten MÜSSEN im Format `HH:MM:SS` (ISO 8601) angegeben werden
- Sekundenangabe DARF weggelassen werden: `"14:30"` ist gültig

**Integer:**

- Der Typ `integer` erlaubt positive und negative Ganzzahlen
- Für nicht-negative Ganzzahlen (Anzahlen) SOLLTE stattdessen `count` verwendet werden

**Count:**

- Der Typ `count` MUSS eine nicht-negative Ganzzahl sein
- Typische Verwendung: Anzahl Kinder, Anzahl Beschäftigte, etc.

```jsonc
"dp_children_count": {
  "name": "Anzahl Kinder",
  "type": "count",
  "validation": {
    "min": 0,
    "max": 20
  },
  "binding": {
    "type": "input"
  }
}
```

**URL:**

- URLs MÜSSEN dem RFC 3986 Format entsprechen
- Tools SOLLTEN die Erreichbarkeit NICHT zur Validierungszeit prüfen

### 4.7.2 Binding-Typen

Das Feld `binding` eines DataPoints gibt an, wie die Daten zur Laufzeit bezogen werden sollen. Es
dient als Hint für das ausführende Tool und ermöglicht eine klare Kategorisierung der Datenquellen.

### Grundstruktur

```jsonc
"binding": {
  "type": "input"
}
```

### Binding-Typen

| **Typ**    | **Beschreibung**                                              | **Tool-Verhalten**                                                |
| ---------- | ------------------------------------------------------------- | ----------------------------------------------------------------- |
| `input`    | Benutzereingabe erforderlich                                  | Tool generiert Formularfeld oder Chatbot-Frage                    |
| `external` | Externe Datenquelle                                           | Tool zeigt Konfigurationsdialog für Datenquelle                   |
| `computed` | Aus anderen DataPoints über einen JSONata-Ausdruck abgeleitet | Tool berechnet den Wert zur Auswertungszeit — keine Nutzereingabe |

### Input-Binding

Der Typ `input` signalisiert, dass dieser Wert vom Benutzer eingegeben werden muss. Das Tool SOLLTE
basierend auf dem DataPoint-Schema automatisch ein passendes Eingabeelement generieren.

```jsonc
"dp_annual_income": {
  "name": "Jahreseinkommen",
  "type": "currency",
  "unit": "EUR",
  "binding": {
    "type": "input"
  },
  "validation": {
    "required": true,
    "min": 0
  }
}
```

**Optionale Felder für Input-Binding:**

| **Feld**       | **Typ** | **Beschreibung**                                                        |
| -------------- | ------- | ----------------------------------------------------------------------- |
| `hint`         | String  | DARF einen Hinweistext für den Benutzer enthalten ([`DP-09`](../08-validation/index.md#rule-dp-09))        |
| `placeholder`  | String  | DARF einen Platzhaltertext für das Eingabefeld enthalten ([`DP-09`](../08-validation/index.md#rule-dp-09)) |
| `defaultValue` | Any     | DARF einen Standardwert vorgeben ([`DP-09`](../08-validation/index.md#rule-dp-09))                         |

**Beispiel mit optionalen Feldern:**

```jsonc
"binding": {
  "type": "input",
  "hint": "Bitte geben Sie Ihr Brutto-Jahreseinkommen an",
  "placeholder": "z.B. 45000",
  "defaultValue": 0
}
```

### External-Binding

Der Typ `external` signalisiert, dass dieser Wert aus einer externen Quelle bezogen wird. Das Tool
MUSS dem Benutzer eine Möglichkeit bieten, die Datenquelle zu konfigurieren.

```jsonc
"dp_credit_score": {
  "name": "Bonitätsscore",
  "type": "number",
  "binding": {
    "type": "external",
    "ref": "schufa_api",
    "description": "SCHUFA-Schnittstelle zur Bonitätsprüfung"
  }
}
```

**Pflichtfelder für External-Binding:**

| **Feld** | **Typ** | **Beschreibung**                                                        |
| -------- | ------- | ----------------------------------------------------------------------- |
| `ref`    | String  | MUSS eine symbolische Referenz zur Datenquelle enthalten ([`DP-10`](../08-validation/index.md#rule-dp-10)) |

**Optionale Felder für External-Binding:**

| **Feld**      | **Typ** | **Beschreibung**                                                                                      |
| ------------- | ------- | ----------------------------------------------------------------------------------------------------- |
| `description` | String  | DARF eine Beschreibung der erwarteten Datenquelle enthalten ([`DP-09`](../08-validation/index.md#rule-dp-09))                            |
| `sourceType`  | Enum    | DARF die Art der Quelle angeben: `"api"`, `"database"`, `"file"`, `"rulemap"` ([`DP-09`](../08-validation/index.md#rule-dp-09))          |
| `fallback`    | Object  | DARF ein alternatives Binding definieren, falls die externe Quelle nicht verfügbar ist ([`DP-09`](../08-validation/index.md#rule-dp-09)) |

**Beispiel mit Fallback:**

```jsonc
"binding": {
  "type": "external",
  "ref": "schufa_api",
  "description": "SCHUFA-Schnittstelle",
  "sourceType": "api",
  "fallback": {
    "type": "input",
    "hint": "Automatische Abfrage nicht verfügbar. Bitte manuell eingeben."
  }
}
```

**Tool-Workflow für External-Bindings:**

1. Beim Laden der RUML-Datei sammelt das Tool alle `external`-Bindings
2. Das Tool zeigt eine Übersicht: "Folgende Datenquellen müssen konfiguriert werden:"
3. Für jede `ref` ermöglicht das Tool die Zuordnung zu einer konkreten Datenquelle
4. Die Zuordnung wird in der Tool-Konfiguration gespeichert, NICHT in der RUML-Datei

### Vollständiges Beispiel

```jsonc
"data": {
  "dp_annual_income": {
    "name": "Jahreseinkommen",
    "type": "currency",
    "unit": "EUR",
    "binding": {
      "type": "input",
      "hint": "Brutto-Jahreseinkommen"
    },
    "validation": {
      "required": true,
      "min": 0
    }
  },
  "dp_credit_score": {
    "name": "Bonitätsscore",
    "type": "number",
    "binding": {
      "type": "external",
      "ref": "schufa_api",
      "description": "SCHUFA-Schnittstelle",
      "fallback": {
        "type": "input"
      }
    }
  }
}
```

### Computed-Binding

Der Typ `computed` leitet den Wert über einen JSONata-Ausdruck aus **anderen DataPoints** ab. Ein
Rechenergebnis wird damit zu einer benannten, typisierten Größe — z.B. ein Geldbetrag einer
Rechtsfolge, ein Fristende oder ein Bescheidwert. Anders als `ruml:query`, das einen
**Wahrheitswert** für einen Knoten liefert, liefert ein computed-DataPoint einen **Wert**, den
andere Capabilities konsumieren können (z.B. Dokument-Templates, Text-Snippets).

```jsonc
"dp_einkommensteuer": {
  "name": "Festzusetzende Einkommensteuer",
  "type": "currency",
  "unit": "EUR",
  "binding": {
    "type": "computed",
    "expression": "(dp_zve - 11604) * 0.14"
  }
}
```

**Felder für Computed-Binding:**

| **Feld**      | **Typ** | **Beschreibung**                                                                                          |
| ------------- | ------- | --------------------------------------------------------------------------------------------------------- |
| `expression`  | String  | MUSS einen JSONata-Ausdruck enthalten ([`DP-11`](../08-validation/index.md#rule-dp-11)). Andere DataPoints werden über ihre ID referenziert. |
| `description` | String  | DARF die Berechnung beschreiben ([`DP-09`](../08-validation/index.md#rule-dp-09))                                                            |

**Regeln:**

- Der berechnete Wert MUSS dem `type` und der `validation` des DataPoints entsprechen.
- Der Ausdruck DARF andere DataPoints referenzieren, auch andere computed-DataPoints; Referenzen
  DÜRFEN NICHT zyklisch sein (direkt oder transitiv) ([`DP-11`](../08-validation/index.md#rule-dp-11), [`DP-12`](../08-validation/index.md#rule-dp-12)).
- Tools DÜRFEN für einen computed-DataPoint KEINE Nutzereingabe anfordern — der Wert wird zur
  Auswertungszeit bestimmt.

### 4.7.3 Validierung

Das optionale Feld `validation` eines DataPoints definiert Regeln zur Prüfung der eingegebenen oder
bezogenen Datenwerte zur Laufzeit. Tools SOLLTEN diese Regeln anwenden, bevor ein Wert für die
Entscheidungslogik verwendet wird.

### Grundstruktur

```jsonc
"validation": {
  "required": true,
  "min": 0,
  "max": 100000,
  "message": "Bitte geben Sie einen gültigen Wert ein"
}
```

### Validierungsregeln

| **Regel**   | **Typ**            | **Beschreibung**                                                  |
| ----------- | ------------------ | ----------------------------------------------------------------- |
| `required`  | Boolean            | Wenn `true`, MUSS ein Wert vorhanden sein                         |
| `min`       | Number oder String | Minimalwert; sein Typ hängt vom Datentyp ab (siehe Hinweise)      |
| `max`       | Number oder String | Maximalwert; sein Typ hängt vom Datentyp ab (siehe Hinweise)      |
| `minLength` | Integer            | Minimale Zeichenlänge (siehe Hinweise)                            |
| `maxLength` | Integer            | Maximale Zeichenlänge (siehe Hinweise)                            |
| `pattern`   | String             | Regulärer Ausdruck zur Formatprüfung (für `string`, `identifier`) |
| `enum`      | Array              | Liste erlaubter Werte                                             |
| `message`   | String             | Benutzerdefinierte Fehlermeldung                                  |

### Anwendbarkeit nach Datentyp

| **Datentyp** | **Anwendbare Regeln**                                              |
| ------------ | ------------------------------------------------------------------ |
| `string`     | `required`, `minLength`, `maxLength`, `pattern`, `enum`, `message` |
| `number`     | `required`, `min`, `max`, `enum`, `message`                        |
| `boolean`    | `required`, `message`                                              |
| `date`       | `required`, `min`, `max`, `message`                                |
| `datetime`   | `required`, `min`, `max`, `message`                                |
| `time`       | `required`, `min`, `max`, `message`                                |
| `integer`    | `required`, `min`, `max`, `enum`, `message`                        |
| `currency`   | `required`, `min`, `max`, `message`                                |
| `percentage` | `required`, `min`, `max`, `message`                                |
| `duration`   | `required`, `min`, `max`, `message`                                |
| `email`      | `required`, `pattern`, `message`                                   |
| `phone`      | `required`, `pattern`, `message`                                   |
| `location`   | `required`, `enum`, `message`                                      |
| `identifier` | `required`, `minLength`, `maxLength`, `pattern`, `message`         |
| `iban`       | `required`, `pattern`, `message`                                   |
| `count`      | `required`, `min`, `max`, `message`                                |
| `url`        | `required`, `pattern`, `message`                                   |
| `address`    | `required`, `message`                                              |
| `enum`       | `required`, `message`                                              |
| `object`     | `required`, `message`                                              |

Eine `validation`-Regel DARF bei einem Datentyp, für den die Tabelle sie nicht aufführt, NICHT
verwendet werden ([`DP-04`](../08-validation/index.md#rule-dp-04)).

### Beispiele

**Pflichtfeld mit Wertebereich:**

```jsonc
"dp_annual_income": {
  "name": "Jahreseinkommen",
  "type": "currency",
  "unit": "EUR",
  "validation": {
    "required": true,
    "min": 0,
    "max": 10000000,
    "message": "Bitte geben Sie ein gültiges Jahreseinkommen an"
  },
  "binding": {
    "type": "input"
  }
}
```

**Textfeld mit Längenbeschränkung und Pattern:**

```jsonc
"dp_postal_code": {
  "name": "Postleitzahl",
  "type": "string",
  "validation": {
    "required": true,
    "minLength": 5,
    "maxLength": 5,
    "pattern": "^[0-9]{5}$",
    "message": "Bitte geben Sie eine gültige deutsche Postleitzahl ein"
  },
  "binding": {
    "type": "input"
  }
}
```

**Auswahl aus erlaubten Werten:**

```jsonc
"dp_country": {
  "name": "Land",
  "type": "location",
  "format": "country",
  "validation": {
    "required": true,
    "enum": ["DE", "AT", "CH"],
    "message": "Diese Regelung gilt nur für Deutschland, Österreich und die Schweiz"
  },
  "binding": {
    "type": "input"
  }
}
```

**Datumsbereich:**

```jsonc
"dp_birth_date": {
  "name": "Geburtsdatum",
  "type": "date",
  "validation": {
    "required": true,
    "min": "1900-01-01",
    "max": "2010-12-31",
    "message": "Das Geburtsdatum muss zwischen 1900 und 2010 liegen"
  },
  "binding": {
    "type": "input"
  }
}
```

**Identifier mit Format-Validierung:**

```jsonc
"dp_vat_id": {
  "name": "Umsatzsteuer-ID",
  "type": "identifier",
  "format": "vatId",
  "validation": {
    "required": false,
    "pattern": "^DE[0-9]{9}$",
    "message": "Bitte geben Sie eine gültige deutsche USt-ID ein (Format: DE123456789)"
  },
  "binding": {
    "type": "input"
  }
}
```

### Hinweise

**Pattern:**

- Das `pattern`-Feld MUSS einen gültigen regulären Ausdruck enthalten ([`DP-13`](../08-validation/index.md#rule-dp-13))
- Der Ausdruck wird gegen den gesamten Wert geprüft (implizites `^...$`)
- Tools MÜSSEN ECMAScript-kompatible reguläre Ausdrücke (ECMA-262) unterstützen

**Min und Max:**

`min` und `max` MÜSSEN den Typ haben, der für ihren Datentyp angegeben ist ([`DP-14`](../08-validation/index.md#rule-dp-14)):

| **Datentyp**                                  | **Typ von `min` und `max`**                                                                                | **Beispiel**                  |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `number`, `integer`, `currency`, `percentage` | Number                                                                                                     | `0`                           |
| `count`                                       | Nicht-negative Ganzzahl                                                                                    | `1`                           |
| `date`                                        | String, ein `full-date` nach [RFC 3339, Abschnitt 5.6](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) | `"1900-01-01"`                |
| `datetime`                                    | String, Datum und Uhrzeit im Format `YYYY-MM-DDTHH:MM`, wahlweise mit Sekunden, Bruchteil und Offset       | `"2024-01-01T08:00:00+01:00"` |
| `time`                                        | String, eine Uhrzeit im Format `HH:MM` oder `HH:MM:SS`, wahlweise mit Sekundenbruchteil und Offset         | `"08:00"`, `"17:30:00+01:00"` |
| `duration`                                    | String, eine ISO-8601-Dauer                                                                                | `"P18Y"`                      |

- Eine `datetime`- oder `time`-Grenze braucht keinen Offset, so wie ein `datetime`- oder `time`-Wert
  keinen braucht (siehe [4.7.1](#471-datentypen)).
- Tools MÜSSEN Daten, Uhrzeiten und Dauern nach ihrem Wert vergleichen, nicht als Strings.

**MinLength und MaxLength:**

- `minLength` und `maxLength` MÜSSEN ganze Zahlen von 0 bis 2<sup>53</sup> − 1 sein, dem Bereich
  ganzer Zahlen, den JSON-Implementierungen verlässlich austauschen
  ([RFC 8259, Abschnitt 6](https://www.rfc-editor.org/rfc/rfc8259#section-6)) ([`DP-08`](../08-validation/index.md#rule-dp-08)).

**Enum in Kombination mit anderen Regeln:**

- Wenn `enum` definiert ist, MUSS der Wert in der Liste enthalten sein
- Andere Regeln wie `min`, `max`, `pattern` werden zusätzlich geprüft

**Message:**

- Wenn `message` nicht definiert ist, SOLLTE das Tool eine Standardfehlermeldung generieren
- Die Nachricht SOLLTE dem Benutzer helfen, den Fehler zu korrigieren

### 4.7.4 Sets (wiederverwendbare strukturierte Typen)

Eine **Set** ist eine wiederverwendbare, benannte Struktur — eine Gruppe zusammengehöriger
DataPoints (eine Person, eine Beschäftigung, eine Bankverbindung) oder ein Abschnitt von Eingaben in
einem Fragebogen. Sets lösen das Problem, dass `data` sonst eine flache Map ohne Gruppierung ist.

Das Muster trennt **Definition** von **Verwendung**:

- Eine **Set** (die wiederverwendbare Vorlage) wird einmal im `sets`-Register definiert.
- Ein **Object** (eine Instanz) ist ein DataPoint mit `type: "object"`, der ein Set referenziert.

#### Sets definieren

Set-Typen werden im `sets`-Objekt der `ruml:datapoints`-Capability deklariert, mit ihrer ID als
Schlüssel:

```jsonc
"sets": {
  "set_person": {
    "name": "Person",
    "fields": {
      "dp_vorname": {
        "name": "Vorname",
        "type": "string",
        "binding": {
          "type": "input"
        }
      },
      "dp_nachname": {
        "name": "Nachname",
        "type": "string",
        "binding": {
          "type": "input"
        }
      },
      "dp_geburtsdatum": {
        "name": "Geburtsdatum",
        "type": "date",
        "binding": {
          "type": "input"
        }
      },
      "dp_beschaeftigung": {
        "name": "Beschäftigung",
        "type": "object",
        "set": "set_beschaeftigung",
        "binding": {
          "type": "input"
        }
      }
    }
  },
  "set_beschaeftigung": {
    "name": "Beschäftigung",
    "fields": {
      "dp_arbeitgeber": {
        "name": "Arbeitgeber",
        "type": "string",
        "binding": {
          "type": "input"
        }
      },
      "dp_beginn": {
        "name": "Beginn der Beschäftigung",
        "type": "date",
        "binding": {
          "type": "input"
        }
      },
      "dp_nettoeinkommen": {
        "name": "Monatliches Nettoeinkommen",
        "type": "currency",
        "unit": "EUR",
        "validation": {
          "min": 0
        },
        "binding": {
          "type": "input"
        }
      }
    }
  }
}
```

| **Feld**      | **Typ** | **Beschreibung**                                                                                                                                   |
| ------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | String  | MUSS einen Anzeigenamen der Set enthalten ([`DP-15`](../08-validation/index.md#rule-dp-15))                                                                                           |
| `fields`      | Object  | MUSS die Mitglieds-DataPoints enthalten, mit ihren IDs als Schlüssel. Ein Feld DARF selbst `type: "object"` sein (Verschachtelung) ([`DP-15`](../08-validation/index.md#rule-dp-15)). |
| `description` | String  | DARF die Set beschreiben ([`DP-15`](../08-validation/index.md#rule-dp-15))                                                                                                            |

#### Sets verwenden

Ein DataPoint instanziiert ein Set mit `type: "object"` und einer `set`-Referenz:

```jsonc
"data": {
  "dp_antragsteller": {
    "name": "Antragsteller",
    "type": "object",
    "set": "set_person",
    "binding": {
      "type": "input"
    }
  },
  "dp_buergen": {
    "name": "Bürgen",
    "type": "object",
    "set": "set_person",
    "cardinality": {
      "min": 0,
      "max": 3
    },
    "binding": {
      "type": "input"
    }
  }
}
```

- **`set`** MUSS eine im `sets`-Register deklarierte ID referenzieren ([`DP-16`](../08-validation/index.md#rule-dp-16)).
- **`cardinality`** (`{ min, max }`) steuert die Wiederholung: ohne Angabe → ein einzelnes Object;
  `max > 1` → eine Liste von Objects (z.B. eine „Weitere hinzufügen"-Liste im Fragebogen, FIM
  _Multiplizität_).
- **Verschachtelung:** Da ein `fields`-Eintrag selbst `type: "object"` sein kann, lassen sich Sets
  zusammensetzen (im Beispiel hat `set_person` ein `set_beschaeftigung`-Feld).

#### Felder referenzieren

Felder innerhalb eines Objects werden per Pfad (JSONata) ausgehend von der DataPoint-ID
referenziert, z.B. `dp_antragsteller.dp_geburtsdatum` in einem `ruml:query`-Ausdruck. Bei einem
wiederholten Object (`cardinality.max > 1`) ist der Wert ein Array und Mitglieder werden indiziert,
z.B. `dp_buergen[0].dp_nachname`.

**Regeln:**

- Jede `set`-Referenz MUSS auf eine ID in `sets` auflösbar sein ([`DP-16`](../08-validation/index.md#rule-dp-16)).
- `fields`-Schlüssel eines Sets und Set-IDs MÜSSEN dem Muster `[a-z_][a-z0-9_]*` entsprechen
  ([`DP-02`](../08-validation/index.md#rule-dp-02)).
- Set-Definitionen DÜRFEN verschachtelt sein, DÜRFEN aber NICHT rekursiv sein (ein Set DARF sich
  NICHT direkt oder transitiv selbst referenzieren) ([`DP-17`](../08-validation/index.md#rule-dp-17)).

## Konformitätstests

- [4.7 DataPoints](../../../tests/04-capabilities/4-7-data-points.test.yaml)
