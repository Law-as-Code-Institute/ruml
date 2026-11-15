<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.5 RUML-EXT-Format

### Überblick

Das RUML-EXT-Format definiert eine **Sidecar-Datei**, die Capability-Erweiterungsdaten separat von
der Ursprungs-RUML-Datei speichert. Sie ergänzt die in [Kapitel 4.1](4-1-concept.md) beschriebene
Inline-Methode durch den Sidecar-Modus.

- **Dateiendung:** `.ruml-ext`
- **Format-Identifikation:** `$format: "RUML-EXT"`
- **Zweck:** Transport von `capabilities`-Daten ohne Modifikation der Ursprungs-RUML-Datei
- **Schema:** [`ruml-ext.schema.json`](../../../schemas/ruml-ext.schema.json)
  ([Draft 2020-12](https://json-schema.org/draft/2020-12))

### Root-Objekt-Struktur

Eine RUML-EXT-Datei MUSS folgende Pflichtfelder enthalten:

```jsonc
{
  "$format": "RUML-EXT",
  "$specVersion": "1.0",
  "$base": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "capabilities": [/* ... */],
  "nodes": {/* ... */}
}
```

| Feld           | Typ    | Pflicht | Beschreibung                                                                                                                                                                         |
| -------------- | ------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `$format`      | String | MUSS    | MUSS den Wert `"RUML-EXT"` haben                                                                                                                                                     |
| `$specVersion` | String | MUSS    | Dieselben Versionierungsregeln wie RUML (siehe [Kapitel 2.3](../02-file-format-basics/2-3-versioning.md))                                                                            |
| `$base`        | Object | MUSS    | Referenz auf die Basis-RUML-Datei (siehe unten)                                                                                                                                      |
| `capabilities` | Array  | MUSS    | Die Capabilities, deren Daten in dieser EXT-Datei enthalten sind — eine Liste von Einträgen wie in [Kapitel 4.2](4-2-capabilities-field.md), deren Reihenfolge nicht signifikant ist |
| `nodes`        | Object | MUSS    | Erweiterungsdaten, indexiert über UUIDs                                                                                                                                              |

Ein Parser MUSS prüfen, ob `$format` den Wert `"RUML-EXT"` hat, bevor er die EXT-Datei
weiterverarbeitet ([`CAP-22`](../08-validation/index.md#rule-cap-22)).

Das Root-Objekt einer RUML-EXT-Datei DARF NICHT die Felder `metadata` und `rulemap` enthalten — sie
sind ausschließlich der Basis-RUML-Datei vorbehalten ([`CAP-23`](../08-validation/index.md#rule-cap-23)). Ein Parser MUSS das
Vorhandensein eines dieser Felder als Validierungsfehler behandeln. `evaluation` ist ebenfalls kein
EXT-Root-Feld — es gehört in RUML-Result-Dateien (`.ruml-result`) —, ist aber nicht Teil der
[`CAP-23`](../08-validation/index.md#rule-cap-23)-Prüfung.

Root-Level-Artefaktdaten werden NICHT als eigene Root-Felder der EXT-Datei transportiert, sondern
über das `payload.data`-Feld des jeweiligen Eintrags im `capabilities`-Array (siehe
[Kapitel 4.2](4-2-capabilities-field.md)).

### Das `$base`-Feld

```jsonc
"$base": {
  "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
  "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
}
```

| Feld   | Typ    | Pflicht | Beschreibung                                                                                                                                                   |
| ------ | ------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`   | UUID   | MUSS    | Die `metadata.id` der Basis-RUML-Datei. MUSS dem UUID-v4-Format entsprechen (Pattern `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`). |
| `hash` | String | MUSS    | Der Hash der Basis-RUML-Datei zum Zeitpunkt der Erstellung dieser EXT-Datei.                                                                                   |

Der Hash MUSS über die kanonische Form der Basis-RUML-Datei nach den Hashing-Regeln des Containers
berechnet werden ([Kapitel 2.4](../02-file-format-basics/2-4-integrity.md),
[Kapitel 7.3](../07-container/7-3-hashing.md)). Er identifiziert die **exakte Version** der
Basis-Datei, auf die sich die EXT-Datei bezieht.

### Hash-Verifizierung

Bevor ein Parser die Erweiterungsdaten aus einer RUML-EXT-Datei mit einer RUML-Datei zusammenführt,
MUSS er folgende Schritte durchführen ([`CAP-24`](../08-validation/index.md#rule-cap-24)):

1. **ID-Abgleich:** Die `$base.id` der EXT-Datei MUSS mit der `metadata.id` der RUML-Datei
   übereinstimmen.
2. **Hash-Verifizierung:** Der aktuelle Hash der RUML-Datei MUSS mit dem `$base.hash` der EXT-Datei
   übereinstimmen.
3. **Wenn der Hash nicht übereinstimmt:** Der Parser MUSS den Merge abbrechen und einen Fehler
   ausgeben.

Ein Parser DARF NICHT auf diesen Hash-Abgleich verzichten — auch nicht in Entwicklungsumgebungen
oder bei explizitem Benutzer-Override, sofern die Spezifikation keine Ausnahme definiert
([`CAP-25`](../08-validation/index.md#rule-cap-25)).

:::warning[Veraltete EXT-Datei]
Wenn die Basis-RUML-Datei seit der Erstellung der EXT-Datei verändert wurde, stimmt der Hash nicht
mehr überein. Der Parser MUSS in diesem Fall den Merge ablehnen. Ein stilles Zusammenführen
veralteter Erweiterungsdaten würde zu inkonsistenten Zuständen führen.
:::

### Das `nodes`-Objekt in RUML-EXT

Die Erweiterungsdaten im `nodes`-Objekt sind über **UUIDs** (nicht LexIDs) indexiert. Dies ist
notwendig, weil LexIDs bei modularen Knoten nicht eindeutig positions-adressierbar sind, UUIDs
hingegen global eindeutig.

```jsonc
"nodes": {
  "0eb360a6-626a-406d-89a1-9f434ced141b": {
    "com.example/review-notes": {
      "status": "approved",
      "reviewer": "rechtsabteilung"
    }
    // ...
  },
  "8fc54c7d-7f60-410e-9493-4f1eecfb1af8": {
    "com.example/review-notes": {
      "status": "pending"
    }
  }
  // ...
}
```

- **Schlüssel:** Eine gültige UUID, die im `nodes`-Objekt der Basis-RUML-Datei existiert (der Wert
  des `id`-Felds des Knotens).
- **Wert:** Ein Objekt, dessen Schlüssel Capability-IDs aus dem `capabilities`-Array der EXT-Datei
  sind.

#### Unbekannte UUID-Referenzen

Wenn eine UUID im `nodes`-Objekt der EXT-Datei keinem Knoten in der Basis-RUML-Datei entspricht,
MUSS der Parser dies als Fehler behandeln ([`CAP-26`](../08-validation/index.md#rule-cap-26)). Dies verhindert stille Daten-Phantome
(Erweiterungsdaten für nicht-existente Knoten).

### Vollständiges Beispiel

**Basis-RUML-Datei** (`pruefung-volljährigkeit.ruml`):

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_age": {
            "name": "Alter",
            "type": "integer",
            "binding": {
              "type": "input"
            }
          },
          "dp_competent": {
            "name": "Geschäftsfähig",
            "type": "boolean",
            "binding": {
              "type": "input"
            }
          }
        }
      }
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.2.0",
    "created": "2024-01-15T09:00:00Z",
    "modified": "2024-03-20T14:30:00Z",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "operator": "AND",
        "label": "Geschäftsfähigkeit",
        "children": ["2", "3"]
      },
      "2": {
        "id": "8fc54c7d-7f60-410e-9493-4f1eecfb1af8",
        "label": "Volljährigkeit",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_age >= 18"
            }
          }
        ]
      },
      "3": {
        "id": "56b5b9db-b791-4fe5-abb0-a05cb0847db6",
        "label": "Keine Entmündigung",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_competent = true"
            }
          }
        ]
      }
    }
  }
}
```

**RUML-EXT-Sidecar** (`pruefung-volljährigkeit.ruml-ext`):

```jsonc
{
  "$format": "RUML-EXT",
  "$specVersion": "1.0",
  "$base": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "capabilities": [
    {
      "id": "com.example/review-notes",
      "role": "data"
    },
    {
      "id": "com.example/priority",
      "role": "data"
    }
  ],
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "com.example/review-notes": {
        "status": "approved",
        "reviewer": "rechtsabteilung"
      },
      "com.example/priority": {
        "level": "high"
      }
    },
    "8fc54c7d-7f60-410e-9493-4f1eecfb1af8": {
      "com.example/review-notes": {
        "status": "pending"
      }
    },
    "56b5b9db-b791-4fe5-abb0-a05cb0847db6": {
      "com.example/review-notes": {
        "status": "approved",
        "reviewer": "rechtsabteilung"
      },
      "com.example/priority": {
        "level": "low"
      }
    }
  }
}
```

### Verhältnis zur Inline-Methode

Es ist nicht erlaubt, dieselbe Capability für denselben Knoten gleichzeitig inline (im
`capabilities`-Feld) und in einer EXT-Datei zu definieren. Bei einem Merge MUSS der Parser prüfen,
ob ein Konflikt vorliegt, und diesen als Fehler behandeln ([`CAP-27`](../08-validation/index.md#rule-cap-27)). Eine stille
Überschreibung oder Zusammenführung DARF NICHT erfolgen.

### Mehrere EXT-Dateien für eine RUML-Datei

Es DARF mehrere EXT-Dateien geben, die dieselbe Basis-RUML-Datei referenzieren — z.B. eine EXT-Datei
pro Capability-Anbieter. Jede EXT-Datei MUSS unabhängig verifiziert werden. Konflikte zwischen
EXT-Dateien (gleiche Capability auf gleichem Knoten in zwei verschiedenen EXT-Dateien) MÜSSEN als
Fehler behandelt werden ([`CAP-27`](../08-validation/index.md#rule-cap-27)).
