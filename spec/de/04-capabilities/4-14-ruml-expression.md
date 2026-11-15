<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.14 ruml:expression

## 4.14 Capability `ruml:expression`

### Überblick

| Eigenschaft             | Wert                                                                                         |
| ----------------------- | -------------------------------------------------------------------------------------------- |
| **Capability-ID**       | `ruml:expression`                                                                            |
| **Scope**               | Root-Level (Deklaration) und Node-Level (`capabilities`-Eintrag mit `id: "ruml:expression"`) |
| **Standard `required`** | keiner — MUSS als `true` deklariert werden ([`CAP-11`](../08-validation/index.md#rule-cap-11))                                   |
| **Rolle**               | `combiner`                                                                                   |

Diese Capability trägt den Ausdruck, der die Ergebnisse der Kinder eines Knotens verknüpft, wenn der
Knoten `operator: "DELEGATED"` verwendet (siehe
[Kapitel 3.6.4](../03-data-model/3-6-operators.md#364-der-operator-delegated)).

Sie ist der **offizielle Kombinierer**: derjenige, den diese Spezifikation definiert und validiert.
Ein Knoten DARF stattdessen an einen eigenen Kombinierer delegieren — jede auf Root-Level mit der
Rolle `combiner` deklarierte Capability —, der an denselben Kombinierer-Vertrag gebunden ist, dessen
Payload diese Spezifikation aber nicht beschreibt. `ruml:expression` ist daher am besten als
Referenzimplementierung dieses Vertrags zu lesen.

:::note[Abgrenzung zu anderen Capabilities]
`ruml:query` entscheidet einen Leaf-Knoten aus Daten ([Kapitel 4.8](4-8-ruml-query.md)),
`ruml:ai-query` entscheidet einen Leaf-Knoten KI-gestützt ([Kapitel 4.9](4-9-ruml-ai-query.md)).
`ruml:expression` entscheidet einen Parent-Knoten **aus den Ergebnissen seiner Kinder** und setzt
diese deshalb voraus.
:::

### Root-Level-Deklaration

```jsonc
"capabilities": [
  {
    "id": "ruml:expression",
    "required": true
  }
]
```

Eine Datei, die `ruml:expression` verwendet, **MUSS** die Capability mit `required: true`
deklarieren; eine Deklaration, die `required` weglässt oder auf `false` setzt, ist ungültig
([`CAP-11`](../08-validation/index.md#rule-cap-11)). Ein Werkzeug, das die Capability nicht unterstützt, kann die Kinder eines solchen
Knotens auf keine vertretbare Weise verknüpfen; nach Regel `CAP-01` führt die Deklaration
`required: true` dazu, dass es die Datei ablehnt, statt auf einen logischen Operator zurückzufallen
und eine Entscheidung zu erzeugen, die die Rulemap nicht ausspricht.

### Node-Level-Wert

```jsonc
"2": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "operator": "DELEGATED",
  "label": "Mindestens drei Merkmale erfüllt",
  "children": ["3", "4", "5", "6", "7"],
  "capabilities": [
    {
      "id": "ruml:expression",
      "payload": {
        "description": "Mindestens drei der fünf Merkmale müssen erfüllt sein",
        "expression": "$count($children[status = 'true']) >= 3"
      }
    }
  ]
}
```

#### Felder auf Node-Level

| **Feld**      | **Typ** | **Pflicht** | **Beschreibung**                                                                                   |
| ------------- | ------- | ----------- | -------------------------------------------------------------------------------------------------- |
| `expression`  | String  | Ja          | MUSS einen JSONata-Ausdruck enthalten, der den Wahrheitswert des Knotens berechnet ([`CAP-38`](../08-validation/index.md#rule-cap-38)) |
| `description` | String  | Ja          | MUSS die Regel, die der Ausdruck abbildet, in Prosa benennen ([`OP-04`](../08-validation/index.md#rule-op-04))                        |

`description` ist hier Pflicht, obwohl es bei `ruml:query` optional ist. Ein logischer Operator sagt
durch seinen Namen, was ein Knoten tut; `DELEGATED` tut das nicht. Ohne die Angabe in Prosa wäre die
Rulemap nicht mehr lesbar, ohne Code zu lesen. Werkzeuge **SOLLTEN** sie überall dort anzeigen, wo
sie den Operator anzeigen.

#### Format des Ausdrucks

Ausdrücke MÜSSEN in **JSONata** geschrieben sein und MÜSSEN zu `true`, `false` oder keinem Ergebnis
auswerten. Das Eingabedokument ist dasselbe wie bei `ruml:query` — DataPoints werden über ihre ID
angesprochen —, erweitert um die gebundene Variable `$children`:

| Feld     | Typ    | Beschreibung            |
| -------- | ------ | ----------------------- |
| `lexId`  | String | Die lexId des Kindes    |
| `label`  | String | Das Label des Kindes    |
| `status` | String | `"true"` oder `"false"` |

Gebunden sind ausschließlich **direkte** Kinder. Das Array folgt der Reihenfolge des
`children`-Arrays des Knotens.

### Auswertungsregeln

- Ein Knoten mit einem Eintrag `ruml:expression` MUSS `operator: "DELEGATED"` und ein nicht-leeres
  `children`-Array besitzen ([`OP-02`](../08-validation/index.md#rule-op-02), [`CAP-08`](../08-validation/index.md#rule-cap-08))
- Ein Knoten DARF NICHT mehr als einen Eintrag `ruml:expression` führen ([`OP-02`](../08-validation/index.md#rule-op-02))
- Alle Kinder MÜSSEN vor der Auswertung des Ausdrucks ausgewertet werden; der Operator DARF NICHT
  short-circuiten (siehe
  [Kapitel 3.6.4](../03-data-model/3-6-operators.md#364-der-operator-delegated))
- Ist ein Kind `undefined`, ist der Knoten `undefined`, und der Ausdruck DARF NICHT ausgewertet
  werden (siehe [Kapitel 3.6.4](../03-data-model/3-6-operators.md#364-der-operator-delegated));
  `$children` enthält daher nur `"true"` und `"false"`
- Ein Ergebnis, das kein Boolean ist, MUSS den Status `undefined` ergeben
- Ausdrücke SOLLTEN deterministisch sein; `$random`, `$now`, `$millis` und `$eval` DÜRFEN verwendet
  werden (siehe [Kapitel 3.6.4](../03-data-model/3-6-operators.md#364-der-operator-delegated))
  ([`OP-05`](../08-validation/index.md#rule-op-05)). Das Knotenergebnis hält `inputs` und `children` fest, nicht aber die Rückgabewerte
  dieser Funktionen; das Ergebnis eines solchen Ausdrucks lässt sich daher nicht allein aus der
  RUML-Result-Datei reproduzieren
- Alle im Ausdruck referenzierten DataPoint-IDs MÜSSEN in der Capability `ruml:datapoints` definiert
  sein (referenzielle Integrität, [`DP-18`](../08-validation/index.md#rule-dp-18))

### Ausdrucksmuster

| Muster                                                             | Ausdruck                                                                             |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Mindestens _n_ der Kinder                                          | `$count($children[status = "true"]) >= 3`                                            |
| Höchstens _n_ dürfen fehlen                                        | `$count($children[status = "false"]) <= 1`                                           |
| Alle außer einem benannten Kind                                    | `$count($children[lexId != "7" and status = "false"]) = 0`                           |
| Einfache Mehrheit                                                  | `$count($children[status = "true"]) * 2 > $count($children)`                         |
| Qualifizierte Mehrheit (zwei Drittel)                              | `$count($children[status = "true"]) * 3 >= $count($children) * 2`                    |
| Ein bestimmtes Kind entscheidet                                    | `$children[lexId = "4"].status = "true"`                                             |
| Subsidiarität — das zweite greift nur, wenn das erste nicht greift | `$children[lexId = "4"].status = "false" and $children[lexId = "5"].status = "true"` |
| Mindestens eines aus einer benannten Teilmenge                     | `$count($children[lexId in ["4", "5"] and status = "true"]) >= 1`                    |
| Daten überspielen die Kinder (gesetzliche Fiktion)                 | `dp_alter >= 65 or $count($children[status = "true"]) = 3`                           |

Durchgerechnetes Beispiel. Der Knoten hat fünf Kinder und den Ausdruck
`$count($children[status = "true"]) >= 3`:

```jsonc
"$children": [
  {
    "lexId": "4",
    "label": "Merkmal 1",
    "status": "true"
  },
  {
    "lexId": "5",
    "label": "Merkmal 2",
    "status": "false"
  },
  {
    "lexId": "6",
    "label": "Merkmal 3",
    "status": "true"
  },
  {
    "lexId": "7",
    "label": "Merkmal 4",
    "status": "true"
  },
  {
    "lexId": "8",
    "label": "Merkmal 5",
    "status": "false"
  }
]
```

`$children[status = "true"]` wählt die Einträge mit den lexIds `4`, `6` und `7`; `$count` davon ist
`3`; `3 >= 3` ist `true`, der Status des Knotens also `true`.

:::caution[Kinder über `lexId` ansprechen, nicht über die Position]
`$children[0]` ist das **erste** Kind (JSONata-Array-Indizes beginnen bei null), `$children[1]` das
zweite. `$children[lexId = "4"]` wählt dagegen über die Identität. Positionsbezogene Ausdrücke
ändern ihre Bedeutung stillschweigend, sobald ein Kind eingefügt, entfernt oder umgestellt wird — in
einer Rulemap, die mehrere Novellierungen überdauert, kodiert ein Ausdruck so am Ende eine andere
Regel als die, die geprüft wurde. Wo ein bestimmtes Kind gemeint ist, wird die Adressierung über
`lexId` daher EMPFOHLEN.
:::

### Kombination mit anderen Capabilities

Ein Knoten mit `operator: "DELEGATED"` führt genau einen Kombinierer, DARF daneben aber Capabilities
der Rollen `data` und `reaction` führen, in beliebiger Reihenfolge ([`CAP-16`](../08-validation/index.md#rule-cap-16)):

```jsonc
"2": {
  "id": "fcf02185-ffee-48a4-bf93-d2fb1b17944d",
  "operator": "DELEGATED",
  "label": "Härtefall liegt vor",
  "children": ["4", "5", "6"],
  "capabilities": [
    {
      "id": "ruml:text-reference",
      "payload": {
        "refs": [
          {
            "id": "text_sgb_xii_90",
            "type": "represents"
          }
        ]
      }
    },
    {
      "id": "ruml:expression",
      "payload": {
        "description": "Mindestens zwei der drei Härtefallmerkmale müssen vorliegen",
        "expression": "$count($children[status = \"true\"]) >= 2"
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "onTrue": {
          "operation": "createDocument",
          "ref": "haertefall_bescheid"
        }
      }
    }
  ]
}
```

Die Textreferenz liefert die Norm, die die Regel umsetzt, der Kombinierer entscheidet den Knoten,
und die Action reagiert auf den entschiedenen Status. Nur der Kombinierer beeinflusst den Status.

### Eigene Kombinierer

Ein Knoten DARF stattdessen an einen nicht-offiziellen Kombinierer delegieren. Die Capability wird
auf Root-Level mit der Rolle `combiner` deklariert, da ein Parser die Rolle einer fremden Capability
nicht aus ihrer ID erschließen kann (siehe [Kapitel 4.1](4-1-concept.md)):

```jsonc
"capabilities": [
  {
    "id": "com.example/expression",
    "required": true,
    "role": "combiner"
  }
]
```

```jsonc
"1": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "operator": "DELEGATED",
  "label": "Gewichtete Gesamtbewertung",
  "children": ["2", "3", "4"],
  "capabilities": [
    {
      "id": "com.example/expression",
      "payload": {
        "description": "Gewichtete Punktsumme ab 27 Punkten",
        "expression": "weightedScore(children) >= 27"
      }
    }
  ]
}
```

Die Gestalt des Payloads bestimmt der Anbieter, nicht diese Spezifikation — der Kombinierer-Vertrag
aus [Kapitel 3.6.4](../03-data-model/3-6-operators.md#364-der-operator-delegated) bindet ihn
gleichwohl: Boolean-Ergebnis, `description` in Prosa, `undefined` bei einem unbestimmten Kind und
kein Short-Circuit. Eine mit `role: "decision"` deklarierte Capability entscheidet ein Blatt aus
Daten und DARF hier NICHT verwendet werden; ihr würden Kinder übergeben, die sie nie liest.

### Payload im Knotenergebnis

Das Knotenergebnis hält fest, was der Ausdruck gesehen hat, damit die Entscheidung allein aus der
RUML-Result-Datei nachvollzogen werden kann (siehe
[Kapitel 5.1](../05-result-format/5-1-result-model.md)):

| Feld         | Typ    | Pflicht | Beschreibung                                                                                                                   |
| ------------ | ------ | ------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `expression` | String | Ja      | Der ausgewertete Ausdruck                                                                                                      |
| `inputs`     | Object | Ja      | Aufgelöste DataPoint-Werte, die der Ausdruck referenziert, indiziert nach DataPoint-ID; ein leeres Objekt, wenn er keine liest |
| `children`   | Array  | Ja      | Die vom Ausdruck gesehenen Kind-Ergebnisse als `{ lexId, status }`, in der Reihenfolge von `children`                          |
| `result`     | Enum   | Ja      | Berechnetes Ergebnis: `true`, `false`, `undefined`                                                                             |

Weitere Felder sind NICHT zulässig.

```jsonc
"1.2": {
  "lexId": "3",
  "status": "true",
  "evaluatedAt": "2024-01-15T10:00:04Z",
  "reason": "3 von 5 Merkmalen erfüllt (Schwelle: 3)",
  "capabilities": [
    {
      "id": "ruml:expression",
      "payload": {
        "expression": "$count($children[status = 'true']) >= 3",
        "inputs": {},
        "children": [
          {
            "lexId": "4",
            "status": "true"
          },
          {
            "lexId": "5",
            "status": "false"
          },
          {
            "lexId": "6",
            "status": "true"
          },
          {
            "lexId": "7",
            "status": "true"
          },
          {
            "lexId": "8",
            "status": "false"
          }
        ],
        "result": "true"
      }
    }
  ]
}
```

`inputs` ist oben leer, weil dieser Ausdruck allein `$children` liest. Ein Ausdruck DARF auch
DataPoints lesen — sie werden genau wie bei `ruml:query` angesprochen —, und dann MÜSSEN die Werte,
die den Knoten mitbestimmt haben, festgehalten werden; sonst erklärt die Result-Datei das Ergebnis
nicht:

```jsonc
"1.3": {
  "lexId": "9",
  "status": "true",
  "reason": "Fiktion: Antragsteller ist 67 Jahre alt",
  "capabilities": [
    {
      "id": "ruml:expression",
      "payload": {
        "expression": "dp_alter >= 65 or $count($children[status = 'true']) = 3",
        "inputs": {
          "dp_alter": 67
        },
        "children": [
          {
            "lexId": "10",
            "status": "true"
          },
          {
            "lexId": "11",
            "status": "false"
          },
          {
            "lexId": "12",
            "status": "false"
          }
        ],
        "result": "true"
      }
    }
  ]
}
```

Nur eines der drei Kinder ist `true`; ohne `inputs` zeigte das festgehaltene Ergebnis also einen
Knoten, der gegen seine eigenen Kinder `true` entschieden wurde, ohne dass etwas dies erklärte. Für
diesen Fall gibt es das Feld.

### Vollständiges Beispiel

Eine Härtefallprüfung: Mindestens zwei von drei Merkmalen müssen vorliegen, und der Antragsteller
muss seinen Wohnsitz im Land haben.

**Datei 1: `haertefall.ruml`**

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_pflegegrad": {
            "name": "Pflegegrad",
            "type": "integer",
            "binding": {
              "type": "input"
            }
          },
          "dp_eigenanteil": {
            "name": "Monatlicher Eigenanteil",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            }
          },
          "dp_alleinlebend": {
            "name": "Alleinlebend",
            "type": "boolean",
            "binding": {
              "type": "input"
            }
          },
          "dp_wohnsitz": {
            "name": "Wohnsitz im Land",
            "type": "boolean",
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
      "id": "ruml:expression",
      "required": true
    }
  ],
  "metadata": {
    "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
    "version": "1.0.0",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z",
    "created": "2024-01-10T09:00:00Z",
    "modified": "2024-01-10T09:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
        "operator": "AND",
        "label": "Härtefallleistung",
        "children": ["2", "7"]
      },
      "2": {
        "id": "42d9431d-b7db-404f-bdf9-7ecdde505cce",
        "operator": "DELEGATED",
        "label": "Härtefall liegt vor",
        "children": ["3", "4", "5"],
        "capabilities": [
          {
            "id": "ruml:expression",
            "payload": {
              "description": "Mindestens zwei der drei Härtefallmerkmale müssen vorliegen",
              "expression": "$count($children[status = \"true\"]) >= 2"
            }
          }
        ]
      },
      "3": {
        "id": "52820488-2849-4487-842b-952dc3ba301d",
        "label": "Pflegegrad mindestens 3",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_pflegegrad >= 3"
            }
          }
        ]
      },
      "4": {
        "id": "48b34df4-06bb-4dc2-aeb7-807a146760f4",
        "label": "Eigenanteil über 800 EUR",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_eigenanteil > 800"
            }
          }
        ]
      },
      "5": {
        "id": "92f909f1-0097-4d9d-87d2-1734bf299d08",
        "label": "Alleinlebend",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_alleinlebend = true"
            }
          }
        ]
      },
      "7": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "label": "Wohnsitz im Land",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_wohnsitz = true"
            }
          }
        ]
      }
    }
  }
}
```

**Datei 2: `haertefall-fall-00123.ruml-result`**

Der Knoten `1.1.2` ist `false`, und dennoch ist kein Kind `ignored`: Der Operator `DELEGATED` wertet
alle aus, weil die Zählung sonst über eine unvollständige Menge ginge.

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "b6620b3c-4279-4a45-9115-c8bb2032d868"
  },
  "evaluation": {
    "id": "7f3d1c88-2b4e-4a19-9c5d-0e6f1a2b3c4d",
    "timestamp": "2024-01-15T10:00:00Z",
    "mode": "complete",
    "caseId": "Antrag-2024-00123",
    "capabilities": [
      {
        "id": "ruml:datapoints"
      },
      {
        "id": "ruml:query"
      },
      {
        "id": "ruml:expression"
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
        "reason": "2 von 3 Merkmalen erfüllt (Schwelle: 2)",
        "capabilities": [
          {
            "id": "ruml:expression",
            "payload": {
              "expression": "$count($children[status = \"true\"]) >= 2",
              "inputs": {},
              "children": [
                {
                  "lexId": "3",
                  "status": "true"
                },
                {
                  "lexId": "4",
                  "status": "false"
                },
                {
                  "lexId": "5",
                  "status": "true"
                }
              ],
              "result": "true"
            }
          }
        ]
      },
      "1.1.1": {
        "lexId": "3",
        "status": "true",
        "reason": "Pflegegrad 4 >= 3"
      },
      "1.1.2": {
        "lexId": "4",
        "status": "false",
        "reason": "Eigenanteil 640 EUR <= 800 EUR"
      },
      "1.1.3": {
        "lexId": "5",
        "status": "true",
        "reason": "Alleinlebend"
      },
      "1.2": {
        "lexId": "7",
        "status": "true",
        "reason": "Wohnsitz im Land"
      }
    }
  }
}
```

### Nicht über RUML-EXT (Sidecar) lieferbar

`ruml:expression` DARF NICHT in einer RUML-EXT-Datei geliefert werden; die ID fehlt im
RUML-EXT-Schema bewusst ([`CAP-37`](../08-validation/index.md#rule-cap-37)).

Eine RUML-EXT-Datei erweitert Knoten, die in der Basisdatei bereits vorhanden sind
([Kapitel 4.5](4-5-ruml-ext.md)). Ein Basisknoten mit `operator: "DELEGATED"` und Kindern führt
seinen Kombinierer bereits (Regel `OP-02`), und ein zweiter verstieße gegen Regel `OP-02`; an einem
Leaf-Node fehlen `ruml:expression` die Kinder, die es voraussetzt, und an jedem anderen Knoten
verstößt es gegen Regel `CAP-08`. Ein Sidecar hat also keinen Knoten, an dem er den Eintrag gültig
ergänzen könnte. Die Beschränkung folgt damit aus den Bindungsregeln und ist keine zusätzliche.

Das ist beabsichtigt: `ruml:text-reference` oder `ruml:context` ergänzen Material **zu** einer
Entscheidung, `ruml:expression` **ist** die Entscheidung. Was eine Rulemap entscheidet, gehört in
die signierte und gehashte Basisdatei und nicht in eine Begleitdatei, die fehlen kann.

### Geplante Erweiterung: Werte aus dem Teilbaum

Schwellenwertregeln über eine **Anzahl** erfüllter Kinder sind allein mit `$children[].status`
abgedeckt. Regeln über eine **Summe** — punktbasierte Bewertungen, aufsummierte Beträge — benötigen
zusätzlich eine Zahl je Knoten, die RUML bisher nicht führt.

Die vorgesehene Richtung ist, dass ein Knoten einen Eintrag `ruml:datapoints` auf Node-Level
deklarieren darf, dessen Einträge `binding.type: "computed"` verwenden und damit einen DataPoint aus
dem Geltungsbereich dieses Knotens bestimmen; der bestimmte Wert wäre dann auf `$children[]` über
seine DataPoint-ID lesbar. Diese Erweiterung ist **nicht** Teil dieses Kapitels und noch nicht im
Schema; die unter _Format des Ausdrucks_ aufgeführten Felder sind vollständig.
