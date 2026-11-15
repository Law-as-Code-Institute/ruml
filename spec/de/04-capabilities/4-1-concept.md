<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.1 Konzept

### Was Capabilities leisten

Die RUML-Kernstruktur (Kapitel 1–3) dient der maschinenlesbaren Abbildung von Regelwerken und
Gesetzen als Entscheidungsbäume — mit Knoten, Operatoren, Rechtsbezügen und Metadaten. Diese
Struktur ist vollständig und stabil, aber bewusst passiv: Sie beschreibt _was_ geprüft werden soll,
nicht _wie_ die Prüfung ausgeführt wird.

Capabilities erfüllen zwei Rollen:

**1. Entscheidungsfähigkeit** — Sie machen eine Rulemap ausführbar. Sie definieren:

- **Womit** entschieden wird — z.B. typisierte Datenpunkte (`ruml:datapoints`), datenbasierte
  Queries (`ruml:query`), KI-Modelle (`ruml:ai-query`)
- **Wie** entschieden wird — Expressions, Prompts, externe Bindungen
- **Was danach passiert** — ausgelöste Aktionen (`ruml:actions`)
- **Worauf sich die Entscheidung stützt** — normative Texte (`ruml:text-reference`), Knoten anderer
  Rulemaps (`ruml:tree-reference`, `ruml:tree-include`), Kontextmaterialien (`ruml:context`)

**2. Erweiterbarkeit** — Das Capabilities-System stellt darüber hinaus einen kontrollierten,
interoperablen Mechanismus bereit, mit dem weitere Informationen deklariert und transportiert werden
können, ohne die Kernstruktur zu verändern:

- Fachdomänen-spezifische Metadaten, die nur für ein bestimmtes Rechtssystem relevant sind
- Experimentelle Erweiterungen, die noch nicht Teil der offenen Spezifikation sind
- Drittanbieter-Annotationen, die parallel zum RUML-Kern geführt werden

### Zwei-Schichten-Modell

RUML folgt einem bewussten Zwei-Schichten-Modell:

| Schicht                             | Inhalt                                                                                                                                                                            | Zweck                                                                                 |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **RUML-Kern** (Kapitel 1–3)         | Entscheidungsbaum, Operatoren, Labels, Metadaten                                                                                                                                  | Strukturelle Abbildung von Regelwerken und Gesetzen; stabil, passiv, zertifizierbar   |
| **RUML + Capabilities** (Kapitel 4) | `ruml:datapoints`, `ruml:query`, `ruml:ai-query`, `ruml:actions`, `ruml:text-reference`, `ruml:tree-reference`, `ruml:tree-include`, `ruml:context` und proprietäre Erweiterungen | Entscheidungsfähigkeit, Ausführungslogik, Materialien und Drittanbieter-Erweiterungen |

Der RUML-Kern ist **strukturell autark**: Eine RUML-Datei ohne Capabilities enthält alle
Informationen zur Darstellung der Regelstruktur und ihrer normativen Textverankerung. Die Anwendung
einer Rulemap auf einen konkreten Sachverhalt — also das Bereitstellen von Eingangsdaten, die
Auswertung von Leaf-Node-Bedingungen und das Auslösen von Actions — wird durch Capabilities
(Kapitel 4) und die Laufzeitumgebung ermöglicht.

### Die zwei Liefermodi

Capability-Daten können auf zwei Wegen in ein RUML-Dokument-Ökosystem eingebracht werden:

#### Inline-Modus (embedded)

