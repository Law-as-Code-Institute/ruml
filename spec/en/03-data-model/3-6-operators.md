<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.6 Operators

The `operator` of a node determines how the results of ALL its direct children are aggregated.

| **Operator**      | **Description**                                         | **Details**                          |
| ----------------- | ------------------------------------------------------- | ------------------------------------ |
| `AND` / `NOT_AND` | Conjunction and negated conjunction                     | [3.6.1](#361-and-and-not_and)        |
| `OR` / `NOT_OR`   | Disjunction and negated disjunction                     | [3.6.2](#362-or-and-not_or)          |
| `XOR` / `NOT_XOR` | Disjunction and negated disjunction with short-circuit  | [3.6.3](#363-xor-and-not_xor)        |
| `DELEGATED`       | Combination defined by a capability carried in the node | [3.6.4](#364-the-delegated-operator) |
| `undefined`       | Not yet defined (draft status)                          | [3.6.5](#365-the-undefined-operator) |

### Evaluation mode

A rulemap is evaluated in one of two modes:

- `optimized`: apply short-circuit rules depending on the operator
- `complete`: evaluate every child node without short-circuit

### Leaf nodes

A leaf node has nothing to combine. Outside a draft, it **MUST NOT** have an `operator`; in a draft
(`metadata.status: "draft"`), it **MAY** have any of the operators, including `DELEGATED` and
`undefined`, and an evaluator ignores it ([`NODE-07`](../08-validation/index.md#rule-node-07)). The result of a leaf node is determined
by its capabilities (see chapter [4](../04-capabilities))

### 3.6.1 `AND` and `NOT_AND`

In `optimized` mode, the evaluator MUST check the child node results one after another.

- If a child node yields `false`, it **MUST** yield `false` immediately. Child nodes that have not
  been inspected MUST be set to `ignored` in the RUML-result.
- If a child node yields `undefined`, it **MUST** yield `undefined` immediately. Child nodes that
  have not been inspected MUST be set to `ignored` in the RUML-result.
- If all child nodes yield `true`, it **MUST** yield `true`.

In `complete` mode, the evaluator MUST check all child results together in the following order

- If any child resulted in `false`, it MUST yield `false`
- If any child resulted in `undefined`, it MUST yield `undefined`
- If all child nodes resulted in `true`, it MUST yield `true`

**`NOT_AND`** MUST apply the same logic but yield `true` when `AND` would yield `false` and vice
versa

### 3.6.2 `OR` and `NOT_OR`

In `optimized` and `complete` mode, the evaluator MUST check all child results together in the
following order

- If any child resulted in `true`, it MUST yield `true`.
- If any child resulted in `undefined`, it MUST yield `undefined`.
- If all child nodes resulted in `false`, it MUST yield `false`.

**`NOT_OR`** MUST apply the same logic but yield `true` when `OR` would yield `false` and vice versa

### 3.6.3 `XOR` and `NOT_XOR`

:::note
`XOR` does not refer to the logical exclusive `XOR` (where two `true` inputs yield `false`), but to
the legal `XOR` meaning that child nodes are deliberately constructed such that only one can be
`true`. The evaluator behaves like a disjunction (`OR`) with early exit on the first `true`.
:::

In `optimized` mode, the evaluator MUST check the child node results one after another.

- If a child node yields `true`, it **MUST** yield `true` immediately. Child nodes that have not
  been inspected MUST be set to `ignored` in the RUML-result.
- If a child node yields `undefined`, it **MUST** yield `undefined` immediately. Child nodes that
  have not been inspected MUST be set to `ignored` in the RUML-result.
- If all child nodes yield `false`, it **MUST** yield `false`.

In `complete` mode, the evaluator MUST check all child results together in the following order

- If any child resulted in `true`, it MUST yield `true`.
- If any child resulted in `undefined`, it MUST yield `undefined`.
- If all child nodes resulted in `false`, it MUST yield `false`.

**`NOT_XOR`** MUST apply the same logic but yield `true` when `XOR` would yield `false` and vice
versa

### 3.6.4 The `DELEGATED` Operator

The `DELEGATED` operator uses a capability to compute the result from the child node results.

It can be used for combinations the logical operators cannot express, in particular threshold rules
("at least three of the following criteria"), tolerance rules ("at most one requirement may be
missing"), majority and quorum rules, and rules that negate a single child rather than the whole
node.

#### Binding to a combiner

The rule itself is carried by a **combiner** — a capability on the node that determines the node's
status from the results of its children. The official combiner is `ruml:expression` (see
[Chapter 4.14](../04-capabilities/4-14-ruml-expression.md)); a non-official can be used as well (see
_Custom combiners_ below).

A parent node has a combiner **if and only if** its operator is `DELEGATED`:

- Outside a draft, a node with `operator: "DELEGATED"` **MUST** have a non-empty `children` array; a
  node with `operator: "DELEGATED"` and `children` **MUST** carry exactly one capability entry whose
  capability has the `combiner` role (rule `OP-02`) ([`OP-02`](../08-validation/index.md#rule-op-02)). In a draft, a leaf node **MAY**
  have `operator: "DELEGATED"` without a combiner; the operator is ignored like any operator on a
  leaf ([`NODE-07`](../08-validation/index.md#rule-node-07)).
- A node carrying a combiner entry **MUST** use `operator: "DELEGATED"` (rule `CAP-08`)
  ([`CAP-08`](../08-validation/index.md#rule-cap-08)). A combiner therefore never sits on a leaf, nor on a node with a logical operator.

Neither half is valid alone. A tool that does not know the combiner therefore cannot mistake such a
node for a logical one: the operator is unknown to it and the file is rejected.

:::note[Exception to the leaf restriction]
A combiner carries the `combiner` role, not `decision`, and is the only kind of capability that
decides a node **with** children. The restriction in
[Chapter 4.1](../04-capabilities/4-1-concept.md) — decision capabilities are leaf-only — applies to
`ruml:query` and `ruml:ai-query`, which decide a node **instead of** its children. A combiner
decides a node **from** its children and therefore requires them.
:::

#### The combiner contract

The operator delegates the combination rule, not the guarantees that make a rulemap auditable. Every
combiner, official or not, **MUST**:

1. Yield `true`, `false` or no result — never a number, a string or a structure. Any other result
   **MUST** yield status `undefined`.
2. Carry a human-readable `description` in its node-level payload, stating the rule in prose. The
   operator `DELEGATED` does not say what the node does, so without this the rulemap cannot be
   reviewed without reading code (rule `OP-04`) ([`OP-04`](../08-validation/index.md#rule-op-04)).
3. Yield `undefined` without running as soon as any child is `undefined`; JSONata is two-valued and
   would otherwise count such a child as not fulfilled, so a threshold rule would look determined
   when it is not.
4. Consume all children: the operator **MUST NOT** short-circuit (rule `OP-03`) ([`OP-03`](../08-validation/index.md#rule-op-03)).

A combiner **SHOULD** be deterministic and reproducible from the same inputs. It **MAY** use
non-deterministic input, such as a random number or the current time ([`OP-05`](../08-validation/index.md#rule-op-05)); it then
**SHOULD** record the values it drew in the node result.

A combiner **SHOULD** record in the node result what it saw — at least the child statuses it
consumed, any datapoint values it read, and the value it computed — so the decision can be
reconstructed from the RUML-Result file alone.

The role of a capability says _where_ it may sit; this contract says _what it must deliver_ to sit
there. Together they are what a combiner is; RUML defines no separate capability type.

#### Custom combiners

Any capability with the `combiner` role MAY act as a combiner, including a third-party one under the
reverse-domain convention (see [Chapter 4.4](../04-capabilities/4-4-namespaces.md)) ([`OP-06`](../08-validation/index.md#rule-op-06)):

```jsonc
"capabilities": [
  {
    "id": "com.example/expression",
    "required": true,
    "role": "combiner"
  }
]
```

Whether a custom capability is a combiner is defined by the parser and evaluator that implement it.
Its root-level entry MUST declare the `combiner` role (rules `CAP-03`, `OP-02`); a parser that
implements the capability checks the declared role against its implementation (rule `CAP-04`)
([`CAP-03`](../08-validation/index.md#rule-cap-03), [`OP-02`](../08-validation/index.md#rule-op-02), [`CAP-04`](../08-validation/index.md#rule-cap-04)). See [Chapter 4.1](../04-capabilities/4-1-concept.md)
for the roles and the difference between `combiner` and `decision`.

`required: true` is what makes rule `CAP-01` reject the file in a tool that does not implement the
combiner, rather than leaving a node with an operator and no rule behind it.

:::caution[A custom combiner makes the rulemap non-portable]
An unknown _leaf_ decision capability leaves one leaf `undefined` while the rest of the rulemap
still evaluates. An unknown _combiner_, declared `required: true` as it must be, causes the whole
document to be rejected. A rulemap using a non-`ruml:` combiner is therefore readable only by tools
that implement it. The official combiner set grows by revision of this specification; a proprietary
combiner is a deliberate trade of portability for expressiveness.
:::

#### What the expression sees

The expression is evaluated against the same input document as a `ruml:query` expression, so
datapoints are addressed by their id (`dp_alter`). In addition, the results of the node's direct
children are bound to the variable `$children`:

| Field    | Type   | Description                                                                                         |
| -------- | ------ | --------------------------------------------------------------------------------------------------- |
| `lexId`  | String | The child's lexId                                                                                   |
| `label`  | String | The child's label                                                                                   |
| `status` | String | The child's status: `"true"` or `"false"` — the expression does not run when a child is `undefined` |

The array is in `children` order. Only **direct** children are visible; a deeper result is reached
by the intermediate node aggregating its own children in turn.

#### Evaluation rules

- The operator **MUST NOT** short-circuit. All children **MUST** be evaluated before the expression
  runs, and a node with `operator: "DELEGATED"` **MUST NOT** cause a child to receive status
  `ignored` with `reason.type: "shortCircuit"` ([`OP-03`](../08-validation/index.md#rule-op-03)). A count over partially evaluated
  children would be wrong rather than merely incomplete.
- The expression **MUST** evaluate to a boolean. Any other result — including no result — **MUST**
  yield status `undefined`, with a reason of type `default` whose `message` **SHOULD** name the
  offending value.
- Expressions **SHOULD** be deterministic. The non-deterministic JSONata functions `$random`, `$now`
  and `$millis`, and `$eval`, **MAY** be used; an expression using them is no longer guaranteed to
  be reproducible from the same inputs ([`OP-05`](../08-validation/index.md#rule-op-05)). `$eval` runs a string as an expression, so
  the rule actually applied need not be visible in `expression` itself — `description` then carries
  all the more weight.
- An expression whose result is equivalent to a logical operator (for example
  `$children[0].status = "true" and $children[1].status = "true"`) **SHOULD** be reported as a
  warning; the logical operator is the reviewable form.

#### Examples

At least three of the listed criteria:

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

At most one requirement may be missing:

```jsonc
"expression": "$count($children[status = 'false']) <= 1"
```

Majority of the children that were evaluated:

```jsonc
"expression": "$count($children[status = 'true']) * 2 > $count($children)"
```

Subsidiarity — the second child only applies if the first does not:

```jsonc
"expression": "$children[0].status = 'false' and $children[1].status = 'true'"
```

A fiction that overrides the children entirely:

```jsonc
"expression": "dp_alter >= 65 or $count($children[status = 'true']) = 3"
```

#### Recording the result

The node's result carries the expression, the child statuses it saw and the computed value, so the
decision can be reconstructed from the RUML-Result file alone — see
[Chapter 4.14](../04-capabilities/4-14-ruml-expression.md).

### 3.6.5 The `undefined` operator

`undefined` means the operator is not yet defined. It **MAY** be used during creation in files with
status `draft`, **MUST NOT** be used in files with any other status, and **MUST** be replaced by a
valid operator before finalization (status `review`, `approved`, `inForce`) ([`OP-07`](../08-validation/index.md#rule-op-07)). It is
the default value when creating a new node. On a leaf node (without `children`), the `operator` is
ignored; outside a draft, a leaf node **MUST NOT** have an `operator` at all, so `undefined` on a
leaf is removed rather than replaced ([`NODE-07`](../08-validation/index.md#rule-node-07)).

| **Status**                                                          | **Rule**                                                         |
| ------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `draft`                                                             | `undefined` **MAY** occur ([`OP-07`](../08-validation/index.md#rule-op-07))                         |
| `review`, `approved`, `inForce`, `suspended`, `expired`, `replaced` | `undefined` **MUST NOT** occur → validation error ([`OP-07`](../08-validation/index.md#rule-op-07)) |

Tools **SHOULD** display a warning for `undefined` operators. Tools **MAY** offer automatic
replacement with a default operator (e.g., `AND`).

## Conformance tests

- [3.6 Operators (AND)](../../../tests/03-data-model/3-6-operators--and.test.yaml)
- [3.6 Operators (DELEGATED validation)](../../../tests/03-data-model/3-6-operators--delegate.test.yaml)
- [3.6 Operators (DELEGATED evaluation)](../../../tests/03-data-model/3-6-operators--delegated-evaluation.test.yaml)
- [3.6 Operators (NOT_AND)](../../../tests/03-data-model/3-6-operators--not-and.test.yaml)
- [3.6 Operators (NOT_OR)](../../../tests/03-data-model/3-6-operators--not-or.test.yaml)
- [3.6 Operators (NOT_XOR)](../../../tests/03-data-model/3-6-operators--not-xor.test.yaml)
- [3.6 Operators (OR)](../../../tests/03-data-model/3-6-operators--or.test.yaml)
- [3.6 Operators (XOR)](../../../tests/03-data-model/3-6-operators--xor.test.yaml)
