<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.3 Capability-Daten am Knoten

### Überblick

Jeder Knoten DARF ein eigenes `capabilities`-Feld tragen — unabhängig vom gleichnamigen
`capabilities`-Array auf Root-Ebene (siehe [Kapitel 4.2](4-2-capabilities-field.md)). Es enthält die
Erweiterungsdaten für die auf diesem Knoten anwendbaren Capabilities.

Das Feld ist Teil der optionalen Felder des Node-Objekts (siehe
[Kapitel 3.5.3](../03-data-model/3-5-node-object.md)) und unterliegt denselben allgemeinen Regeln:
Es braucht nicht vorhanden zu sein; sein Fehlen hat keine Auswirkung auf die Kernverarbeitung.

### Struktur

```jsonc
"capabilities": [
  {
    "id": "ruml:query",
    "payload": {/* ... */}
  },
  {
    "id": "ruml:draft/ai-annotations",
    "payload": {/* ... */}
  }
]
```

- **`id`:** Eine Capability-ID, die im Root-Level-`capabilities`-Array deklariert ist.
- **`payload`:** Ein Objekt, dessen innere Struktur durch die jeweilige Capability-Spezifikation
  definiert ist.

Beide Felder sind Pflicht: Jeder Eintrag MUSS `id` und `payload` enthalten ([`CAP-17`](../08-validation/index.md#rule-cap-17)). Eine
Capability ohne Daten auf Knotenebene, etwa `ruml:protocol`, DARF deshalb NICHT im
`capabilities`-Array eines Knotens vorkommen ([`CAP-18`](../08-validation/index.md#rule-cap-18)).

### Referenzielle Integrität

Die `id` jedes Eintrags im `capabilities`-Array eines Knotens MUSS eine Capability-ID sein, die im
Root-Level-`capabilities`-Array deklariert ist ([`CAP-15`](../08-validation/index.md#rule-cap-15)).

:::warning[Ungültige Capability-Referenz]
Wenn das `capabilities`-Array eines Knotens einen Eintrag enthält, dessen `id` **nicht** im
Root-Level-`capabilities`-Array deklariert ist, MUSS der Parser dies als Validierungsfehler
behandeln ([`CAP-15`](../08-validation/index.md#rule-cap-15)). Diese Regel gilt unabhängig davon, ob der Parser die Capability
inhaltlich kennt oder nicht.
:::

**Ungültig** — `org.ruml.test/decision` ist nicht im Root-`capabilities`-Array deklariert:

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "org.ruml.test/data",
      "role": "data"
    }
  ],
  "metadata": {
    "id": "fa906bd6-24f1-47f3-8ad5-ae3d5c745b56",
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
        "label": "Anspruch auf Schadensersatz",
        "capabilities": [
          {
            "id": "org.ruml.test/decision",
            "payload": {
              "result": "true"
            }
          }
        ]
      }
    }
  }
}
```

**Gültig** — Capability korrekt deklariert:

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "com.example/review-notes",
      "role": "data"
    }
  ],
  "metadata": {
    "id": "dc456c3b-cfa6-44a8-9617-cb5119bbe1ee",
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
        "label": "Anspruch auf Schadensersatz",
        "capabilities": [
          {
            "id": "com.example/review-notes",
            "payload": {
              "status": "pending"
            }
          }
        ]
      }
    }
  }
}
```

### Anwendbarkeit auf Knotentypen

Das `capabilities`-Feld DARF auf jedem Knotentyp vorkommen: Root-Node, Parent-Node und Leaf-Node
([`CAP-16`](../08-validation/index.md#rule-cap-16)).

**Einschränkung für entscheidungsrelevante Capabilities:** Capabilities mit der Rolle `decision`
DÜRFEN NICHT auf andere Knoten als Leaf-Nodes angewendet werden ([`CAP-07`](../08-validation/index.md#rule-cap-07)). Der Status von
Root- und Parent-Nodes ergibt sich ausschließlich aus der Baumstruktur und den Operatoren (siehe
[Kapitel 3.6](../03-data-model/3-6-operators.md)). Die Rolle jeder Capability ist in deren
Spezifikation definiert (siehe [Kapitel 4.1](4-1-concept.md)).

Capabilities mit der Rolle `data` oder `reaction` DÜRFEN auf beliebigen Knotentypen vorkommen
([`CAP-16`](../08-validation/index.md#rule-cap-16)).

Ebenso DARF es auf modularen Knoten (`modular: true`) und auf Knoten innerhalb modularer Teilbäume
vorkommen. Bei modularen Knoten gelten die `capabilities`-Daten für **alle Instanziierungen** des
Knotens (siehe [Kapitel 3.5.3](../03-data-model/3-5-node-object.md)).

### Wiederholte Capability-IDs

Anders als im Array auf Root-Level, dessen IDs eindeutig sind (siehe
[Kapitel 4.2](4-2-capabilities-field.md#eindeutigkeitsregel)), DARF das `capabilities`-Array eines
Knotens dieselbe `id` mehrfach enthalten, wenn die Rolle der Capability es zulässt (siehe
[Kapitel 4.1](4-1-concept.md)):

| **Rolle**  | **Dieselbe `id` mehrfach an einem Knoten**                                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `data`     | DARF NICHT. Ein Eintrag trägt alle Daten des Knotens für diese Capability.                                                                       |
| `decision` | DARF, z. B. zwei `ruml:query`-Einträge mit verschiedenen Ausdrücken; `decisionMode` kombiniert ihre Ergebnisse.                                  |
| `combiner` | DARF NICHT. Ein Knoten führt ohnehin höchstens einen Kombinierer ([`OP-02`](../08-validation/index.md#rule-op-02)).                                                                 |
| `reaction` | DARF, z. B. zwei `ruml:actions`-Einträge; sie werden in Listenreihenfolge verarbeitet (siehe [Reihenfolge der Felder](#reihenfolge-der-felder)). |

Die Regel zählt Einträge mit derselben `id`, nicht Einträge mit derselben Rolle: Ein Knoten DARF
`ruml:text-reference` und `ruml:context` nebeneinander führen. Das Schema erzwingt sie für die
offiziellen `data`-Capabilities; für `ruml:draft/`- und Drittanbieter-IDs ergibt sich die Rolle aus
der Deklaration auf Root-Level, daher ist die Prüfung eine Parser-Pflicht ([`CAP-06`](../08-validation/index.md#rule-cap-06)).

### Payload-Typ

Das `payload` MUSS ein Objekt sein ([`CAP-17`](../08-validation/index.md#rule-cap-17)). Arrays, primitive Werte und `null` DÜRFEN NICHT
verwendet werden; eine Capability, die eine Liste trägt, legt sie in einem benannten Feld des
Objekts ab. Die innere Struktur des Objekts ist durch die Capability-Spezifikation definiert.

```jsonc
"capabilities": [
  {
    "id": "com.example/review-notes",
    "payload": {
      "status": "approved",
      "reviewer": "rechtsabteilung"
    }
  },
  {
    "id": "ruml:draft/ai-annotations",
    "payload": {
      "annotations": [
        {
          "type": "confidence",
          "value": 0.92
        },
        {
          "type": "source",
          "value": "gpt-4o"
        }
      ]
    }
  }
]
```

### Vollständiges Knotenbeispiel

Das folgende Beispiel zeigt einen Leaf-Node mit zwei verschiedenen Capability-Erweiterungen:

```jsonc
"2": {
  "id": "f32b5875-2557-499a-a9b5-bd5efdeab0fd",
  "label": "Volljährigkeit nachgewiesen",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_age >= 18"
      }
    },
    {
      "id": "ruml:draft/ai-annotations",
      "payload": {
        "confidence": 0.97,
        "lastReviewed": "2024-09-15",
        "reviewer": "llm-assistant-v2"
      }
    }
  ]
}
```

### Kombinationsmodus (`decisionMode`)

Wenn ein Leaf-Node mehrere Capabilities mit der Rolle `decision` enthält, bestimmt das optionale
Feld `decisionMode` am Knoten, wie die Ergebnisse kombiniert werden:

| `decisionMode` | Verhalten                                                                                                                                                                                                                                                                                                                           |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fallback`     | Capabilities werden in Listenreihenfolge ausgewertet. Die erste definitive Antwort (`true`/`false`) bestimmt den Knotenstatus. Bei `undefined` wird die nächste decision-Capability ausgewertet; gibt keine eine definitive Antwort, ist das Ergebnis `undefined`. Dies ist der **Standard** wenn `decisionMode` nicht gesetzt ist. |
| `agreement`    | Alle decision-Capabilities MÜSSEN übereinstimmen. Alle MÜSSEN ausgewertet werden. Bei Widerspruch (z.B. eine ergibt `true`, eine andere `false`) ist das Ergebnis `undefined`.                                                                                                                                                      |
| `majority`     | Mehrheitsentscheidung über alle decision-Capabilities. Alle MÜSSEN ausgewertet werden. Bei Gleichstand ist das Ergebnis `undefined`.                                                                                                                                                                                                |

Beispiel:

```jsonc
"3": {
  "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
  "label": "Antragsteller volljährig",
  "decisionMode": "fallback",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_age >= 18"
      }
    },
    {
      "id": "ruml:ai-query",
      "payload": {
        "model": "fast",
        "prompt": "Ist der Antragsteller volljährig?"
      }
    }
  ]
}
```

**Regeln:**

- `decisionMode` ist ein optionales Feld am Node-Objekt (siehe
  [Kapitel 3.5.3](../03-data-model/3-5-node-object.md)), NICHT im `capabilities`-Array.
- `decisionMode` wirkt nur bei Leaf-Nodes. Bei Parent-Nodes MUSS es ignoriert werden
  ([`CAP-19`](../08-validation/index.md#rule-cap-19)).
- Wenn ein Leaf-Node genau eine `decision`-Capability hat, ist `decisionMode` irrelevant und SOLLTE
  NICHT gesetzt werden.
- Bei `fallback` bestimmt die Reihenfolge der Einträge in der `capabilities`-Liste die
  Auswertungsreihenfolge. Autoren SOLLTEN die bevorzugte decision-Capability an die erste Stelle
  setzen.

### Reihenfolge der Felder

Die `capabilities`-Liste ist geordnet, und die Reihenfolge ist signifikant: Capabilities werden in
Listenreihenfolge verarbeitet, und Tools MÜSSEN sie beim Lesen und Schreiben erhalten und DÜRFEN die
Einträge NICHT umsortieren — etwa nach Capability-ID ([`CAP-20`](../08-validation/index.md#rule-cap-20)). Ein Umsortieren der Einträge
ist eine Änderung am Dokument und keine Formatierungsfrage — bei `decisionMode: "fallback"` ändert
es, welche Capability den Knoten entscheidet.

### Verhältnis zu `metadata` auf Node-Ebene

Das optionale `metadata`-Feld eines Knotens (siehe
[Kapitel 3.5.3](../03-data-model/3-5-node-object.md)) ist für **nicht-strukturelle** Informationen
vorgesehen, die keiner Capability zugeordnet sind. Das `capabilities`-Feld ist für **deklarierte,
capability-gebundene** Erweiterungsdaten vorgesehen. Beide Felder DÜRFEN gleichzeitig vorhanden
sein.

```jsonc
"4": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "label": "Ausnahmetatbestand",
  "metadata": {
    "author": "Dr. Müller",
    "lastEditedBy": "validator-bot"
  },
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_age >= 18"
      }
    }
  ]
}
```

## Konformitätstests

- [4.3 Capability Data on Nodes](../../../tests/04-capabilities/4-3-capabilities-node-field.test.yaml)
