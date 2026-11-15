<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 5.1 Ergebnismodell und Speicherung

### 5.1.1 Grundkonzept

Nach Abschluss einer Auswertung DÜRFEN die Ergebnisse persistent gespeichert werden.
Auswertungsergebnisse MÜSSEN in einer separaten RUML-Result-Datei (`.ruml-result`) gespeichert
werden. Das Einbetten von Auswertungsergebnissen in eine RUML-Datei (`.ruml`) ist NICHT erlaubt.

---

**Inhalte eines Auswertungsergebnisses:**

Ein vollständiges Auswertungsergebnis SOLLTE folgende Informationen enthalten:

- **Metadaten:** ID, Zeitstempel, verwendeter Modus, Fallreferenz
- **Knotenstatus:** Der finale Status jedes ausgewerteten Knotens (`true`, `false`, `undefined`,
  `ignored`). Knoten mit Status `pending` werden NICHT gespeichert — ein fehlender Eintrag im
  `results`-Objekt bedeutet implizit `pending`.
- **Begründungen:** Erklärungen für das jeweilige Ergebnis
- **Capability-Ergebnisse:** Capability-spezifische Auswertungsdaten pro Knoten (z.B.
  Query-Ergebnisse, ausgelöste Actions)
- **Aktive Capabilities:** Deklaration der bei der Auswertung verwendeten Capabilities

---

### 5.1.2 RUML-Result-Datei

Das Auswertungsergebnis wird in einer eigenständigen Datei gespeichert, die auf die RUML-Struktur
verweist.

---

**Dateiendung:** `.ruml-result`

**Struktur:**

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d9c7e5c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e"
  },
  "evaluation": {
    "id": "17175dae-2a30-4757-b146-71bdb114eea6",
    "timestamp": "2024-01-15T10:00:00Z",
    "mode": "complete",
    "caseId": "Fall-2024-00123",
    "capabilities": [
      {
        "id": "ruml:datapoints"
      },
      {
        "id": "ruml:query"
      },
      {
        "id": "ruml:actions"
      }
    ],
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "reason": "AND: alle Kinder true"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "reason": "Alter 25 >= 18"
      },
      "1.2": {
        "lexId": "3",
        "status": "true",
        "reason": "XOR: genau ein Kind true"
      },
      "1.2.1": {
        "lexId": "4",
        "status": "true",
        "reason": "Einkommen 35000 <= 40000"
      },
      "1.2.2": {
        "lexId": "5",
        "status": "false",
        "reason": "Kein Härtefall"
      },
      "1.3": {
        "lexId": "6",
        "status": "true",
        "reason": "Wohnsitz BY == BY"
      }
    }
  }
}
```

---

**Pflichtfelder im rumlReference-Objekt:**

| Feld | Typ  | Beschreibung                     |
| ---- | ---- | -------------------------------- |
| `id` | UUID | ID der referenzierten RUML-Datei |

**Optionale Felder im rumlReference-Objekt:**

| Feld   | Typ    | Beschreibung                                                                                                                                                                                                      |
| ------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hash` | String | Hash der referenzierten RUML-Datei zur Integritätsprüfung. Wenn vorhanden, verifiziert das Tool ihn; wenn nicht vorhanden, kann die Integrität der RUML-Struktur nicht geprüft werden und das Tool SOLLTE warnen. |

---

**Pflichtfelder im evaluation-Objekt:**

| Feld        | Typ      | Beschreibung                                           |
| ----------- | -------- | ------------------------------------------------------ |
| `id`        | UUID     | Eindeutige ID des Auswertungsergebnisses               |
| `timestamp` | DateTime | Zeitpunkt des Auswertungsabschlusses                   |
| `mode`      | Enum     | Verwendeter Auswertungsmodus (`optimized`, `complete`) |
| `results`   | Object   | Ergebnisse pro Knoten-Instanz, indiziert nach Pfad     |

---

**Optionale Felder im evaluation-Objekt:**

