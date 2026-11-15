<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.6 Operatoren

Der `operator` eines Knotens bestimmt, wie die Ergebnisse ALLER seiner direkten Kinder aggregiert
werden.

| **Operator**      | **Beschreibung**                                        | **Details**                          |
| ----------------- | ------------------------------------------------------- | ------------------------------------ |
| `AND` / `NOT_AND` | Konjunktion und negierte Konjunktion                    | [3.6.1](#361-and-und-not_and)        |
| `OR` / `NOT_OR`   | Disjunktion und negierte Disjunktion                    | [3.6.2](#362-or-und-not_or)          |
| `XOR` / `NOT_XOR` | Disjunktion und negierte Disjunktion mit Short-Circuit  | [3.6.3](#363-xor-und-not_xor)        |
| `DELEGATED`       | Verknüpfung durch eine im Knoten hinterlegte Capability | [3.6.4](#364-der-operator-delegated) |
| `undefined`       | Noch nicht definiert (Draft-Status)                     | [3.6.5](#365-der-undefined-operator) |

### Auswertungsmodus

Eine Rulemap wird in einem von zwei Modi ausgewertet:

- `optimized`: Short-Circuit-Regeln abhängig vom Operator anwenden
- `complete`: jeden Child-Node ohne Short-Circuit auswerten

### Leaf-Nodes

Ein Leaf-Node hat nichts zu verknüpfen. Außerhalb eines Entwurfs **DARF** er **KEINEN** `operator`
haben; in einem Entwurf (`metadata.status: "draft"`) **DARF** er jeden der Operatoren haben,
einschließlich `DELEGATED` und `undefined`, und ein Evaluator ignoriert ihn ([`NODE-07`](../08-validation/index.md#rule-node-07)). Das
Ergebnis eines Leaf-Nodes wird durch seine Capabilities bestimmt (siehe Kapitel
[4](../04-capabilities)).

### 3.6.1 `AND` und `NOT_AND`

Im Modus `optimized` **MUSS** der Evaluator die Ergebnisse der Child-Nodes nacheinander prüfen.

- Liefert ein Child-Node `false`, **MUSS** sofort `false` geliefert werden. Nicht geprüfte
  Child-Nodes **MÜSSEN** im RUML-Result auf `ignored` gesetzt werden.
- Liefert ein Child-Node `undefined`, **MUSS** sofort `undefined` geliefert werden. Nicht geprüfte
  Child-Nodes **MÜSSEN** im RUML-Result auf `ignored` gesetzt werden.
- Liefern alle Child-Nodes `true`, **MUSS** `true` geliefert werden.

Im Modus `complete` **MUSS** der Evaluator alle Ergebnisse der Kinder gemeinsam in folgender
Reihenfolge prüfen:

- Hat ein Kind `false` ergeben, **MUSS** `false` geliefert werden
- Hat ein Kind `undefined` ergeben, **MUSS** `undefined` geliefert werden
- Haben alle Child-Nodes `true` ergeben, **MUSS** `true` geliefert werden

**`NOT_AND`** **MUSS** dieselbe Logik anwenden, aber `true` liefern, wo `AND` `false` liefern würde,
und umgekehrt.

### 3.6.2 `OR` und `NOT_OR`

In den Modi `optimized` und `complete` **MUSS** der Evaluator alle Ergebnisse der Kinder gemeinsam
in folgender Reihenfolge prüfen:

- Hat ein Kind `true` ergeben, **MUSS** `true` geliefert werden.
- Hat ein Kind `undefined` ergeben, **MUSS** `undefined` geliefert werden.
- Haben alle Child-Nodes `false` ergeben, **MUSS** `false` geliefert werden.

**`NOT_OR`** **MUSS** dieselbe Logik anwenden, aber `true` liefern, wo `OR` `false` liefern würde,
und umgekehrt.

### 3.6.3 `XOR` und `NOT_XOR`

:::note
`XOR` bezeichnet nicht das logische Exklusiv-Oder (bei dem zwei `true`-Eingaben `false` ergeben),
sondern das juristische `XOR`: Die Child-Nodes sind bewusst so konstruiert, dass nur einer `true`
sein kann. Der Evaluator verhält sich wie eine Disjunktion (`OR`) mit vorzeitigem Abbruch beim
ersten `true`.
:::

Im Modus `optimized` **MUSS** der Evaluator die Ergebnisse der Child-Nodes nacheinander prüfen.

- Liefert ein Child-Node `true`, **MUSS** sofort `true` geliefert werden. Nicht geprüfte Child-Nodes
  **MÜSSEN** im RUML-Result auf `ignored` gesetzt werden.
- Liefert ein Child-Node `undefined`, **MUSS** sofort `undefined` geliefert werden. Nicht geprüfte
  Child-Nodes **MÜSSEN** im RUML-Result auf `ignored` gesetzt werden.
- Liefern alle Child-Nodes `false`, **MUSS** `false` geliefert werden.

Im Modus `complete` **MUSS** der Evaluator alle Ergebnisse der Kinder gemeinsam in folgender
Reihenfolge prüfen:

- Hat ein Kind `true` ergeben, **MUSS** `true` geliefert werden.
- Hat ein Kind `undefined` ergeben, **MUSS** `undefined` geliefert werden.
- Haben alle Child-Nodes `false` ergeben, **MUSS** `false` geliefert werden.

**`NOT_XOR`** **MUSS** dieselbe Logik anwenden, aber `true` liefern, wo `XOR` `false` liefern würde,
und umgekehrt.

### 3.6.4 Der Operator `DELEGATED`

Der Operator `DELEGATED` berechnet das Ergebnis aus den Ergebnissen der Child-Nodes mithilfe einer
Capability.

Er kann für Verknüpfungen verwendet werden, die die logischen Operatoren nicht ausdrücken können,
insbesondere Schwellenwertregeln („mindestens drei der folgenden Merkmale"), Toleranzregeln
(„höchstens eine Voraussetzung darf fehlen"), Mehrheits- und Quorumsregeln sowie Regeln, die ein
einzelnes Kind negieren statt des ganzen Knotens.

#### Bindung an einen Kombinierer

Die Regel selbst wird von einem **Kombinierer** getragen — einer Capability am Knoten, die dessen
Status aus den Ergebnissen seiner Kinder bestimmt. Der offizielle Kombinierer ist `ruml:expression`
(siehe [Kapitel 4.14](../04-capabilities/4-14-ruml-expression.md)); ein nicht-offizieller kann
ebenfalls verwendet werden (siehe _Eigene Kombinierer_ weiter unten).

Ein Parent-Node führt einen Kombinierer **genau dann, wenn** sein Operator `DELEGATED` ist:

- Außerhalb eines Entwurfs **MUSS** ein Knoten mit `operator: "DELEGATED"` ein nicht-leeres
  `children`-Array besitzen; ein Knoten mit `operator: "DELEGATED"` und `children` **MUSS** genau
  einen Capability-Eintrag führen, dessen Capability die Rolle `combiner` hat (Regel `OP-02`)
  ([`OP-02`](../08-validation/index.md#rule-op-02)). In einem Entwurf **DARF** ein Leaf-Node `operator: "DELEGATED"` ohne Kombinierer
  haben; der Operator wird wie jeder Operator an einem Leaf-Node ignoriert ([`NODE-07`](../08-validation/index.md#rule-node-07)).
- Ein Knoten mit einem Kombinierer-Eintrag **MUSS** `operator: "DELEGATED"` verwenden (Regel
  `CAP-08`) ([`CAP-08`](../08-validation/index.md#rule-cap-08)). Ein Kombinierer steht daher nie an einem Leaf-Node und nie an einem
  Knoten mit logischem Operator.

Keine der beiden Hälften ist für sich gültig. Ein Werkzeug, das den Kombinierer nicht kennt, kann
einen solchen Knoten daher nicht für einen logischen halten: Der Operator ist ihm unbekannt und die
Datei wird abgelehnt.

:::note[Ausnahme von der Leaf-Beschränkung]
Ein Kombinierer trägt die Rolle `combiner`, nicht `decision`, und ist die einzige Art von
Capability, die einen Knoten **mit** Kindern entscheidet. Die Beschränkung in
[Kapitel 4.1](../04-capabilities/4-1-concept.md) — Decision-Capabilities nur auf Leaf-Knoten — gilt
`ruml:query` und `ruml:ai-query`, die einen Knoten **anstelle** seiner Kinder entscheiden. Ein
Kombinierer entscheidet einen Knoten **aus** seinen Kindern und setzt sie deshalb voraus.
:::

#### Der Kombinierer-Vertrag

Der Operator delegiert die Verknüpfungsregel, nicht die Zusicherungen, die eine Rulemap prüfbar
machen. Jeder Kombinierer, offiziell oder nicht, **MUSS**:

1. `true`, `false` oder kein Ergebnis liefern — niemals eine Zahl, eine Zeichenkette oder eine
   Struktur. Jedes andere Ergebnis **MUSS** den Status `undefined` ergeben.
2. In seinem Payload auf Node-Level eine lesbare `description` führen, die die Regel in Prosa
   benennt. Der Operator `DELEGATED` sagt nicht, was der Knoten tut; ohne diese Angabe ist die
   Rulemap nicht prüfbar, ohne Code zu lesen (Regel `OP-04`) ([`OP-04`](../08-validation/index.md#rule-op-04)).
3. Ohne Auswertung `undefined` ergeben, sobald ein Kind `undefined` ist; JSONata ist zweiwertig und
   würde ein solches Kind sonst als nicht erfüllt zählen, sodass eine Schwellenwertregel bestimmt
   aussähe, obwohl sie es nicht ist.
4. Alle Kinder verbrauchen: Der Operator **DARF NICHT** short-circuiten (Regel `OP-03`)
   ([`OP-03`](../08-validation/index.md#rule-op-03)).

Ein Kombinierer **SOLLTE** deterministisch und aus denselben Eingaben reproduzierbar sein. Er
**DARF** nicht-deterministische Eingaben verwenden, etwa eine Zufallszahl oder die aktuelle Zeit
([`OP-05`](../08-validation/index.md#rule-op-05)); dann **SOLLTE** er die gezogenen Werte im Knotenergebnis festhalten.

Ein Kombinierer **SOLLTE** im Knotenergebnis festhalten, was er gesehen hat — mindestens die
verbrauchten Kind-Status, alle gelesenen DataPoint-Werte und den berechneten Wert —, damit die
Entscheidung allein aus der RUML-Result-Datei nachvollzogen werden kann.

Die Rolle einer Capability sagt, _wo_ sie stehen darf; dieser Vertrag sagt, _was sie leisten muss_,
um dort zu stehen. Zusammen sind sie, was einen Kombinierer ausmacht; RUML definiert keinen eigenen
Capability-Typ.

#### Eigene Kombinierer

Jede Capability mit der Rolle `combiner` **DARF** als Kombinierer auftreten, auch eine fremde nach
der Reverse-Domain-Konvention (siehe [Kapitel 4.4](../04-capabilities/4-4-namespaces.md))
([`OP-06`](../08-validation/index.md#rule-op-06)):

```jsonc
"capabilities": [
  {
    "id": "com.example/expression",
    "required": true,
    "role": "combiner"
  }
]
```

Ob eine eigene Capability ein Kombinierer ist, legen Parser und Evaluator fest, die sie
implementieren. Ihr Eintrag auf Root-Level **MUSS** die Rolle `combiner` deklarieren (Regeln
`CAP-03`, `OP-02`); ein Parser, der die Capability implementiert, gleicht die deklarierte Rolle mit
seiner Implementierung ab (Regel `CAP-04`) ([`CAP-03`](../08-validation/index.md#rule-cap-03), [`OP-02`](../08-validation/index.md#rule-op-02), [`CAP-04`](../08-validation/index.md#rule-cap-04)). Zu den
Rollen und zum Unterschied zwischen `combiner` und `decision` siehe
[Kapitel 4.1](../04-capabilities/4-1-concept.md).

`required: true` ist das, was Regel `CAP-01` dazu bringt, die Datei in einem Werkzeug abzulehnen,
das den Kombinierer nicht implementiert, statt einen Knoten mit einem Operator ohne dahinterliegende
Regel zu hinterlassen.

:::caution[Ein eigener Kombinierer macht die Rulemap nicht portabel]
Eine unbekannte Decision-Capability an einem _Blatt_ lässt ein Blatt `undefined`, während die übrige
Rulemap weiter ausgewertet wird. Ein unbekannter _Kombinierer_, der wie vorgeschrieben
`required: true` deklariert ist, führt zur Ablehnung des gesamten Dokuments. Eine Rulemap mit einem
nicht-`ruml:`-Kombinierer ist daher nur von Werkzeugen lesbar, die ihn implementieren. Die Menge der
offiziellen Kombinierer wächst durch Revision dieser Spezifikation; ein proprietärer Kombinierer ist
ein bewusster Tausch von Portabilität gegen Ausdrucksstärke.
:::

#### Was der Ausdruck sieht

Der Ausdruck wird gegen dasselbe Eingabedokument ausgewertet wie ein Ausdruck von `ruml:query`;
DataPoints werden also über ihre ID angesprochen (`dp_alter`). Zusätzlich sind die Ergebnisse der
direkten Kinder des Knotens an die Variable `$children` gebunden:

| Feld     | Typ    | Beschreibung                                                                                        |
| -------- | ------ | --------------------------------------------------------------------------------------------------- |
| `lexId`  | String | Die lexId des Kindes                                                                                |
| `label`  | String | Das Label des Kindes                                                                                |
| `status` | String | Der Status des Kindes: `"true"` oder `"false"` — ist ein Kind `undefined`, läuft der Ausdruck nicht |

Das Array folgt der Reihenfolge von `children`. Sichtbar sind ausschließlich **direkte** Kinder; ein
tiefer liegendes Ergebnis wird erreicht, indem der dazwischenliegende Knoten seinerseits seine
Kinder verknüpft.

#### Auswertungsregeln

- Der Operator **DARF NICHT** short-circuiten. Alle Kinder **MÜSSEN** vor der Auswertung des
  Ausdrucks ausgewertet werden, und ein Knoten mit `operator: "DELEGATED"` **DARF NICHT** dazu
  führen, dass ein Kind den Status `ignored` mit `reason.type: "shortCircuit"` erhält
  ([`OP-03`](../08-validation/index.md#rule-op-03)). Eine Zählung über nur teilweise ausgewertete Kinder wäre nicht bloß unvollständig,
  sondern falsch.
- Der Ausdruck **MUSS** zu einem Boolean auswerten. Jedes andere Ergebnis — auch das Ausbleiben
  eines Ergebnisses — **MUSS** den Status `undefined` ergeben, mit einer Begründung vom Typ
  `default`, deren `message` den beanstandeten Wert benennen **SOLLTE**.
- Ausdrücke **SOLLTEN** deterministisch sein. Die nicht-deterministischen JSONata-Funktionen
  `$random`, `$now` und `$millis` sowie `$eval` **DÜRFEN** verwendet werden; ein Ausdruck, der sie
  verwendet, ist aus denselben Eingaben nicht mehr zwingend reproduzierbar ([`OP-05`](../08-validation/index.md#rule-op-05)). `$eval`
  führt eine Zeichenkette als Ausdruck aus, die angewandte Regel steht dann also nicht notwendig in
  `expression` selbst — umso mehr Gewicht trägt `description`.
- Ein Ausdruck, dessen Ergebnis einem logischen Operator entspricht (etwa
  `$children[0].status = "true" and $children[1].status = "true"`), **SOLLTE** als Warnung gemeldet
  werden; der logische Operator ist die prüfbare Form.

#### Beispiele

Mindestens drei der aufgeführten Merkmale:

```jsonc
"1": {
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

Höchstens eine Voraussetzung darf fehlen:

```jsonc
"expression": "$count($children[status = 'false']) <= 1"
```

Mehrheit der ausgewerteten Kinder:

```jsonc
"expression": "$count($children[status = 'true']) * 2 > $count($children)"
```

Subsidiarität — das zweite Kind greift nur, wenn das erste nicht greift:

```jsonc
"expression": "$children[0].status = 'false' and $children[1].status = 'true'"
```

Eine Fiktion, die die Kinder insgesamt überspielt:

```jsonc
"expression": "dp_alter >= 65 or $count($children[status = 'true']) = 3"
```

#### Festhalten des Ergebnisses

Das Knotenergebnis führt den Ausdruck, die von ihm gesehenen Kind-Status und den berechneten Wert
mit, sodass die Entscheidung allein aus der RUML-Result-Datei nachvollzogen werden kann — siehe
[Kapitel 4.14](../04-capabilities/4-14-ruml-expression.md).

### 3.6.5 Der `undefined`-Operator

`undefined` bedeutet, der Operator ist noch nicht definiert. Er **DARF** während der Erstellung in
Dateien mit Status `draft` verwendet werden, **DARF NICHT** in Dateien mit einem anderen Status
verwendet werden und **MUSS** vor Finalisierung (Status `review`, `approved`, `inForce`) durch einen
gültigen Operator ersetzt werden ([`OP-07`](../08-validation/index.md#rule-op-07)). Er ist der Standardwert bei Neuerstellung eines
Knotens. An einem Leaf-Node (ohne `children`) wird der `operator` ignoriert; außerhalb eines
Entwurfs **DARF** ein Leaf-Node überhaupt **KEINEN** `operator` haben, `undefined` an einem
Leaf-Node wird daher entfernt statt ersetzt ([`NODE-07`](../08-validation/index.md#rule-node-07)).

| **Status**                                                          | **Regel**                                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `draft`                                                             | `undefined` **DARF** vorkommen ([`OP-07`](../08-validation/index.md#rule-op-07))                            |
| `review`, `approved`, `inForce`, `suspended`, `expired`, `replaced` | `undefined` **DARF NICHT** vorkommen → Validierungsfehler ([`OP-07`](../08-validation/index.md#rule-op-07)) |

Tools **SOLLTEN** bei `undefined`-Operatoren eine Warnung anzeigen. Tools **DÜRFEN** automatische
Ersetzung durch einen Standard-Operator (z.B. `AND`) anbieten.

## Konformitätstests

- [3.6 Operators (AND)](../../../tests/03-data-model/3-6-operators--and.test.yaml)
- [3.6 Operators (DELEGATED validation)](../../../tests/03-data-model/3-6-operators--delegate.test.yaml)
- [3.6 Operators (DELEGATED evaluation)](../../../tests/03-data-model/3-6-operators--delegated-evaluation.test.yaml)
- [3.6 Operators (NOT_AND)](../../../tests/03-data-model/3-6-operators--not-and.test.yaml)
- [3.6 Operators (NOT_OR)](../../../tests/03-data-model/3-6-operators--not-or.test.yaml)
- [3.6 Operators (NOT_XOR)](../../../tests/03-data-model/3-6-operators--not-xor.test.yaml)
- [3.6 Operators (OR)](../../../tests/03-data-model/3-6-operators--or.test.yaml)
- [3.6 Operators (XOR)](../../../tests/03-data-model/3-6-operators--xor.test.yaml)
