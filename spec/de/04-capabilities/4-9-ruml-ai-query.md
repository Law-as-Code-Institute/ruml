<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.9 ruml:ai-query

## 4.9 Capability `ruml:ai-query`

### Überblick

| Eigenschaft             | Wert                                       |
| ----------------------- | ------------------------------------------ |
| **Capability-ID**       | `ruml:ai-query`                            |
| **Scope**               | Node-Level (`capabilities`-Feld am Knoten) |
| **Standard `required`** | `false`                                    |
| **Rolle**               | `decision`                                 |

Die `ruml:ai-query`-Capability ergänzt Leaf-Nodes um LLM-basierte Auswertung. Die Baumstruktur der
Rulemap grenzt die Fragestellung so weit ein, dass das LLM eine klar definierte Prüfung beantwortet
— das Ergebnis MUSS `true`, `false` oder `undefined` sein. Die Auswertung ist dabei nicht im
gleichen Maße deterministisch wie eine `ruml:query`-Expression, aber durch die enge Fragestellung
und konfigurierbare Parameter (z.B. `temperature`) lässt sich eine hohe Reproduzierbarkeit
erreichen.

Wenn ein Knoten sowohl `ruml:query` als auch `ruml:ai-query` enthält, bestimmt das Feld
`decisionMode` am Knoten, wie die Ergebnisse kombiniert werden (siehe
[Kapitel 4.3](4-3-capabilities-node-field.md)). Im Standardmodus `fallback` wird `ruml:ai-query` nur
ausgeführt, wenn `ruml:query` `undefined` zurückgibt.

### Datenstruktur am Knoten

Der `payload` des `ruml:ai-query`-Eintrags im `capabilities`-Array eines Knotens hat folgende
Struktur:

```jsonc
"payload": {
  "model": "strong",
  "prompt": "Prüfe anhand der bereitgestellten Unterlagen, ob eine Härtefallbegründung plausibel ist. Antworte ausschließlich mit true, false oder undefined.",
  "description": "Prüft die Plausibilität der Härtefallbegründung",
  "inputs": {
    "context": [
      {
        "id": "ctx_guidelines",
        "role": "reference"
      },
      {
        "id": "ctx_gutachten",
        "role": "subject"
      }
    ],
    "dataPoints": ["dp_hardship_reason", "dp_annual_income"],
    "texts": ["text_bgb_823"]
  },
  "config": {
    "deterministic": true,
    "effort": "high",
    "temperature": 0.1
  }
}
```

### Felder

