<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.15 ruml:tree-reference

## 4.15 Capability `ruml:tree-reference`

### Überblick

| Eigenschaft             | Wert                                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| **Capability-ID**       | `ruml:tree-reference`                                                                    |
| **Scope**               | Root-Level (nur Deklaration) + Node-Level                                                |
| **Standard `required`** | `false`                                                                                  |
| **Node-Level**          | `payload.represents` und `payload.refersTo` des `ruml:tree-reference`-Eintrags am Knoten |
| **Rolle**               | `data`                                                                                   |

Diese Capability lässt einen Knoten auf einen **Knoten einer anderen RUML-Datei** verweisen — und
damit auf den Teilbaum unter diesem Knoten. Der typische Fall ist eine Entscheidungs-Rulemap, deren
Regeln auf einem Gesetz beruhen, das selbst als Rulemap vorliegt: Der Knoten „Gesellschaftsvertrag
notariell beurkundet“ verweist auf den Knoten des Gesetzes für § 2 Abs. 1 GmbHG statt auf den Text
von § 2 Abs. 1.

Ein Knoten _repräsentiert_ höchstens einen Knoten einer anderen Datei und _verweist_ auf beliebig
viele. Keine der beiden Referenzen wird ausgewertet: Der referenzierte Teilbaum beeinflusst den
Status des Knotens nicht. Um einen referenzierten Teilbaum an Stelle eines Leaf-Nodes auszuwerten,
verwendet ein Knoten [`ruml:tree-include`](4-16-ruml-tree-include.md).

Der referenzierte Knoten bringt seinen Text mit: Die Knoten des Gesetzes haben eigene
[`ruml:text-reference`](4-12-ruml-text-reference.md)-Anker in den Text des Gesetzes, sodass eine
Baumreferenz zur Vorschrift **und** zu ihrem Wortlaut führt. Der Text ist an genau einer Stelle
verankert — in der Datei des Gesetzes.

**Abgrenzung:**

- [`ruml:text-reference`](4-12-ruml-text-reference.md) verankert **Textelemente** derselben
  RUML-Datei; `ruml:tree-reference` verweist auf **Knoten** anderer RUML-Dateien.
- [Modulare Knoten](../06-modular-nodes/index.md) verwenden einen Teilbaum **innerhalb derselben
  Datei** wieder; eine Baumreferenz zeigt in eine **andere** Datei.

### Root-Level-Deklaration

```jsonc
"capabilities": [
  {
    "id": "ruml:tree-reference"
  }
]
```

