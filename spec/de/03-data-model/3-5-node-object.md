<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 3.5 Node-Objekt

## 3.5 Node-Objekt (Kernarchitektur)

### 3.5.1 Knotentypen nach Rolle

In der flachen Map-Architektur sind alle Knoten direkt im `nodes`-Objekt gespeichert. Die
Knotentypen ergeben sich aus ihrer **logischen Rolle** in der Hierarchie, die durch die `lexId` und
`children`-Referenzen definiert wird:

| **Typ** | **Logische Rolle** | **Beschreibung**               | **Erkennungsmerkmal**                         |
| ------- | ------------------ | ------------------------------ | --------------------------------------------- |
| root    | Wurzel             | Der oberste Knoten der Rulemap | Hat den Key `"1"` im `nodes`-Objekt (LexID 1) |
| parent  | Verzweigung        | Knoten mit eigenen Kindern     | Hat ein nicht-leeres `children`-Array         |
| leaf    | Blatt              | Endknoten ohne Kinder          | Hat kein `children`-Array                     |

Für die Knotentypen gelten folgende Regeln:

- Der Root-Knoten **MUSS** vorhanden sein ([`FMT-08`](../08-validation/index.md#rule-fmt-08)).
- Der Root-Knoten **DARF NICHT** im `children`-Array eines Knotens vorkommen ([`NODE-05`](../08-validation/index.md#rule-node-05)).
- Ein `children`-Array **DARF NICHT** leer sein ([`NODE-06`](../08-validation/index.md#rule-node-06)).

**Wichtig:** Der Typ **DARF NICHT** explizit gespeichert werden, da er sich aus der Struktur ergibt
([`NODE-03`](../08-validation/index.md#rule-node-03)).

**Laufzeit-Status:** Der Auswertungsstatus eines Knotens (`pending`, `true`, `false`, `undefined`,
`ignored`) wird zur Laufzeit berechnet und ist NICHT Teil der Node-Definition. Die Speicherung von
Auswertungsergebnissen erfolgt ausschließlich in einer separaten RUML-Result-Datei (`.ruml-result`)
(siehe [Kapitel 5](../05-result-format/index.md)).

### 3.5.2 Pflichtfelder eines Knotens

| Feld    | Typ      | Beschreibung                                                                                                                                                                                     |
| ------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`    | `UUID`   | **MUSS** vorhanden sein ([`NODE-01`](../08-validation/index.md#rule-node-01)). **MUSS** innerhalb der Datei eindeutig sein, auch gegenüber `metadata.id` ([`NODE-08`](../08-validation/index.md#rule-node-08)). **MUSS** dem Format aus 3.2.2 entsprechen ([`FMT-10`](../08-validation/index.md#rule-fmt-10)). |
| `label` | `String` | **MUSS** eine menschenlesbare Bezeichnung enthalten ([`NODE-01`](../08-validation/index.md#rule-node-01)). **MUSS** mindestens 1 Zeichen haben ([`NODE-09`](../08-validation/index.md#rule-node-09)).                                                                      |

**Hinweis zur LexID:** Die LexID eines Knotens ergibt sich aus dem Key im `nodes`-Objekt (siehe
[3.2.1](3-2-data-types-and-formats.md)). Ein separates `lexId`-Feld ist NICHT erforderlich und DARF
NICHT verwendet werden ([`NODE-03`](../08-validation/index.md#rule-node-03)).

### 3.5.2a Das Feld `operator`

Das Feld `operator` (Typ `Enum`) legt fest, wie ein Knoten die Ergebnisse seiner Kinder verknüpft.

- Ein Parent-Node **MUSS** einen `operator` haben; er gilt für ALLE direkten Kinder
  ([`NODE-12`](../08-validation/index.md#rule-node-12)).
- Ein Leaf-Node hat nichts zu verknüpfen. Er **DARF KEINEN** `operator` haben, außer
  `metadata.status` ist `draft`; in einem Entwurf **DARF** ein Leaf-Node jeden Operator haben, und
  ein Evaluator ignoriert ihn ([`NODE-07`](../08-validation/index.md#rule-node-07)).
- Der Wert **MUSS** einer der in [3.6](3-6-operators.md) definierten Operatoren sein ([`OP-01`](../08-validation/index.md#rule-op-01)).

### 3.5.3 Optionale Felder eines Knotens

Ein Knoten DARF jedes der folgenden Felder haben; ein Parser MUSS jedes davon akzeptieren, ob
vorhanden oder nicht ([`NODE-07`](../08-validation/index.md#rule-node-07)).

| Feld           | Typ             | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `altText`      | `String`        | **DARF** einen alternativen/vollständigen Text enthalten. **SOLLTE** für UI-Darstellung (Tooltips, Screen-Reader) verwendet werden. Wenn nicht gesetzt, **SOLLTE** `label` verwendet werden.                                                                                                                                                                                                                                                   |
| `description`  | `String`        | **DARF** eine ausführliche Beschreibung enthalten. DARF 10.000 Zeichen NICHT überschreiten ([`NODE-11`](../08-validation/index.md#rule-node-11)).                                                                                                                                                                                                                                                                                                                                   |
| `children`     | `Array[String]` | **DARF** eine geordnete Liste von Kind-Referenzen enthalten. Jeder Eintrag **MUSS** eine `LexID`-Referenz sein (String, siehe [2.5](../02-file-format-basics/2-5-identifier-system.md)) ([`FMT-11`](../08-validation/index.md#rule-fmt-11)). Jede referenzierte `LexID` **MUSS** im `nodes`-Objekt existieren ([`NODE-10`](../08-validation/index.md#rule-node-10)). Dieselbe `LexID` **SOLLTE NICHT** mehr als einmal in einem `children`-Array vorkommen. Die Reihenfolge ist signifikant.                            |
| `capabilities` | `Array`         | **DARF** capability-spezifische Daten für diesen Knoten enthalten, als geordnete Liste von `{ id, payload }`-Einträgen; jeder Eintrag MUSS beide Felder haben ([`CAP-17`](../08-validation/index.md#rule-cap-17)). Jede `id` MUSS einer in der Datei deklarierten Capability entsprechen ([`CAP-15`](../08-validation/index.md#rule-cap-15)). Über `capabilities` werden u.a. `ruml:query`, `ruml:actions` und `ruml:ai-query` bereitgestellt. Siehe [Kapitel 4.3](../04-capabilities/4-3-capabilities-node-field.md). |
| `metadata`     | `Object`        | **DARF** zusätzliche Metadaten enthalten. **SOLLTE** für nicht-strukturelle Informationen verwendet werden.                                                                                                                                                                                                                                                                                                                                    |
| `decisionMode` | `Enum`          | **DARF** den Kombinationsmodus für mehrere entscheidungsrelevante Capabilities definieren. Nur relevant bei Leaf-Nodes mit mehr als einer `decision`-Capability. Erlaubte Werte: `fallback`, `agreement`, `majority`. Standard: `fallback`. Siehe [Kapitel 4.3](../04-capabilities/4-3-capabilities-node-field.md).                                                                                                                            |
| `modular`      | `Boolean`       | Kennzeichnet den Knoten als modularen Knoten (Definition siehe [6.2](../06-modular-nodes/6-2-implementation.md#definition-modularer-knoten)). Ein modularer Knoten **MUSS** `modular: true` haben ([`MOD-01`](../08-validation/index.md#rule-mod-01)); ein Knoten, der nicht modular ist, **SOLLTE** es **NICHT** haben.                                                                                                                                                           |

**Wichtige Regeln:**

- Einschränkungen für entscheidungsrelevante Capabilities (`ruml:query`, `ruml:ai-query`) werden in
  der jeweiligen Capability-Spezifikation definiert (siehe
  [Kapitel 4.8](../04-capabilities/4-8-ruml-query.md))
- Die Norm, die ein Knoten repräsentiert, und die Texte, auf die er sich bezieht, werden über den
  `capabilities`-Eintrag mit `id: "ruml:text-reference"` bereitgestellt (Anker in `refs`, siehe
  [Kapitel 4.12](../04-capabilities/4-12-ruml-text-reference.md))
- Die `id` jedes Eintrags im `capabilities`-Array eines Knotens MUSS im
  Root-Level-`capabilities`-Array derselben Datei deklariert sein (referenzielle Integrität, Regel
  CAP-15 in Kapitel 08) ([`CAP-15`](../08-validation/index.md#rule-cap-15)). Die vollständige Spezifikation findet sich in
  [Kapitel 4.3](../04-capabilities/4-3-capabilities-node-field.md).

:::note[Capability-gelieferte Node-Erweiterungen]
Folgende Konzepte sind **keine direkten Node-Felder**, sondern werden über `capabilities`
bereitgestellt:

| Capability            | Node-Feld                                          | Beschreibung                                                                                                                |
| --------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `ruml:query`          | `capabilities`-Eintrag `id: "ruml:query"`          | Datenbasierte Abfrage-Expression für Leaf-Nodes — siehe [Kapitel 4.8](../04-capabilities/4-8-ruml-query.md)                 |
| `ruml:actions`        | `capabilities`-Eintrag `id: "ruml:actions"`        | Actions für `onTrue`, `onFalse`, `onUndefined` — siehe [Kapitel 4.10](../04-capabilities/4-10-ruml-actions.md)              |
| `ruml:ai-query`       | `capabilities`-Eintrag `id: "ruml:ai-query"`       | LLM-basierte Entscheidung — siehe [Kapitel 4.9](../04-capabilities/4-9-ruml-ai-query.md)                                    |
| `ruml:text-reference` | `capabilities`-Eintrag `id: "ruml:text-reference"` | Verweise auf normative Texte (Gesetze, Verordnungen) — siehe [Kapitel 4.12](../04-capabilities/4-12-ruml-text-reference.md) |
:::

### 3.5.4 Knotenpositionen (Pfade)

Knotenpositionen (Pfade) werden zur Laufzeit aus der Baumstruktur berechnet und sind NICHT Teil der
RUML-Datei. Die hierarchische Position eines Knotens ergibt sich vollständig aus den
`children`-Arrays und der `lexId`-Struktur im `nodes`-Objekt.

Bei modularen Knoten (siehe [Kapitel 6](../06-modular-nodes/index.md)) kann derselbe Knoten über
verschiedene Pfade im Baum erreicht werden. Die Pfade werden zur Laufzeit berechnet und im
`results`-Objekt der RUML-Result-Datei (siehe [Kapitel 5](../05-result-format/index.md)) als
Schlüssel für die Auswertungsergebnisse verwendet.

## Konformitätstests

- [3.5 Node Object](../../../tests/03-data-model/3-5-node-object.test.yaml)
