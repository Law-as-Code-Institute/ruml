<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.2 Capability-Deklaration

### Überblick

Das `capabilities`-Feld ist eine optionale Liste auf der Root-Ebene einer RUML-Datei. Es deklariert
alle Capabilities, die in dieser Datei verwendet werden, mit je einem Eintrag.

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [],
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
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Anspruch auf Schadensersatz"
      }
    }
  }
}
```

### Positionierung im Root-Objekt

Das `capabilities`-Feld DARF im Root-Objekt einer RUML-Datei vorhanden sein.

:::note[Verhältnis zur Root-Struktur]
Die vollständige Root-Objekt-Struktur ist in
[Kapitel 2.2](../02-file-format-basics/2-2-file-structure.md) definiert. Das `capabilities`-Feld
erweitert die optionalen Root-Felder um einen Eintrag.:::

### Eintragsformat

Jeder Eintrag benennt seine Capability in `id` (nach der Namensraum-Konvention in
[Kapitel 4.4](4-4-namespaces.md)) und trägt die folgenden Felder:

```jsonc
"capabilities": [
  {
    "id": "ruml:ai-query",
    "required": true
  },
  {
    "id": "com.example/custom-actions",
    "role": "reaction"
  }
]
```

| Feld       | Typ     | Pflicht                       | Beschreibung                                                                                                                                                                                                                                                |
| ---------- | ------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`       | String  | MUSS                          | Die Capability-ID (siehe [Kapitel 4.4](4-4-namespaces.md)). DARF NICHT mehr als einmal im Array vorkommen (siehe [Eindeutigkeitsregel](#eindeutigkeitsregel)) ([`CAP-09`](../08-validation/index.md#rule-cap-09), [`CAP-10`](../08-validation/index.md#rule-cap-10)).                                                               |
| `required` | Boolean | DARF                          | Wenn `true`: Parser MUSS diese Capability kennen, sonst MUSS er die Datei ablehnen. Wenn `false` oder abwesend: Ignorierung erlaubt. Standard: `false`; `ruml:expression` MUSS `true` deklarieren ([Kapitel 4.14](4-14-ruml-expression.md)) ([`CAP-11`](../08-validation/index.md#rule-cap-11)) |
| `payload`  | Object  | DARF                          | Alles Capability-Spezifische. Die Struktur wird durch die jeweilige Capability-Spezifikation definiert; die beiden konventionellen Unterfelder sind unten beschrieben ([`CAP-09`](../08-validation/index.md#rule-cap-09)).                                                                      |
| `role`     | String  | MUSS für nicht-offizielle IDs | Die Rolle, die die Rulemap von dieser Capability erwartet: `data`, `decision`, `combiner` oder `reaction` (siehe [Kapitel 4.1](4-1-concept.md#capability-rollen), das auch die Regeln für ihre Deklaration festlegt) ([`CAP-03`](../08-validation/index.md#rule-cap-03)).                       |

Ein Capability-Eintrag ohne besondere Eigenschaften besteht nur aus `id`.

**Konventionelle `payload`-Unterfelder:**

| Unterfeld        | Typ          | Beschreibung                                                                                                                                                                                                            |
| ---------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `payload.data`   | Object (Map) | Root-Level-Artefaktdaten als Map-Struktur (Key = ID). Wird von Capabilities verwendet, die benannte Objekte bereitstellen (z.B. DataPoints, Context, Texts). Siehe [Abschnitt „Das `data`-Feld"](#das-data-feld) unten. |
| `payload.config` | Object       | Globale Konfiguration dieser Capability. Wird von Capabilities verwendet, die Laufzeit-Parameter benötigen (z.B. `systemPrompt` bei `ruml:ai-query`). Siehe [Abschnitt „Das `config`-Feld"](#das-config-feld) unten.    |

#### Das `data`-Feld

Das optionale `data`-Feld im `payload` eines Eintrags transportiert **Root-Level-Artefaktdaten** als
Map-Struktur (Key = ID, Value = Objekt). Es wird von Capabilities verwendet, die benannte Objekte
bereitstellen — z.B. DataPoint-Definitionen, Context-Materialien oder Rechtstexte.

**Capabilities mit `data`-Feld:**

- `ruml:datapoints` — DataPoint-Definitionen (Key = DataPoint-ID)
- `ruml:context` — Context-Objekte (Key = Context-ID)
- `ruml:text-reference` — Rechtstexte (Key = Text-ID)

**Regeln:**

1. Das `data`-Feld MUSS eine Map-Struktur sein (Object mit benannten Keys) ([`CAP-12`](../08-validation/index.md#rule-cap-12)).
2. Ein Parser, der die Capability nicht implementiert und `required: false` vorfindet, MUSS das
   `data`-Feld ignorieren ([`CAP-02`](../08-validation/index.md#rule-cap-02)).
3. Ein Parser, der die Capability kennt, MUSS das `data`-Feld gemäß der Capability-Spezifikation
   validieren ([`CAP-13`](../08-validation/index.md#rule-cap-13)).

```jsonc
"capabilities": [
  {
    "id": "ruml:context",
    "payload": {
      "data": {
        "ctx_guidance": {
          "title": "Leitfaden zur Prüfung",
          "category": "administrativeGuidance",
          "type": "url",
          "url": "https://example.com/leitfaden",
          "timestamp": "2024-01-01T00:00:00Z"
        }
      }
    }
  },
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
          }
        }
      }
    }
  }
]
```

#### Das `config`-Feld

Das optionale `config`-Feld im `payload` eines Eintrags transportiert **globale Konfiguration**, die
für alle Ausführungen dieser Capability in der Datei gilt. Im Gegensatz zu `data` enthält es keine
benannten Artefakte, sondern Laufzeit-Parameter.

**Regeln:**

1. Die Struktur von `config` wird durch die jeweilige Capability-Spezifikation definiert.
2. Ein Parser, der die Capability nicht implementiert und `required: false` vorfindet, MUSS das
   `config`-Feld ignorieren ([`CAP-02`](../08-validation/index.md#rule-cap-02)).
3. Ein Parser, der die Capability kennt, MUSS das `config`-Feld gemäß der Capability-Spezifikation
   validieren ([`CAP-13`](../08-validation/index.md#rule-cap-13)).
4. Ein `payload` DARF `data`, `config` oder beides enthalten — aber die Verwendung wird durch die
   Capability-Spezifikation festgelegt ([`CAP-12`](../08-validation/index.md#rule-cap-12)).

### Parser-Verhalten bei `required: true`

Wenn eine Capability `required: true` hat und der Parser sie nicht implementiert ([`CAP-01`](../08-validation/index.md#rule-cap-01)):

1. Der Parser MUSS einen Fehler ausgeben, der die unbekannte Capability-ID nennt.
2. Der Parser DARF die Datei NICHT partiell verarbeiten und dabei die unbekannten
   `capabilities`-Daten stillschweigend verwerfen.

```
Fehler: Unbekannte erforderliche Capability 'com.example/custom-actions'.
        Diese Datei kann ohne Unterstützung dieser Capability nicht korrekt verarbeitet werden.
```

### Parser-Verhalten bei `required: false`

Wenn eine Capability `required: false` oder kein `required` hat und der Parser sie nicht
implementiert ([`CAP-02`](../08-validation/index.md#rule-cap-02)):

1. Der Parser DARF die Verarbeitung wegen dieser Capability NICHT abbrechen.
2. Der Parser SOLLTE eine Warnung ausgeben, die die unbekannte Capability-ID nennt.
3. Der Parser MUSS die entsprechenden `capabilities`-Felder auf Knoten ignorieren.

Eine `ruml:`-ID, die diese Spezifikationsversion nicht definiert, fällt nicht unter [`CAP-01`](../08-validation/index.md#rule-cap-01)
und [`CAP-02`](../08-validation/index.md#rule-cap-02): Ein Parser lehnt eine Datei, die sie enthält, unabhängig vom Wert von `required`
ab ([Kapitel 4.4](4-4-namespaces.md)).

### Eindeutigkeitsregel

Jede `id` DARF NICHT mehr als einmal im `capabilities`-Array vorkommen. Ein Parser MUSS eine
doppelte `id` als Validierungsfehler behandeln ([`CAP-10`](../08-validation/index.md#rule-cap-10)). Das Schema erzwingt dies nur für die
eingebauten `ruml:`-Capabilities; für `ruml:draft/`- und Drittanbieter-IDs ist die Prüfung eine
Parser-Pflicht, da das Schema Eindeutigkeit über einen offenen ID-Raum nicht erzwingen kann.

Die Regel gilt für das Array auf Root-Level. Ob ein Knoten dieselbe ID mehrfach führen darf, hängt
von der Rolle der Capability ab (siehe
[Kapitel 4.3](4-3-capabilities-node-field.md#wiederholte-capability-ids)).

### Abwesenheit des Feldes

Wenn `capabilities` im Root-Objekt fehlt oder ein leeres Array ist:

- Die Datei verwendet keine Capabilities.
- Das Feld `capabilities` MUSS auf allen Knoten abwesend sein. Enthält ein Knoten dennoch ein
  `capabilities`-Feld, MUSS der Parser dies als Validierungsfehler behandeln ([`CAP-14`](../08-validation/index.md#rule-cap-14)).

:::warning[Keine impliziten Capabilities]
Ein Knoten DARF NICHT das `capabilities`-Feld befüllen, ohne die zugehörige Capability im
Root-Objekt deklariert zu haben — unabhängig davon, ob der Parser die Capability kennt oder nicht
([`CAP-15`](../08-validation/index.md#rule-cap-15)).:::

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
          "dp_damage": {
            "name": "Schadenshöhe",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            }
          },
          "dp_causality": {
            "name": "Kausalität gegeben",
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
      "id": "com.example/review-notes",
      "required": true,
      "role": "data"
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "created": "2024-06-01T00:00:00Z",
    "modified": "2024-06-01T00:00:00Z",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "operator": "AND",
        "label": "Anspruch auf Schadensersatz",
        "children": ["2", "3"],
        "capabilities": [
          {
            "id": "com.example/review-notes",
            "payload": {
              "status": "reviewed",
              "reviewer": "rechtsabteilung"
            }
          }
        ]
      },
      "2": {
        "id": "8fc54c7d-7f60-410e-9493-4f1eecfb1af8",
        "label": "Schaden entstanden",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_damage > 0"
            }
          },
          {
            "id": "com.example/review-notes",
            "payload": {
              "status": "pending"
            }
          }
        ]
      },
      "3": {
        "id": "56b5b9db-b791-4fe5-abb0-a05cb0847db6",
        "label": "Kausalität gegeben",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_causality = true"
            }
          }
        ]
      }
    }
  }
}
```

## Konformitätstests

- [4.2 Capability Declaration](../../../tests/04-capabilities/4-2-capabilities-field.test.yaml)
