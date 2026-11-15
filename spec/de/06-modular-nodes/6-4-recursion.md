<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.4 Rekursion

Modulare Knoten **DÜRFEN** sich selbst als Kind enthalten (Rekursion). ([`MOD-02`](../08-validation/index.md#rule-mod-02)) Dies
ermöglicht die Modellierung von Prozessen mit unbekannter Iterationstiefe, wie z.B.
Vertragsverhandlungen.

---

### Struktur rekursiver Knoten

Ein rekursiver Knoten ist ein modularer Knoten, der seine eigene `lexId` im `children`-Array
enthält:

```jsonc
"4": {
  "id": "7d3f2a91-5c6e-4b8a-9f1d-2e4c6a8b0d13",
  "modular": true,
  "operator": "XOR",
  "label": "Verhandlungsrunde",
  "children": [
    "5",
    "6",
    "4" // ← Selbstreferenz
  ]
}
```

---

### Sichere Rekursion

Rekursion kann zu Endlosschleifen führen. Eine sichere Rekursion ist **NUR** möglich, wenn **BEIDE**
Bedingungen erfüllt sind:

1. Der Operator des rekursiven Knotens ist `XOR` oder `NOT_XOR`
2. Der rekursive Selbstverweis ist **NICHT** als erstes Kind positioniert

**Begründung:** Bei `XOR`/`NOT_XOR` wird die Auswertung beendet, sobald ein Kind `true` wird. Wenn
ein nicht-rekursives Kind (Exit-Bedingung) vor dem Selbstverweis `true` wird, endet die Auswertung –
die Rekursion wird nicht betreten.

---

### Maximale Rekursionstiefe

Implementierungen **MÜSSEN** eine maximale Rekursionstiefe definieren, um Endlosschleifen zu
verhindern:

| Aspekt                       | Anforderung                                                                                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Standard-Maximum             | 500 Ebenen                                                                                                                                                  |
| Konfigurierbarkeit           | **SOLLTE** konfigurierbar sein                                                                                                                              |
| Verhalten bei Überschreitung | Knoten erhält Status `undefined` mit einer Begründung vom Typ `error` (siehe [5.0](../05-result-format/5-0-status-types.md)); der Fehler wird protokolliert |

Die Rekursionstiefe einer Knoteninstanz zählt die Selbstreferenzen auf ihrem Pfad: Die erste Instanz
eines rekursiven Knotens hat die Tiefe 0, und jedes Mal, wenn der Knoten sich selbst enthält, wächst
die Tiefe um 1. Im [vollständigen Beispiel](#vollständiges-beispiel) unten:

| Pfad      | Instanz                              | Rekursionstiefe |
| --------- | ------------------------------------ | --------------- |
| `1.2`     | Verhandlungsrunde (lexId 4), Runde 1 | 0               |
| `1.2.3`   | Verhandlungsrunde (lexId 4), Runde 2 | 1               |
| `1.2.3.3` | Verhandlungsrunde (lexId 4), Runde 3 | 2               |

Bei einem Maximum von _n_ werden Instanzen bis zur Tiefe _n_ ausgewertet; die Instanz mit der Tiefe
_n_ + 1 erhält den Status `undefined`. Die Rekursionstiefe ist nicht die Tiefe des Pfads: Knoten
oberhalb des rekursiven Knotens zählen nicht mit.

---

### Vollständiges Beispiel

**Use Case:** Vertragsverhandlung mit beliebig vielen Runden

**Struktur:**

```
Root (AND, lexId: 1)
├── Vertragsfähigkeit geprüft (Leaf, lexId: 2)
└── Verhandlungsrunde (XOR, lexId: 4, modular, rekursiv)
    ├── Angebot angenommen (Leaf, lexId: 5)
    ├── Verhandlung abgebrochen (Leaf, lexId: 6)
    └── [Rekursion → lexId: 4]
```

---

**RUML-Datei (statisch):**

```jsonc
"rulemap": {
  "nodes": {
    "1": {
      "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
      "operator": "AND",
      "label": "Vertragsabschluss",
      "children": ["2", "4"]
    },
    "2": {
      "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
      "label": "Vertragsfähigkeit geprüft",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_legal_capacity = true"
          }
        }
      ]
    },
    "4": {
      "id": "7d3f2a91-5c6e-4b8a-9f1d-2e4c6a8b0d13",
      "modular": true,
      "operator": "XOR",
      "label": "Verhandlungsrunde",
      "children": ["5", "6", "4"]
    },
    "5": {
      "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
      "label": "Angebot angenommen",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_offer_accepted = true"
          }
        }
      ]
    },
    "6": {
      "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
      "label": "Verhandlung abgebrochen",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_negotiation_cancelled = true"
          }
        }
      ]
    }
  }
}
```

**Auswertungsergebnis nach zwei Verhandlungsrunden:**

Szenario: Erste Runde – kein Ergebnis, zweite Runde – Angebot angenommen.

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d9c7e5c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e"
  },
  "evaluation": {
    "id": "20453004-30ad-4a39-9be3-0c687754948f",
    "timestamp": "2024-01-15T10:00:00Z",
    "mode": "optimized",
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "reason": "AND: alle Kinder true"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "reason": "Vertragsfähigkeit bestätigt"
      },
      "1.2": {
        "lexId": "4",
        "status": "true",
        "reason": "XOR: Kind 1.2.3 ist true (Rekursion betreten)"
      },
      "1.2.1": {
        "lexId": "5",
        "status": "false",
        "reason": "Angebot nicht angenommen"
      },
      "1.2.2": {
        "lexId": "6",
        "status": "false",
        "reason": "Verhandlung nicht abgebrochen"
      },
      "1.2.3": {
        "lexId": "4",
        "status": "true",
        "reason": "XOR: Angebot angenommen (Rekursionsebene 1)"
      },
      "1.2.3.1": {
        "lexId": "5",
        "status": "true",
        "reason": "Angebot angenommen"
      },
      "1.2.3.2": {
        "lexId": "6",
        "status": "ignored",
        "reason": {
          "type": "shortCircuit",
          "trigger": "Knoten 1.2.3.1 wurde true",
          "operator": "XOR",
          "mode": "optimized"
        }
      },
      "1.2.3.3": {
        "lexId": "4",
        "status": "ignored",
        "reason": {
          "type": "shortCircuit",
          "trigger": "Knoten 1.2.3.1 wurde true",
          "operator": "XOR",
          "mode": "optimized"
        }
      }
    }
  }
}
```

**Hinweis:** Die Pfade `1.2.3`, `1.2.3.1`, `1.2.3.2` und `1.2.3.3` im `results`-Objekt sind
dynamisch generiert — sie werden zur Laufzeit aus der Baumstruktur berechnet.

---

### UI-Darstellung

Implementierungen **SOLLTEN** rekursive Knoten visuell kennzeichnen:

| Aspekt              | Empfehlung                                          |
| ------------------- | --------------------------------------------------- |
| **Symbol**          | Spezielles Icon zur Kennzeichnung rekursiver Knoten |
| **Expansion**       | Klick auf Symbol öffnet die nächste Rekursionsebene |
| **Tiefenanzige**    | Anzeige der aktuellen Rekursionstiefe               |
| **Maximum-Warnung** | Warnung bei Annäherung an die maximale Tiefe        |

---

### Validierungsregeln

| Regel                                  | Beschreibung                                                                                                                                                                                                                                                                                            |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Selbstreferenz nur bei `modular: true` | Ein Knoten ohne `modular: true` **DARF** sich **NICHT** selbst referenzieren ([`MOD-01`](../08-validation/index.md#rule-mod-01))                                                                                                                                                                                                            |
| Operator-Empfehlung                    | Rekursive Knoten **SOLLTEN NICHT** den Operator `AND`, `NOT_AND`, `OR` oder `NOT_OR` verwenden, da dies zu potenziell nie auflösbarer Entscheidungslogik führen kann                                                                                                                                    |
| Laufzeit-Warnung                       | Implementierungen **MÜSSEN** eine Warnung ausgeben, wenn ein rekursiver Knoten mit `AND`, `NOT_AND`, `OR` oder `NOT_OR` betrieben wird. Diese Warnung ist keine Zyklenerkennung (Tiefenlimit, siehe Maximale Rekursionstiefe), sondern ein Hinweis auf semantisch blockierte Auswertung ([`MOD-03`](../08-validation/index.md#rule-mod-03)) |
| Position der Selbstreferenz            | Die Selbstreferenz **DARF NICHT** an Position 0 im `children`-Array stehen ([`MOD-04`](../08-validation/index.md#rule-mod-04))                                                                                                                                                                                                              |
| Mindestens eine Exit-Bedingung         | Rekursive Knoten **MÜSSEN** mindestens ein nicht-rekursives Kind haben ([`MOD-05`](../08-validation/index.md#rule-mod-05))                                                                                                                                                                                                                  |

**Hinweis:** Die Validierung dieser Regeln wird in Kapitel 8 definiert.