| **Feld**      | **Typ** | **Beschreibung**                                                                                                                                                                                       |
| ------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `model`       | String  | MUSS eine symbolische Referenz auf das zu verwendende KI-Modell enthalten ([`CAP-30`](../08-validation/index.md#rule-cap-30))                                                                                                              |
| `prompt`      | String  | DARF den Prompt-Text inline in der RUML-Datei angeben. Wenn vorhanden, wird dieser Prompt verwendet — andernfalls wird die im Tool konfigurierte Prompt-Vorlage des Modells verwendet ([`CAP-30`](../08-validation/index.md#rule-cap-30)). |
| `description` | String  | DARF die Aufgabe des AI Queries beschreiben ([`CAP-30`](../08-validation/index.md#rule-cap-30))                                                                                                                                            |
| `inputs`      | Object  | DARF die Eingabedaten für das LLM definieren ([`CAP-30`](../08-validation/index.md#rule-cap-30))                                                                                                                                           |
| `config`      | Object  | DARF Konfigurationshinweise für die Ausführung enthalten ([`CAP-30`](../08-validation/index.md#rule-cap-30))                                                                                                                               |

### inputs-Objekt

| **Feld**     | **Typ**                 | **Beschreibung**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `context`    | Array[String \| Object] | DARF IDs aus der `ruml:context`-Capability angeben. Jede ID MUSS ein Key im `data` von `ruml:context` sein ([`CTX-10`](../08-validation/index.md#rule-ctx-10)). Als String: Kurzform (implizit `role: "reference"`). Als Object: `id` (MUSS) und `role` (DARF, `"reference"` oder `"subject"`, Standard: `"reference"`) ([`CAP-31`](../08-validation/index.md#rule-cap-31)). `"subject"` markiert das Dokument als Prüfgegenstand für diese Query. **Hinweis:** Context-Objekte, die als `role: "subject"` referenziert werden, SOLLTEN im Context-Objekt selbst `subject: true` gesetzt haben (siehe [Kapitel 4.11](4-11-ruml-context.md)). |
| `dataPoints` | Array[String]           | DARF DataPoint-IDs angeben, deren Werte dem LLM übergeben werden ([`CAP-31`](../08-validation/index.md#rule-cap-31)). Jede ID MUSS ein Key im `data` von `ruml:datapoints` sein ([`DP-18`](../08-validation/index.md#rule-dp-18))                                                                                                                                                                                                                                                                                                                                                                                                           |
| `texts`      | Array[String]           | DARF IDs aus der `ruml:text-reference`-Capability angeben (siehe [Kapitel 4.12](4-12-ruml-text-reference.md)) ([`CAP-31`](../08-validation/index.md#rule-cap-31)). Jede ID MUSS ein Key im `data` von `ruml:text-reference` sein ([`TXT-19`](../08-validation/index.md#rule-txt-19))                                                                                                                                                                                                                                                                                                                                                         |

### config-Objekt

| **Feld**        | **Typ** | **Beschreibung**                                                                                                                                                          |
| --------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `deterministic` | Boolean | DARF angeben, ob dasselbe Modell und dieselben Eingaben ein konsistentes Ergebnis liefern sollen ([`CAP-32`](../08-validation/index.md#rule-cap-32))                                                          |
| `effort`        | String  | DARF angeben, wie viel Aufwand das Modell für die Query betreiben soll (`"low"`, `"medium"`, `"high"`), z.B. als Reasoning-Aufwand. Standard: `"medium"` ([`CAP-32`](../08-validation/index.md#rule-cap-32)). |
| `temperature`   | Number  | DARF die Sampling-Temperatur für das LLM angeben (0.0–1.0) ([`CAP-32`](../08-validation/index.md#rule-cap-32)).                                                                                               |

### KI-Modell

Das Feld `model` referenziert das KI-Modell (LLM) bzw. die Klasse von Modellen, welche zur
Auswertung verwendet werden soll. Die erlaubten Werte und ihre Bedeutung sind vom jeweiligen Tool
abhängig und nicht Teil dieses Standards. Das konkrete mit einem Wert assoziierte Modell, der
API-Endpunkt und die Prompt-Vorlage werden in den Tool-Einstellungen gespeichert, **NICHT** in der
RUML-Datei — es sei denn, das `prompt`-Feld liefert den Prompt-Text direkt inline. In diesem Fall
hat der inline `prompt` Vorrang vor der Tool-konfigurierten Vorlage.

### Auswertungsregel

- Ein Knoten DARF sowohl `ruml:query` als auch `ruml:ai-query` definieren ([`CAP-33`](../08-validation/index.md#rule-cap-33))
- Wenn mehrere `decision`-Capabilities am Knoten vorhanden sind, bestimmt `decisionMode` die
  Kombinationslogik (siehe [Kapitel 4.3](4-3-capabilities-node-field.md))
- Das LLM MUSS ein Ergebnis `true`, `false` oder `undefined` zurückgeben
- Bei `undefined` (unentscheidbar) SOLLTE `ruml:actions` mit `onUndefined` kombiniert werden

### Beispiel — Vollständiger Knoten

```jsonc
"3": {
  "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
  "label": "Begründung plausibel",
  "capabilities": [
    {
      "id": "ruml:ai-query",
      "payload": {
        "model": "strong",
        "prompt": "Prüfe anhand der bereitgestellten Unterlagen, ob eine Härtefallbegründung plausibel ist. Antworte ausschließlich mit true, false oder undefined.",
        "description": "Prüft die Plausibilität der Härtefallbegründung anhand der Richtlinien und Beispielfälle",
        "inputs": {
          "context": [
            "ctx_guidelines",
            "ctx_bsg_ruling",
            "ctx_example_approved_medical",
            "ctx_example_rejected_luxury"
          ],
          "dataPoints": ["dp_hardship_reason", "dp_annual_income"]
        },
        "config": {
          "deterministic": true,
          "effort": "high",
          "temperature": 0.1
        }
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "onUndefined": {
          "operation": "requestDecision",
          "ref": "manual_review_workflow",
          "config": {
            "recipient": "role:social-worker",
            "deadline": "P5D",
            "responseOptions": ["approve", "reject", "requestMoreInfo"]
          }
        }
      }
    }
  ]
}
```

### Root-Level-Deklaration

Um `ruml:ai-query` in einer RUML-Datei zu verwenden, MUSS die Capability im
Root-`capabilities`-Array deklariert werden ([`CAP-15`](../08-validation/index.md#rule-cap-15)). Das optionale `config`-Feld DARF einen
globalen `systemPrompt` enthalten, der bei allen AI-Query-Ausführungen in dieser Datei verwendet
wird:

```jsonc
"capabilities": [
  {
    "id": "ruml:ai-query",
    "payload": {
      "config": {
        "systemPrompt": "Du bist ein rechtlicher Assistent. Analysiere die bereitgestellten Sachverhalte anhand der geltenden deutschen Rechtslage und antworte ausschließlich mit true, false oder undefined."
      }
    }
  }
]
```

| Feld           | Typ    | Beschreibung                                                                                                                                                                                                                                                                         |
| -------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `systemPrompt` | String | DARF einen globalen System-Prompt definieren, der für alle `ruml:ai-query`-Ausführungen in dieser Datei gilt. Wenn ein Knoten zusätzlich ein `prompt`-Feld hat, wird der `systemPrompt` als System-Rolle übergeben und der node-spezifische `prompt` als User-Rolle ([`CAP-32`](../08-validation/index.md#rule-cap-32)). |