Die Capability wird im `capabilities`-Array der RUML-Datei deklariert, und die Erweiterungsdaten
werden direkt als `capabilities`-Feld auf den betroffenen Knoten oder als Teil der Deklaration im
Root gespeichert.

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
            "name": "Alter des Antragstellers",
            "type": "integer",
            "binding": {
              "type": "input"
            }
          },
          "dp_income": {
            "name": "Jahreseinkommen",
            "type": "number",
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
        "label": "Kreditwürdigkeit prüfen",
        "children": ["2", "3"]
      },
      "2": {
        "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
        "label": "Mindestalter erfüllt",
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
        "label": "Einkommen ausreichend",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_income >= 30000"
            }
          }
        ]
      }
    }
  }
}
```

#### Sidecar-Modus (RUML-EXT)

Die Erweiterungsdaten werden in einer separaten `.ruml-ext`-Datei gespeichert, die über eine
`$base`-Referenz (UUID + Hash) mit der Ursprungs-RUML-Datei verknüpft ist.

### Fail-Fast bei unbekannten Capabilities

Jede Capability deklariert über `required`, ob sie für die korrekte Verarbeitung zwingend notwendig
ist:

- `required: true` — Der Parser **MUSS** diese Capability unterstützen. Erkennt er sie nicht,
  **MUSS** er die Datei ablehnen ([`CAP-01`](../08-validation/index.md#rule-cap-01)).
- `required: false` — Der Parser **MUSS** die Datei akzeptieren und diese Capability ignorieren
  ([`CAP-02`](../08-validation/index.md#rule-cap-02)). Er **SOLLTE** eine Warnung ausgeben.

Ein Parser **DARF** eine Datei mit einer unbekannten `required: true`-Capability **niemals** still
akzeptieren ([`CAP-01`](../08-validation/index.md#rule-cap-01)). Stilles Verwerfen von Erweiterungsdaten würde zu einer scheinbar
korrekten, aber unvollständigen Verarbeitung führen.

### Capability-Rollen

Jede Capability hat genau eine **Rolle**, die in der jeweiligen Capability-Spezifikation festgelegt
ist. Die Rolle bestimmt,

- ob eine Capability an einem Knoten einmal oder mehrfach vorkommen kann,
- wie die Capability ausgewertet wird und
- wie sich das Ergebnis auf die Rulemap auswirkt.

Die Rolle jeder offiziellen `ruml:`-Capability ist in dieser Spezifikation festgelegt.

`ruml:draft/`- und Reverse-Domain-Capabilities sind Erweiterungspunkte dieser Spezifikation. Ihre
Rolle legen Parser und Evaluator fest, die sie implementieren, nicht diese Spezifikation.

Der Eintrag auf Root-Level einer solchen Capability MUSS die Rolle, die die Rulemap erwartet, im
Feld `role` deklarieren (siehe [Kapitel 4.2](4-2-capabilities-field.md); [`CAP-03`](../08-validation/index.md#rule-cap-03)). Die
Deklaration macht die Rolle in der Datei sichtbar und lässt sie von Werkzeugen prüfen:

- Ein Parser, der die Capability implementiert, MUSS die Datei zurückweisen, wenn die deklarierte
  Rolle von der implementierten abweicht ([`CAP-04`](../08-validation/index.md#rule-cap-04)).
- Ein Parser, der die Capability nicht implementiert, wendet die folgenden rollenbezogenen Regeln
  auf die deklarierte Rolle an.

Eine offizielle `ruml:`-Capability DARF `role` NICHT deklarieren ([`CAP-05`](../08-validation/index.md#rule-cap-05)).

#### `data`

- **Einschränkungen:** keine
- **Mehrfachvorkommen:** Jede ID einer `data`-Capability DARF NICHT mehr als einmal an einem Knoten
  vorkommen ([`CAP-06`](../08-validation/index.md#rule-cap-06)).
- **Beispiele:** `ruml:datapoints`, `ruml:text-reference`, `ruml:tree-reference`, `ruml:context`

Stellt Eingabedaten oder Materialien bereit, liefert aber selbst kein Ergebnis.

#### `decision`

- **Einschränkungen:** Capabilities mit der Rolle `decision` DÜRFEN NICHT auf Knoten mit Kindern
  angewendet werden ([`CAP-07`](../08-validation/index.md#rule-cap-07)).
- **Mehrfachvorkommen:** IDs einer `decision`-Capability DÜRFEN an jedem Knoten mehrfach vorkommen
  ([`CAP-06`](../08-validation/index.md#rule-cap-06)).
- **Beispiele:** `ruml:query`, `ruml:ai-query`, `ruml:tree-include`

Bestimmt den Status eines Leaf-Nodes. Sie MUSS `true`, `false` oder `undefined` zurückgeben. Enthält
ein Leaf-Node mehrere `decision`-Capabilities, bestimmt das Feld `decisionMode` am Knoten, wie die
Ergebnisse kombiniert werden (siehe [Kapitel 4.3](4-3-capabilities-node-field.md)).

#### `combiner`

- **Einschränkungen:** Capabilities mit der Rolle `combiner` DÜRFEN NICHT auf Knoten angewendet
  werden, deren Operator nicht `DELEGATED` ist ([`CAP-08`](../08-validation/index.md#rule-cap-08)).
- **Mehrfachvorkommen:** Ein Knoten mit dem Operator `DELEGATED` und Kindern MUSS genau eine
  Capability mit der Rolle `combiner` haben ([`OP-02`](../08-validation/index.md#rule-op-02)).
- **Beispiele:** `ruml:expression`

Bestimmt den Status eines Parent-Nodes aus dem Status seiner Kinder. Sie kommt zum Einsatz, wenn die
übrigen eingebauten Operatoren nicht ausreichen. Sie MUSS `true`, `false` oder `undefined`
zurückgeben.

#### `reaction`

- **Einschränkungen:** keine
- **Mehrfachvorkommen:** IDs einer `reaction`-Capability DÜRFEN an jedem Knoten mehrfach vorkommen
  ([`CAP-06`](../08-validation/index.md#rule-cap-06)).
- **Beispiele:** `ruml:actions`

Eine Capability hat genau eine Rolle. Ein Anbieter, der dieselbe Logik als `decision` am Blatt und
als `combiner` anbieten will — etwa eine Ausdruckssprache, die an beiden Stellen einsetzbar ist —,
registriert zwei Capability-IDs, eine je Rolle. Die Rolle wird in der Überblickstabelle der
Capability-Spezifikation dokumentiert.

### Signierung von Capabilities

Wenn Capabilities inline im `capabilities`-Array bereitgestellt werden, sind sie **Teil der Datei**
und werden beim Signieren miterfasst. Eine RUML-Datei mit inline Capabilities somit vollständig
zertifiziert werden. Die Signatur schützt sowohl die Kernstruktur als auch die erweiterten
Artefakte.