Der Root-Level-Eintrag DARF KEINE Payload haben ([`TREE-01`](../08-validation/index.md#rule-tree-01)). Wie bei jeder Capability MUSS eine
Datei, deren Knoten `ruml:tree-reference`-Einträge haben, sie im Root deklarieren (siehe
[Kapitel 4.3](4-3-capabilities-node-field.md)) ([`CAP-15`](../08-validation/index.md#rule-cap-15)).

### Node-Level: Referenzen

```jsonc
{
  "id": "ruml:tree-reference",
  "payload": {
    "represents": {
      "uri": "https://rulemapping.org/rulemapping/gmbhg:2025-01-01#node/6e51c5a6-f7ff-43e1-b211-c70bd69937d7"
    },
    "refersTo": [
      {
        "uri": "https://rulemapping.org/rulemapping/gmbhg:2025-01-01#node/7791005b-3d30-455b-a538-6d96f04680d9"
      }
    ]
  }
}
```

| **Feld**     | **Typ**       | **Pflicht** | **Beschreibung**                                                                                                                                                             |
| ------------ | ------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `represents` | Object        | **DARF**    | Der Knoten einer anderen RUML-Datei, für den dieser Knoten steht.                                                                                                            |
| `refersTo`   | Array[Object] | **DARF**    | [Knotenanker](#knotenanker) auf Knoten anderer RUML-Dateien, auf die dieser Knoten verweist. **MUSS**, falls vorhanden, mindestens einen Eintrag enthalten ([`TREE-01`](../08-validation/index.md#rule-tree-01)). |

**Validierungsregeln:**

- Die Payload **MUSS** `represents`, `refersTo` oder beide enthalten und **DARF KEINE** weiteren
  Felder enthalten; `represents` und jeder `refersTo`-Eintrag **MÜSSEN** genau `uri` haben
  ([`TREE-01`](../08-validation/index.md#rule-tree-01)).
- Jede `uri` **MUSS** ein Knotenanker sein ([`TREE-02`](../08-validation/index.md#rule-tree-02)). Ein Verweis innerhalb des Dokuments
  (`#node/…`) ist kein Knotenanker — Wiederverwendung innerhalb einer Datei ist Aufgabe
  [modularer Knoten](../06-modular-nodes/index.md).
- Dieselbe `uri` **DARF NICHT** zweimal in `refersTo` vorkommen ([`TREE-03`](../08-validation/index.md#rule-tree-03)).
- Der Zielknoten **MUSS** in der referenzierten Version der Datei existieren ([`TREE-04`](../08-validation/index.md#rule-tree-04)).

Baumreferenzen **DÜRFEN** Zyklen über Dateien hinweg bilden; sie werden nicht ausgewertet
([`TREE-05`](../08-validation/index.md#rule-tree-05)).

### Knotenanker

Ein Knotenanker besteht aus der URI **einer bestimmten Version** einer RUML-Datei, gefolgt von einem
Fragment, das einen Knoten darin benennt:

```
node-anchor      = ruml-version-uri "#node/" uuid
ruml-version-uri = <absolute URI einer unveränderlichen RUML-Version: ein veröffentlichter Tag oder ein Inhalts-Digest>
```

- **Version:** Die RUML-URI **MUSS** genau eine unveränderliche Version identifizieren — einen
  veröffentlichten Versions-Tag (`…/gmbhg:2025-01-01`) oder einen Inhalts-Digest
  (`…/gmbhg@sha3-256:…`). Ein Anker ohne Version **DARF NICHT** in einer exportierten oder
  ausgetauschten RUML-Datei vorkommen ([`TREE-06`](../08-validation/index.md#rule-tree-06); siehe [Arbeitsanker](#arbeitsanker)).
- **Knoten:** `node/<uuid>` adressiert einen Knoten über seine `id` und damit den Teilbaum darunter.
- **Eine Version je Datei:** Alle Knotenanker einer RUML-Datei, die in dieselbe andere RUML-Datei
  zeigen, **MÜSSEN** dieselbe Version davon verwenden ([`TREE-06`](../08-validation/index.md#rule-tree-06)). Der Wechsel auf eine neue
  Fassung des Gesetzes schreibt die Version in den Ankern um; da die Knoten-`id`s bleiben (siehe
  [Stabile Knotenidentität](#stabile-knotenidentität)), bleiben die Fragmente gleich.

Der Katalog unter `rulemapping.org` stellt solche URIs bereit
(`https://rulemapping.org/<org>/<name>:<tag>`); jede andere URI, die eine unveränderliche
RUML-Version identifiziert, ist ebenso gültig.

[`ruml:tree-include`](4-16-ruml-tree-include.md) verwendet dieselben Knotenanker.

#### Arbeitsanker

Während RUML-Dateien geschrieben werden, verweisen sie oft aufeinander, bevor eine davon
veröffentlicht ist. Ein Tool **DARF** daher **Arbeitsanker** halten, die die Zieldatei über ihre
`metadata.id` ohne Version benennen und auf ihren aktuellen Stand auflösen:

```
working-anchor = "urn:uuid:" metadata-id "#node/" uuid
```

`urn:uuid:5b0e7c8d-2f41-4a9e-8c3b-1d6f0e2a7b95#node/6e51c5a6-f7ff-43e1-b211-c70bd69937d7`

Arbeitsanker existieren nur im Arbeitsstand eines Tools. Wird eine RUML-Datei exportiert oder
ausgetauscht, **MUSS** das Tool jeden Arbeitsanker durch einen Knotenanker auf eine veröffentlichte
Version seines Ziels ersetzen; hat ein Ziel keine veröffentlichte Version, **MUSS** der Export
fehlschlagen. Ein Arbeitsanker bleibt gültig, während die Zieldatei bearbeitet wird, solange der
Zielknoten seine `id` behält.

### Auflösung und Anzeige

Ein Tool löst einen Knotenanker auf, indem es die referenzierte Version der Datei lädt (zuerst aus
einer [gebündelten Datei](#bündelung-für-den-export)) und den Knoten wählt, dessen `id` gleich der
`<id>` des Fragments ist. Dieser Knoten und sein Teilbaum sind der referenzierte Inhalt.

- **Texte:** Die referenzierten Knoten behalten ihre eigenen `ruml:text-reference`-Anker, die
  innerhalb der referenzierten Datei aufgelöst werden. Ein Tool **SOLLTE** die Texte des
  referenzierten Teilbaums zusammen mit ihm anzeigen; der verweisende Knoten braucht dafür keine
  eigenen Textanker. Er **DARF** zusätzlich eigene `ruml:text-reference`-Anker haben
  ([`TREE-07`](../08-validation/index.md#rule-tree-07)).
- **Anzeige:** Ein Tool **DARF** den referenzierten Teilbaum schreibgeschützt am verweisenden Knoten
  anzeigen. Der referenzierte Teilbaum wird nie in die verweisende Datei kopiert.

### Bündelung für den Export

Eine RUML-Datei, deren Knotenanker in andere RUML-Dateien zeigen, kann als Container
([Kapitel 7](../07-container/index.md)) exportiert werden, der diese Dateien mit enthält — jede mit
ihrer Versions-URI im Feld `uri` des Manifest-Eintrags
([Gebündelte RUML-Dateien](../07-container/7-2-structure.md#gebündelte-ruml-dateien)). Ein Parser
**MUSS** einen Knotenanker gegen die gebündelte RUML-Datei auflösen, deren Manifest-`uri` der
RUML-URI des Ankers entspricht, bevor er sie anderweitig abruft. In die verweisende Datei wird
nichts kopiert; die Integritäts- und Signaturebenen des Containers decken die gebündelten Dateien
wie jede andere Datei ab.

### Stabile Knotenidentität

Knotenanker benennen `id`-Werte von Knoten; sie überstehen eine neue Version der referenzierten
Datei daher nur, wenn deren Knoten ihre `id` behalten.

- Eine Rulemap, auf die andere Dateien verweisen können, **SOLLTE** die `id` eines Knotens über
  Versionen hinweg unverändert lassen, solange der Knoten für dasselbe steht.
- Eine Rulemap, die ein Gesetz abbildet, **SOLLTE** als `id` eines Knotens, der ein Element ihres
  eigenen Textes verankert, die [`GUID`](4-12-ruml-text-reference.md#element-identität-guid) dieses
  Elements verwenden — sofern sie eine UUID v4 in Kleinbuchstaben ist und unter den Knoten-`id`s der
  Datei eindeutig. Die Knotenidentität folgt dann der Textidentität, die Neunummerierungen
  übersteht.

**Verhalten bei modularen Knoten:** Eine Baumreferenz an einem modularen Knoten (`modular: true`)
gilt für **alle Instanziierungen**, unabhängig davon, wo der Knoten im Regelbaum erscheint.

## Konformitätstests

- [4.15 ruml:tree-reference](../../../tests/04-capabilities/4-15-ruml-tree-reference.test.yaml)
