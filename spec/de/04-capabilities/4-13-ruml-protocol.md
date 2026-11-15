<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.13 ruml:protocol

## 4.13 Capability `ruml:protocol`

### Überblick

| Eigenschaft             | Wert                         |
| ----------------------- | ---------------------------- |
| **Capability-ID**       | `ruml:protocol`              |
| **Scope**               | Root-Level (nur Deklaration) |
| **Standard `required`** | `false`                      |
| **Rolle**               | `reaction`                   |

Diese Capability fordert ein **Auswertungsprotokoll** an: eine chronologische, maschinenlesbare
Aufzeichnung all dessen, was die Engine während einer Auswertung getan hat — geschrieben in die
RUML-Result-Datei (siehe [Kapitel 5](../05-result-format/index.md)). Sie liefert vollständige
Nachvollziehbarkeit für Audit-Zwecke, einschließlich Ereignissen, die in keinem Knotenergebnis
erscheinen: Datenbeschaffung, Warnungen, Abbrüche, Short-Circuit-Überspringungen.

Das Protokoll **ergänzt** die Knotenergebnisse: Knotenergebnisse enthalten das detaillierte Ergebnis
pro Knoten (Status, Capability-Details), das Protokoll enthält die **Abfolge** des Laufs.

### Root-Level-Deklaration

```jsonc
"capabilities": [
  {
    "id": "ruml:protocol",
    "required": true,
    "payload": {
      "config": {
        "level": "standard"
      }
    }
  }
]
```