| Feld             | Typ      | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `caseId`         | String   | Externe Fallreferenz (z.B. Aktenzeichen)                                                                                                                                                                                                                                                                                                                                                                                            |
| `userId`         | String   | ID des auswertenden Benutzers                                                                                                                                                                                                                                                                                                                                                                                                       |
| `toolId`         | String   | ID des ausführenden Tools                                                                                                                                                                                                                                                                                                                                                                                                           |
| `toolVersion`    | String   | Version des ausführenden Tools                                                                                                                                                                                                                                                                                                                                                                                                      |
| `startTimestamp` | DateTime | Zeitpunkt des Auswertungsbeginns                                                                                                                                                                                                                                                                                                                                                                                                    |
| `capabilities`   | Array    | DARF die bei der Auswertung aktiven Capabilities als Einträge der Form `{ id, payload? }` deklarieren; ihre Reihenfolge ist nicht signifikant. Capability-spezifische Felder (z.B. Modell-Version, Konfiguration) DÜRFEN im `payload` des Eintrags enthalten sein. Bei `ruml:protocol` enthält der `payload` des Eintrags das aufgezeichnete Auswertungsprotokoll (siehe [Kapitel 4.13](../04-capabilities/4-13-ruml-protocol.md)). |

---

**Die Eigenschaft `results`**

