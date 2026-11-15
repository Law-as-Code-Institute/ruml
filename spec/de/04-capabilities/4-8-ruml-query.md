<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.8 ruml:query

## 4.8 Capability `ruml:query`

### Überblick

| Eigenschaft             | Wert                                                       |
| ----------------------- | ---------------------------------------------------------- |
| **Capability-ID**       | `ruml:query`                                               |
| **Scope**               | Node-Level (`capabilities`-Eintrag mit `id: "ruml:query"`) |
| **Standard `required`** | `false`                                                    |
| **Rolle**               | `decision`                                                 |

Diese Capability definiert datenbasierte Abfragen an Leaf-Nodes, die deren Wahrheitswert ermitteln.
Queries greifen auf DataPoints zu, die über die `ruml:datapoints`-Capability definiert werden (siehe
[Kapitel 4.7](4-7-data-points.md)).

:::note[Abgrenzung zu anderen Capabilities]
Für normative Textreferenzen wird `ruml:text-reference` verwendet (siehe
[Kapitel 4.12](4-12-ruml-text-reference.md)). `ruml:query` deckt ausschließlich datenbasierte
Queries ab. Für KI-gestützte Entscheidungen wird die separate Capability `ruml:ai-query` verwendet
(siehe [Kapitel 4.9](4-9-ruml-ai-query.md)).
:::

### Root-Level-Deklaration

Um `ruml:query` zu verwenden, MUSS die Capability im Root-`capabilities`-Array deklariert werden
([`CAP-15`](../08-validation/index.md#rule-cap-15)):

```jsonc
"capabilities": [
  {
    "id": "ruml:query"
  }
]
```

**Hinweis:** DataPoints werden über die eigenständige `ruml:datapoints`-Capability definiert (siehe
[Kapitel 4.7](4-7-data-points.md)). `ruml:query` greift auf die dort definierten Datenpunkte zu,
enthält selbst aber kein `data`-Objekt.

### Node-Level-Query

An Leaf-Nodes wird die Query im `capabilities`-Array des Knotens bereitgestellt:

```jsonc
"1": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "label": "Einkommen ausreichend",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_annual_income > 50000"
      }
    }
  ]
}
```

#### Felder der Node-Level-Query

| **Feld**      | **Typ** | **Beschreibung**                                                                        |
| ------------- | ------- | --------------------------------------------------------------------------------------- |
| `expression`  | String  | MUSS einen JSONata-Ausdruck zur Berechnung des Wahrheitswerts enthalten ([`CAP-29`](../08-validation/index.md#rule-cap-29)) |
| `description` | String  | DARF eine Beschreibung der Query enthalten ([`CAP-29`](../08-validation/index.md#rule-cap-29))                              |

#### Expression-Format

Expressions MÜSSEN in [JSONata](https://docs.jsonata.org/) 2.2.0 geschrieben sein.

Die Expression wird gegen ein Eingabedokument ausgewertet: ein JSON-Objekt, das den Wert jedes
DataPoints unter dessen ID enthält. Ein DataPoint ohne Wert hat keinen Eintrag.

Das Ergebnis `true` oder `false` ist der Status des Knotens. Jedes andere Ergebnis — auch kein
Ergebnis — **MUSS** den Status `undefined` ergeben.

```jsonc
"expression": "dp_annual_income > 50000"
```

### Auswertungsregeln

- Ein Knoten mit einem `ruml:query`-Eintrag in `capabilities` DARF KEIN nicht-leeres
  `children`-Array haben
- Ein Knoten mit nicht-leerem `children`-Array DARF KEINEN `ruml:query`-Eintrag in `capabilities`
  haben ([`CAP-07`](../08-validation/index.md#rule-cap-07))
- `ruml:query` ermittelt den Wahrheitswert eines Leaf-Nodes; Actions (der `ruml:actions`-Eintrag)
  reagieren auf den Wahrheitswert — beide sind unabhängige Konzepte
- Alle in der Expression referenzierten DataPoint-IDs MÜSSEN in der `ruml:datapoints`-Capability
  definiert sein (referenzielle Integrität, [`DP-18`](../08-validation/index.md#rule-dp-18))

### Kombination mit anderen Capabilities

Ein Knoten kann `ruml:query` mit anderen Capabilities kombinieren:

```jsonc
"1": {
  "id": "fcf02185-ffee-48a4-bf93-d2fb1b17944d",
  "label": "Einkommensprüfung",
  "capabilities": [
    {
      "id": "ruml:text-reference",
      "payload": {
        "refs": [
          {
            "id": "text_sgb_ii_11",
            "type": "refers-to"
          }
        ]
      }
    },
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_annual_income > 50000"
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "onTrue": {
          "operation": "createDocument",
          "ref": "approval_service"
        },
        "onFalse": {
          "operation": "sendNotification",
          "ref": "rejection_service"
        }
      }
    }
  ]
}
```

### Vollständiges Beispiel

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
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
          },
          "dp_credit_score": {
            "name": "Bonitätsscore",
            "type": "number",
            "binding": {
              "type": "external",
              "ref": "schufa_api"
            }
          }
        }
      }
    },
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:text-reference",
      "payload": {
        "data": {
          "text_bgb_488": {
            "title": "§ 488 BGB – Darlehensvertrag",
            "uri": "/akn/de/act/1896-08-18/bgb#sec_488",
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "inForce",
            "type": "embedded",
            "text": "Durch den Darlehensvertrag wird der Darlehensgeber verpflichtet, dem Darlehensnehmer einen Geldbetrag in der vereinbarten Höhe zur Verfügung zu stellen. Der Darlehensnehmer ist verpflichtet, einen geschuldeten Zins zu zahlen und bei Fälligkeit das zur Verfügung gestellte Darlehen zurückzuzahlen."
          }
        }
      }
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
        "operator": "AND",
        "label": "Kreditprüfung",
        "capabilities": [
          {
            "id": "ruml:text-reference",
            "payload": {
              "refs": [
                {
                  "id": "text_bgb_488",
                  "type": "refers-to"
                }
              ]
            }
          }
        ],
        "children": ["2", "3"]
      },
      "2": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Einkommen ausreichend",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "description": "Mindesteinkommensgrenze",
              "expression": "dp_annual_income > 50000"
            }
          }
        ]
      },
      "3": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "label": "Bonität ausreichend",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_credit_score >= 600"
            }
          }
        ]
      }
    }
  }
}
```

### Lieferung via RUML-EXT (Sidecar)

Wenn `ruml:query` über eine RUML-EXT-Datei geliefert wird, werden die Node-Level-Queries im
`nodes`-Objekt (keyed by UUID) bereitgestellt:

```jsonc
{
  "$format": "RUML-EXT",
  "$specVersion": "1.0",
  "$base": {
    "id": "7812e8d0-bd75-437e-9c20-e4f8fb028ced",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "capabilities": [
    {
      "id": "ruml:query"
    }
  ],
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "ruml:query": {
        "expression": "dp_annual_income > 50000"
      }
    }
  }
}
```