Es gibt kein `data`-Objekt und keinen Node-Level-Payload — die Capability ist eine Anweisung an die
auswertende Engine. `ruml:protocol` DARF NICHT im `capabilities`-Array eines Knotens vorkommen,
weder inline noch in einer RUML-EXT-Datei ([`CAP-18`](../08-validation/index.md#rule-cap-18)).

**Semantik:**

- Ist `ruml:protocol` deklariert, SOLLTE die Engine ein Protokoll in das Result schreiben.
- Bei Deklaration mit `required: true` MUSS die Engine ein Protokoll schreiben. Eine Engine, die das
  nicht kann, DARF die Datei NICHT auswerten.
- Engines DÜRFEN auch ohne Deklaration ein Protokoll schreiben.

**Konfiguration (`config`):**

| **Feld** | **Typ** | **Beschreibung**                                                                                                    |
| -------- | ------- | ------------------------------------------------------------------------------------------------------------------- |
| `level`  | Enum    | DARF die Detailtiefe angeben: `standard` (Standard) oder `verbose`. Siehe Ereignis-Vokabular unten ([`CAP-36`](../08-validation/index.md#rule-cap-36)). |

### Protokoll-Format: CloudEvents

Das Protokoll wird in der RUML-Result-Datei im `evaluation.capabilities`-Eintrag mit
`id: "ruml:protocol"` gespeichert — konsistent damit, wie alle capability-erzeugten Daten in Results
erscheinen:

| **Feld** | **Typ** | **Beschreibung**                                                                                                                                                                                                                   |
| -------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `level`  | Enum    | Die Detailtiefe, mit der das Protokoll aufgezeichnet wurde (`standard` oder `verbose`)                                                                                                                                             |
| `events` | Array   | Das Protokoll: ein JSON-Array gemäß dem [CloudEvents v1.0 JSON Batch Format](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md) (eigenständiger Media-Type: `application/cloudevents-batch+json`) |

Jeder Eintrag in `events` ist ein CloudEvent; RUML definiert darauf folgendes Profil:

| **Attribut**  | **CloudEvents**         | **RUML-Profil**                                                                                                            |
| ------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `specversion` | Pflicht                 | MUSS `"1.0"` sein                                                                                                          |
| `id`          | Pflicht                 | MUSS innerhalb des Protokolls eindeutig sein (CloudEvents: `source` + `id` eindeutig)                                      |
| `source`      | Pflicht (URI-Referenz)  | MUSS die auswertende Engine identifizieren (und SOLLTE deren Version enthalten); eine absolute URI ist EMPFOHLEN           |
| `type`        | Pflicht                 | MUSS einer der `ruml.*`-Ereignistypen unten sein, oder ein benutzerdefinierter Typ, der NICHT den Präfix `ruml.` verwendet |
| `time`        | in CloudEvents optional | in diesem Profil **ERFORDERLICH** (RFC 3339)                                                                               |
| `subject`     | optional                | Der Knoten-**Pfad** bzw. die DataPoint-ID, auf die sich das Ereignis bezieht (sofern zutreffend)                           |
| `data`        | optional                | Ereignis-Payload als direkter JSON-Wert (ohne `datacontenttype` ⇒ gemäß CloudEvents als `application/json` behandelt)      |

**Reihenfolge:** CloudEvents definiert keine Ereignisreihenfolge. In diesem Profil ist **die
Array-Reihenfolge normativ**: Ereignisse MÜSSEN in der Reihenfolge erscheinen, in der die Engine sie
erzeugt hat. `time` allein genügt nicht (mehrere Ereignisse können denselben Zeitstempel tragen).

**Hinweis zur `type`-Benennung:** CloudEvents empfiehlt Reverse-DNS-Präfixe für Typen; dieses Profil
verwendet für spezifikationsdefinierte Ereignisse bewusst den kurzen Präfix `ruml.`.
Implementierungsspezifische Ereignisse MÜSSEN einen eigenen, abweichenden Präfix verwenden.

### Ereignis-Vokabular

| **Typ**                     | **Level** | **`subject`** | **`data`**                                                    |
| --------------------------- | --------- | ------------- | ------------------------------------------------------------- |
| `ruml.evaluation.started`   | standard  | —             | `{ "mode": … }`                                               |
| `ruml.evaluation.completed` | standard  | —             | DARF Zusammenfassungswerte enthalten                          |
| `ruml.evaluation.aborted`   | standard  | —             | `{ "reason": … }`                                             |
| `ruml.node.evaluated`       | standard  | Knoten-Pfad   | `{ "lexId": …, "status": …, "capability"?: …, "reason"?: … }` |
| `ruml.node.skipped`         | verbose   | Knoten-Pfad   | `{ "lexId": …, "cause": "shortCircuit" }`                     |
| `ruml.datapoint.resolved`   | verbose   | DataPoint-ID  | `{ "binding": …, "value"?: … }`                               |
| `ruml.action.triggered`     | standard  | Knoten-Pfad   | `{ "operation": …, "trigger": …, "status": … }`               |
| `ruml.warning`              | standard  | optional      | `{ "message": …, "code"?: … }`                                |
| `ruml.error`                | standard  | optional      | `{ "message": …, "code"?: … }`                                |

`standard`-Ereignisse MÜSSEN auf beiden Stufen geschrieben werden; `verbose`-Ereignisse DÜRFEN NICHT
bei `level: "standard"` geschrieben werden. Implementierungen DÜRFEN zusätzliche Ereignistypen
definieren (eigener Präfix).

**Sensible Daten:** Die Werte von DataPoints mit `sensitive: true` (siehe
[Kapitel 4.7](4-7-data-points.md)) DÜRFEN NICHT im Protokoll erscheinen — weder in `data.value` noch
in Meldungen.

### Beispiel

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934"
  },
  "evaluation": {
    "id": "d8129e0c-cf2e-4ef9-b7b6-fa8b206d5517",
    "timestamp": "2024-01-15T10:00:05Z",
    "mode": "complete",
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "reason": "Child 1.1 is true"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "reason": "ruml:query yields true for dp_annual_income 50000"
      }
    },
    "capabilities": [
      {
        "id": "ruml:protocol",
        "payload": {
          "level": "verbose",
          "events": [
            {
              "specversion": "1.0",
              "id": "0001",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.evaluation.started",
              "time": "2024-01-15T10:00:00Z",
              "data": {
                "mode": "complete"
              }
            },
            {
              "specversion": "1.0",
              "id": "0002",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.datapoint.resolved",
              "time": "2024-01-15T10:00:01Z",
              "subject": "dp_annual_income",
              "data": {
                "binding": "input",
                "value": 50000
              }
            },
            {
              "specversion": "1.0",
              "id": "0003",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.node.evaluated",
              "time": "2024-01-15T10:00:02Z",
              "subject": "1.1",
              "data": {
                "lexId": "2",
                "status": "true",
                "capability": "ruml:query"
              }
            },
            {
              "specversion": "1.0",
              "id": "0004",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.node.evaluated",
              "time": "2024-01-15T10:00:03Z",
              "subject": "1",
              "data": {
                "lexId": "1",
                "status": "true"
              }
            },
            {
              "specversion": "1.0",
              "id": "0005",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.evaluation.completed",
              "time": "2024-01-15T10:00:05Z"
            }
          ]
        }
      }
    ]
  }
}
```

### Engine-Pflichten

| ID    | Anforderung                                                                                                                                                                                                                                        |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PT-01 | Ist `ruml:protocol` mit `required: true` deklariert, MUSS die Engine das Protokoll in `payload.events` des `evaluation.capabilities`-Eintrags mit `id: "ruml:protocol"` schreiben; eine Engine, die das nicht kann, DARF die Datei NICHT auswerten |
| PT-02 | Jeder Protokolleintrag MUSS CloudEvents v1.0 (JSON-Format) entsprechen; die Array-Reihenfolge MUSS der Reihenfolge des Auftretens entsprechen                                                                                                      |
| PT-03 | `time` MUSS bei jedem Ereignis vorhanden sein (RFC 3339)                                                                                                                                                                                           |
| PT-04 | Werte von `sensitive`-DataPoints DÜRFEN NICHT im Protokoll erscheinen                                                                                                                                                                              |
| PT-05 | Implementierungsspezifische Ereignistypen DÜRFEN NICHT den Präfix `ruml.` verwenden                                                                                                                                                                |
