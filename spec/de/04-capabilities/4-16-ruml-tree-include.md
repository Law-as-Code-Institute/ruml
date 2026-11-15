<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.16 ruml:tree-include

## 4.16 Capability `ruml:tree-include`

### Überblick

| Eigenschaft             | Wert                                                     |
| ----------------------- | -------------------------------------------------------- |
| **Capability-ID**       | `ruml:tree-include`                                      |
| **Scope**               | Root-Level (nur Deklaration) + Node-Level                |
| **Standard `required`** | `false`                                                  |
| **Node-Level**          | `payload.uri` des `ruml:tree-include`-Eintrags am Knoten |
| **Rolle**               | `decision`                                               |

Diese Capability macht einen Leaf-Node zum **Platzhalter** für den Teilbaum eines Knotens einer
anderen RUML-Datei: Der referenzierte Teilbaum wird an Stelle des Leaf-Nodes ausgewertet, und sein
Status wird zum Status des Leaf-Nodes.

Sie ergänzt [`ruml:tree-reference`](4-15-ruml-tree-reference.md), das nur auf Knoten anderer Dateien
verweist. Beide verwenden dieselben [Knotenanker](4-15-ruml-tree-reference.md#knotenanker); es sind
zwei Capabilities, weil eine Capability genau eine Rolle hat (siehe
[Kapitel 4.1](4-1-concept.md#capability-rollen)).

**Warum „include“:** Der Name beschreibt die Beziehung aus Sicht des einbindenden Knotens — der
referenzierte Teilbaum ist genau an dieser Stelle Teil dieser Rulemap, ohne kopiert zu werden, wie
bei Akoma Ntoso `componentRef`, XInclude oder DITA `conref`.

**Abgrenzung zu modularen Knoten:** [Modulare Knoten](../06-modular-nodes/index.md) verwenden einen
Teilbaum **innerhalb derselben Datei** wieder. `ruml:tree-include` wertet den referenzierten
Teilbaum aus wie eine Instanz eines modularen Knotens, dessen Definition in einer **anderen** Datei
liegt.

### Root-Level-Deklaration

```jsonc
"capabilities": [
  {
    "id": "ruml:tree-include"
  }
]
```

Der Root-Level-Eintrag DARF KEINE Payload haben ([`TREE-01`](../08-validation/index.md#rule-tree-01)).

### Node-Level: Der eingebundene Knoten

```jsonc
{
  "id": "ruml:tree-include",
  "payload": {
    "uri": "https://rulemapping.org/rulemapping/gmbhg:2025-01-01#node/6e51c5a6-f7ff-43e1-b211-c70bd69937d7"
  }
}
```

| **Feld** | **Typ** | **Pflicht** | **Beschreibung**                                                                                                         |
| -------- | ------- | ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| `uri`    | String  | **MUSS**    | Ein [Knotenanker](4-15-ruml-tree-reference.md#knotenanker) auf den eingebundenen Knoten: `<ruml-version-uri>#node/<id>`. |

**Validierungsregeln:**

- Die Payload **MUSS** `uri` enthalten und **DARF KEINE** weiteren Felder enthalten
  ([`TREE-01`](../08-validation/index.md#rule-tree-01)), und `uri` **MUSS** ein Knotenanker sein ([`TREE-02`](../08-validation/index.md#rule-tree-02)).
- Ein Knoten mit `ruml:tree-include` **DARF KEINE** Kinder haben ([`CAP-07`](../08-validation/index.md#rule-cap-07)).
- Ein Knoten mit `ruml:tree-include` **DARF** in seiner `ruml:tree-reference` **KEIN** `represents`
  haben ([`TREE-08`](../08-validation/index.md#rule-tree-08)): Ein Knoten, der einen anderen Knoten einbindet, steht bereits für ihn.
- Die Regeln für Knotenanker aus [Kapitel 4.15](4-15-ruml-tree-reference.md#knotenanker) gelten:
  eine unveränderliche Version, dieselbe Version für alle Knotenanker in eine Datei
  ([`TREE-06`](../08-validation/index.md#rule-tree-06)), und der Zielknoten existiert in dieser Version ([`TREE-04`](../08-validation/index.md#rule-tree-04)).
- Einbindungen **DÜRFEN KEINEN** Zyklus über Dateien hinweg bilden ([`TREE-09`](../08-validation/index.md#rule-tree-09)): Datei A bindet
  einen Knoten von B ein, und B einen Knoten von A — direkt oder über weitere Dateien.

### Mehrere Teilbäume einbinden

Um mehrere Teilbäume einzubinden, verwendet eine Rulemap mehrere Platzhalterknoten. Der Baum legt
dann alles fest, was die Kombination braucht: Die Reihenfolge ist die Reihenfolge der Kinder, die
Verknüpfung ist der Operator des Parent-Nodes, eine Negation ist ein Parent-Node mit einem
`NOT_…`-Operator (siehe [Kapitel 3.6](../03-data-model/3-6-operators.md)), und jede Einbindung hat
ihr eigenes Label, ihre eigene Erläuterung, eigene Textreferenzen und ein eigenes Ergebnis.

```
„Gesellschaft wirksam gegründet“                   AND
├── „Gesellschaftsvertrag notariell beurkundet“    include → gmbhg:2025-01-01#node/6e51…
├── „Stammkapital mind. 25.000 €“                  include → gmbhg:2025-01-01#node/7791…
└── „Eintragung ins Handelsregister“               (eigene Logik)
```

Wie bei modularen Knoten ist Wiederverwendung als Knoten im Baum sichtbar, nicht als verborgene
zusätzliche Kinder.

### Auswertung

Ein Tool löst den eingebundenen Knoten auf (siehe
[Auflösung und Anzeige](4-15-ruml-tree-reference.md#auflösung-und-anzeige)), wertet ihn mit seinem
Teilbaum nach den Regeln der referenzierten Datei aus und verwendet den ermittelten Status als
Ergebnis der Capability. Hat der Leaf-Node weitere `decision`-Capabilities, verknüpft `decisionMode`
ihre Ergebnisse (siehe [Kapitel 4.3](4-3-capabilities-node-field.md)).

**In dieser Version nicht definiert:** Wie der eingebundene Teilbaum seine Eingaben erhält — die
Datenpunkte und Fragen, die seine Leaf-Nodes auswerten —, ist in dieser Version der Spezifikation
nicht definiert. Erwogen werden Eingaben, die mit der einbindenden Datei über die Datenpunkt-`id`
geteilt werden, Eingaben mit einem eigenen Namensraum je referenzierter Datei und eine ausdrückliche
Bindung je Einbindung.

Ein Tool, das eine Einbindung nicht auswerten kann — weil es `ruml:tree-include` nicht unterstützt
oder weil die referenzierte Version oder der referenzierte Knoten nicht geladen werden kann —,
**MUSS** `undefined` als ihr Ergebnis verwenden (siehe
[Kapitel 5.0](../05-result-format/5-0-status-types.md)); der Knoten **DARF NICHT** als erfüllt
behandelt werden.

**Verhalten bei modularen Knoten:** Eine Einbindung an einem modularen Knoten (`modular: true`) gilt
für **alle Instanziierungen**.

## Konformitätstests

- [4.16 ruml:tree-include](../../../tests/04-capabilities/4-16-ruml-tree-include.test.yaml)