Die Eigenschaft `results` MUSS für jede Knotenauswertung ein Knoten-Ergebnis enthalten, indiziert
nach dessen Pfad, sowie für jeden Knoten, der im `optimized`-Modus durch einen Short-Circuit
ignoriert wurde (siehe [Kapitel 3.6](../03-data-model/3-6-operators.md#auswertungsmodus)). Ein
Child-Node eines ignorierten Knotens DARF NICHT im `results`-Objekt enthalten sein.

Der Schlüssel eines Knoten-Ergebnisses MUSS eine durch Punkte getrennte Liste von Array-Indizes
sein, die bei 1 beginnen, jeweils bezogen auf das `children`-Array des übergeordneten Knotens.

| Pfad    | Knoten                                                      |
| ------- | ----------------------------------------------------------- |
| `1`     | Der Root-Node                                               |
| `1.2`   | Der zweite Child-Node des Root-Nodes                        |
| `1.2.1` | Der erste Child-Node des zweiten Child-Nodes des Root-Nodes |

**Struktur eines Knoten-Ergebnisses:**

```jsonc
"results": {
  "1": {
    "lexId": "1",
    "status": "true",
    "evaluatedAt": "2024-01-15T10:00:01Z",
    "reason": "Alle Voraussetzungen erfüllt",
    "capabilities": [
      {
        "id": "ruml:query",
        "payload": {
          "expression": "dp_age >= 18",
          "inputs": {
            "dp_age": 25
          },
          "result": "true"
        }
      },
      {
        "id": "ruml:actions",
        "payload": {
          "triggered": [
            {
              "id": "notify-approval",
              "trigger": "onTrue",
              "operation": "sendNotification",
              "timestamp": "2024-01-15T10:00:02Z",
              "status": "success"
            }
          ]
        }
      }
    ]
  }
}
```

---

**Felder eines Knoten-Ergebnisses:**

| Feld           | Typ                | Pflicht | Beschreibung                                                                                                                                         |
| -------------- | ------------------ | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lexId`        | String             | Ja      | Die `lexId` des Knotens, auf den sich dieses Ergebnis bezieht (Pattern `^[1-9][0-9]*$`)                                                              |
| `status`       | Enum               | Ja      | Finaler Status: `true`, `false`, `undefined`, `ignored`. `pending` ist kein gültiger Wert — ausstehende Knoten erscheinen nicht im `results`-Objekt. |
| `evaluatedAt`  | DateTime           | Nein    | Zeitpunkt der Auswertung dieses Knotens                                                                                                              |
| `reason`       | String oder Object | Ja      | Begründung für den Status; ihre Form hängt von `status` ab, siehe [Kapitel 5.0](5-0-status-types.md)                                                 |
| `capabilities` | Array              | Nein    | Capability-spezifische Auswertungsergebnisse als geordnete Einträge `{ id, payload? }`; jede `id` ist eine bei der Auswertung aktive Capability.     |

**Node-Result-Payload von `ruml:query`:**

| Feld         | Typ    | Pflicht | Beschreibung                                                                                                                |
| ------------ | ------ | ------- | --------------------------------------------------------------------------------------------------------------------------- |
| `expression` | String | Ja      | Der ausgewertete Query-Ausdruck (nicht leer, siehe [Kapitel 4.8](../04-capabilities/4-8-ruml-query.md))                     |
| `inputs`     | Object | Ja      | Aufgelöste Eingabewerte, die der Ausdruck referenziert, indiziert nach DataPoint-ID                                         |
| `result`     | Enum   | Ja      | Ergebnis der Auswertung des Ausdrucks: `true`, `false`, `undefined` — dieselben Werte wie bei `status`, als Strings notiert |

Zusätzliche Felder sind NICHT erlaubt.

**Node-Result-Payload von `ruml:expression`:**

| Feld         | Typ    | Pflicht | Beschreibung                                                                                                                                |
| ------------ | ------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `expression` | String | Ja      | Der ausgewertete Ausdruck (nicht leer, siehe [Kapitel 4.14](../04-capabilities/4-14-ruml-expression.md))                                    |
| `inputs`     | Object | Ja      | Aufgelöste DataPoint-Werte, die der Ausdruck referenziert, indiziert nach DataPoint-ID; leer, wenn er keine liest                           |
| `children`   | Array  | Ja      | Die vom Ausdruck gesehenen Kind-Ergebnisse als `{ lexId, status }`, in der Reihenfolge von `children`; jeder Status ist `true` oder `false` |
| `result`     | Enum   | Ja      | Ergebnis der Auswertung des Ausdrucks: `true`, `false`, `undefined`                                                                         |

Zusätzliche Felder sind NICHT erlaubt. Das Festhalten der Kind-Status ist es, was die Entscheidung
reproduzierbar macht: Anders als bei einem logischen Operator ergibt sich die Regel nicht aus dem
Namen des Operators. Der Payload wird nur geschrieben, wenn der Ausdruck gelaufen ist; ein Knoten,
der wegen eines Kindes mit `undefined` selbst `undefined` ist, führt keinen
`ruml:expression`-Payload.

---

**Pfad-basierte Indizierung und modulare Knoten:**

Das `results`-Objekt verwendet den **Pfad** als Schlüssel, nicht die `lexId`. Diese Entscheidung
ermöglicht die korrekte Behandlung modularer Knoten (siehe
[Kapitel 6](../06-modular-nodes/index.md)):

- **Normale Knoten:** Haben genau einen Pfad und damit genau einen Eintrag in `results`
- **Modulare Knoten:** Können an mehreren Stellen im Baum referenziert werden. Jede Instanz hat
  einen eigenen Pfad und kann ein **unterschiedliches Ergebnis** haben. Daher erhält jede Instanz
  einen eigenen Eintrag in `results`.

**Beispiel für einen modularen Knoten mit unterschiedlichen Ergebnissen:**

```jsonc
"results": {
  "1": {
    "lexId": "1",
    "status": "false",
    "reason": "AND: Kind 1.2 false"
  },
  "1.1": {
    "lexId": "8",
    "status": "true",
    "reason": "Bonität ausreichend"
  },
  "1.2": {
    "lexId": "2",
    "status": "false",
    "reason": "AND: Kind 1.2.1 false"
  },
  "1.2.1": {
    "lexId": "8",
    "status": "false",
    "reason": "Bonität nicht ausreichend"
  }
}
```

Im Beispiel wird Knoten mit `lexId: 8` an zwei Stellen referenziert (Pfade `1.1` und `1.2.1`) und
hat unterschiedliche Ergebnisse (`true` vs. `false`).

---

**Verhalten beim Laden:**

1. Tool lädt die RUML-Result-Datei
2. Tool lädt die referenzierte RUML-Datei anhand von `rumlReference.id`
3. Wenn `rumlReference.hash` vorhanden ist: Tool verifiziert den Hash der RUML-Datei dagegen
4. Bei Hash-Übereinstimmung (oder wenn kein Hash vorhanden ist und die RUML-Datei gefunden wird):
   RUML-Datei verwenden
5. Bei Hash-Abweichung: Tool MUSS eine Warnung ausgeben, dass die Regelstruktur nicht
   rekonstruierbar ist
6. Wenn `rumlReference.hash` fehlt: Tool DARF die RUML-Datei verwenden, SOLLTE aber warnen, dass
   ihre Integrität nicht verifiziert werden kann
7. Wenn die referenzierte RUML-Datei fehlt: Tool MUSS eine Warnung ausgeben, dass die Regelstruktur
   nicht rekonstruierbar ist

---

### 5.1.3 Integritätssicherung

Für rechtlich relevante Verfahren MUSS die Integrität der Ergebnisse gewährleistet sein. Die
Integritätssicherung von RUML-Result-Dateien wird auf Container-Ebene behandelt (siehe Kapitel 7).

---

**Hash-Anforderungen:**

| Hash          | Zweck                                                 | Berechnung                     |
| ------------- | ----------------------------------------------------- | ------------------------------ |
| **RUML-Hash** | Sicherstellt, dass die Struktur nicht verändert wurde | Wie in Kapitel 3.2.4 definiert |

---

**Verifikation:**

Beim Laden einer RUML-Result-Datei SOLLTEN Implementierungen:

1. Den RUML-Hash gegen die referenzierte RUML-Datei prüfen
2. Bei Abweichungen: Benutzer warnen und Abweichung dokumentieren

---

### 5.1.4 Anwendungsszenarien

| Szenario              | Beschreibung                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| Massenverfahren       | Eine Rulemap wird für viele Fälle ausgewertet — jeder Fall erhält eine eigene `.ruml-result`-Datei |
| Aktensysteme          | Ergebnisse werden in bestehende Aktenstrukturen integriert                                         |
| Langzeitarchivierung  | Trennung von Struktur und Instanz für revisionssichere Aufbewahrung                                |
| Versionierte Rulemaps | Mehrere Ergebnisse können auf verschiedene Versionen derselben Rulemap verweisen                   |
| Mandantentrennung     | Ergebnisse können separat pro Mandant gespeichert werden                                           |
| Einzelfallprüfung     | Auch Einzelfälle werden als `.ruml-result`-Datei gespeichert                                       |

---

### 5.1.5 Vollständiges Beispiel

Das folgende Beispiel zeigt eine RUML-Datei und die zugehörige RUML-Result-Datei. Die Rulemap prüft
die Voraussetzungen für einen Förderantrag.

---

**Datei 1: `foerderantrag.ruml`**

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_age": {
            "name": "Alter des Antragstellers",
            "type": "integer",
            "binding": {
              "type": "input"
            }
          },
          "dp_income": {
            "name": "Jahreseinkommen",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            }
          },
          "dp_hardship": {
            "name": "Härtefall anerkannt",
            "type": "boolean",
            "binding": {
              "type": "input"
            }
          },
          "dp_state": {
            "name": "Bundesland des Wohnsitzes",
            "type": "string",
            "binding": {
              "type": "input"
            }
          }
        }
      }
    },
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:actions"
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z",
    "created": "2024-01-10T09:00:00Z",
    "modified": "2024-01-10T09:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
        "operator": "AND",
        "label": "Fördervoraussetzungen",
        "children": ["2", "3", "6"]
      },
      "2": {
        "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
        "label": "Antragsteller volljährig",
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
        "id": "42d9431d-b7db-404f-bdf9-7ecdde505cce",
        "operator": "XOR",
        "label": "Einkommensprüfung",
        "children": ["4", "5"]
      },
      "4": {
        "id": "52820488-2849-4487-842b-952dc3ba301d",
        "label": "Einkommen unter Grenze",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_income <= 40000"
            }
          }
        ]
      },
      "5": {
        "id": "48b34df4-06bb-4dc2-aeb7-807a146760f4",
        "label": "Härtefall anerkannt",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_hardship = true"
            }
          }
        ]
      },
      "6": {
        "id": "92f909f1-0097-4d9d-87d2-1734bf299d08",
        "label": "Wohnsitz in Bayern",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_state = \"BY\""
            }
          },
          {
            "id": "ruml:actions",
            "payload": {
              "onFalse": {
                "operation": "sendNotification",
                "ref": "notification_service",
                "config": {
                  "template": "antrag-falsches-bundesland",
                  "channel": "email"
                }
              }
            }
          }
        ]
      }
    }
  }
}
```

---

**Datei 2: `foerderantrag-fall-00456.ruml-result`**

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d9c7e5c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e"
  },
  "evaluation": {
    "id": "7f3d1c88-2b4e-4a19-9c5d-0e6f1a2b3c4d",
    "timestamp": "2024-01-15T10:00:00Z",
    "mode": "optimized",
    "caseId": "Antrag-2024-00456",
    "capabilities": [
      {
        "id": "ruml:datapoints"
      },
      {
        "id": "ruml:query"
      },
      {
        "id": "ruml:actions"
      }
    ],
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:04Z",
        "reason": "Alle Voraussetzungen erfüllt (AND: alle Kinder true)"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:01Z",
        "reason": "Alter 25 >= 18",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_age >= 18",
              "inputs": {
                "dp_age": 25
              },
              "result": "true"
            }
          }
        ]
      },
      "1.2": {
        "lexId": "3",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:02Z",
        "reason": "XOR erfüllt: Einkommen unter Grenze"
      },
      "1.2.1": {
        "lexId": "4",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:02Z",
        "reason": "Einkommen 35000 <= 40000",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_income <= 40000",
              "inputs": {
                "dp_income": 35000
              },
              "result": "true"
            }
          }
        ]
      },
      "1.2.2": {
        "lexId": "5",
        "status": "ignored",
        "reason": {
          "type": "shortCircuit",
          "trigger": "Knoten 1.2.1 (lexId: 4) wurde true",
          "operator": "XOR",
          "mode": "optimized"
        }
      },
      "1.3": {
        "lexId": "6",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:03Z",
        "reason": "Wohnsitz BY == BY",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_state = \"BY\"",
              "inputs": {
                "dp_state": "BY"
              },
              "result": "true"
            }
          }
        ]
      }
    }
  }
}
```

---

**Erläuterung des Auswertungsverlaufs:**

1. Knoten 1.1 (Antragsteller volljährig): Alter 25 >= 18 → `true`
2. Knoten 1.2.1 (Einkommen unter Grenze): 35.000 <= 40.000 → `true`
3. Knoten 1.2.2 (Härtefall): Wird nicht ausgewertet (Short-Circuit), da Knoten 1.2.1 bereits `true`
   ist und der Parent-Operator `XOR` ist → `ignored`
4. Knoten 1.2 (Einkommensprüfung): XOR mit `true`, `ignored` → `true`
5. Knoten 1.3 (Wohnsitz): BY == BY → `true`
6. Knoten 1 (Root): AND mit `true`, `true`, `true` → `true`

---

**Beachtenswerte Aspekte:**

- Die RUML-Datei enthält ausschließlich die Regelstruktur — keine Auswertungsergebnisse
- Das `results`-Objekt in der `.ruml-result`-Datei verwendet den **Pfad** als String-Key
- Jedes Knoten-Ergebnis enthält die `lexId` als Pflichtfeld, um die Zuordnung zum Node-Objekt zu
  ermöglichen
- Bei modularen Knoten (siehe [Kapitel 6](../06-modular-nodes/index.md)) existieren mehrere Einträge
  mit unterschiedlichen Pfaden aber derselben `lexId`
- Knoten 1.2.2 demonstriert den `ignored`-Status durch Short-Circuit-Evaluation im `optimized`-Modus
- Capability-spezifische Auswertungsdaten (z.B. Query-Expressions und Eingabewerte) werden im
  `capabilities`-Objekt des jeweiligen Knoten-Ergebnisses dokumentiert
