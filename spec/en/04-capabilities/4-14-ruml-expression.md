<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.14 ruml:expression

## 4.14 Capability `ruml:expression`

### Overview

| Property               | Value                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| **Capability ID**      | `ruml:expression`                                                                           |
| **Scope**              | Root-Level (declaration) and Node-Level (`capabilities` entry with `id: "ruml:expression"`) |
| **Default `required`** | none — MUST be declared `true` ([`CAP-11`](../08-validation/index.md#rule-cap-11))                                              |
| **Role**               | `combiner`                                                                                  |

This Capability carries the expression that combines the results of a node's children when the node
uses `operator: "DELEGATED"` (see
[Chapter 3.6.4](../03-data-model/3-6-operators.md#364-the-delegated-operator)).

It is the **official combiner**: the one this specification defines and validates. A node may
instead delegate to a custom combiner — any capability declared at root with the `combiner` role —
which is bound by the same combiner contract but whose payload this specification does not describe.
`ruml:expression` is therefore best read as the reference implementation of that contract.

:::note[Distinction from other Capabilities]
`ruml:query` decides a Leaf-Node from data ([Chapter 4.8](4-8-ruml-query.md)), `ruml:ai-query`
decides a Leaf-Node with AI assistance ([Chapter 4.9](4-9-ruml-ai-query.md)). `ruml:expression`
decides a Parent-Node **from the results of its children**, and therefore requires them.
:::

### Root-Level Declaration

```jsonc
"capabilities": [
  {
    "id": "ruml:expression",
    "required": true
  }
]
```

A file using `ruml:expression` **MUST** declare it with `required: true`; a declaration that omits
`required` or sets it to `false` is invalid ([`CAP-11`](../08-validation/index.md#rule-cap-11)). A tool that does not support the
capability cannot combine the children of such a node in any defensible way; under rule `CAP-01` the
`required: true` declaration makes it reject the file instead of falling back to a logical operator
and producing a decision the rulemap does not state.

### Node-Level Value

```jsonc
"2": {
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

#### Node-Level Fields

| **Field**     | **Type** | **Required** | **Description**                                                                    |
| ------------- | -------- | ------------ | ---------------------------------------------------------------------------------- |
| `expression`  | String   | Yes          | MUST contain a JSONata expression computing the node's truth value ([`CAP-38`](../08-validation/index.md#rule-cap-38)) |
| `description` | String   | Yes          | MUST state, in prose, the rule the expression encodes ([`OP-04`](../08-validation/index.md#rule-op-04))               |

`description` is required here although it is optional for `ruml:query`. A logical operator says
what a node does by its name; `DELEGATED` does not, so without the prose statement the rulemap is no
longer readable without reading code. Tools **SHOULD** display it wherever they display the
operator.

#### Expression Format

Expressions MUST be written in **JSONata** and MUST evaluate to `true`, `false`, or no result. The
input document is the one used for `ruml:query` — datapoints are addressed by their id — extended by
the bound variable `$children`:

| Field    | Type   | Description           |
| -------- | ------ | --------------------- |
| `lexId`  | String | The child's lexId     |
| `label`  | String | The child's label     |
| `status` | String | `"true"` or `"false"` |

Only **direct** children are bound. The array follows the order of the node's `children` array.

### Evaluation Rules

- A node carrying a `ruml:expression` entry MUST have `operator: "DELEGATED"` and a non-empty
  `children` array ([`OP-02`](../08-validation/index.md#rule-op-02), [`CAP-08`](../08-validation/index.md#rule-cap-08))
- A node MUST NOT carry more than one `ruml:expression` entry ([`OP-02`](../08-validation/index.md#rule-op-02))
- All children MUST be evaluated before the expression runs; the operator MUST NOT short-circuit
  (see [Chapter 3.6.4](../03-data-model/3-6-operators.md#364-the-delegated-operator))
- If any child is `undefined`, the node is `undefined` and the expression MUST NOT be evaluated (see
  [Chapter 3.6.4](../03-data-model/3-6-operators.md#364-the-delegated-operator)); `$children`
  therefore only ever holds `"true"` and `"false"`
- A result that is not a boolean MUST yield status `undefined`
- Expressions SHOULD be deterministic; `$random`, `$now`, `$millis` and `$eval` MAY be used (see
  [Chapter 3.6.4](../03-data-model/3-6-operators.md#364-the-delegated-operator)) ([`OP-05`](../08-validation/index.md#rule-op-05)). The
  node result records `inputs` and `children` but not the values these functions return, so the
  result of such an expression cannot be reproduced from the RUML-Result file alone
- All DataPoint IDs referenced in the expression MUST be defined in the `ruml:datapoints` Capability
  (referential integrity, [`DP-18`](../08-validation/index.md#rule-dp-18))

### Expression Patterns

| Pattern                                                      | Expression                                                                           |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| At least _n_ of the children                                 | `$count($children[status = "true"]) >= 3`                                            |
| At most _n_ may fail                                         | `$count($children[status = "false"]) <= 1`                                           |
| All but a named child                                        | `$count($children[lexId != "7" and status = "false"]) = 0`                           |
| Simple majority                                              | `$count($children[status = "true"]) * 2 > $count($children)`                         |
| Qualified majority (two thirds)                              | `$count($children[status = "true"]) * 3 >= $count($children) * 2`                    |
| A specific child decides                                     | `$children[lexId = "4"].status = "true"`                                             |
| Subsidiarity — the second applies only if the first does not | `$children[lexId = "4"].status = "false" and $children[lexId = "5"].status = "true"` |
| At least one out of a named subset                           | `$count($children[lexId in ["4", "5"] and status = "true"]) >= 1`                    |
| Data overrides the children (statutory fiction)              | `dp_alter >= 65 or $count($children[status = "true"]) = 3`                           |

Worked example. The node has five children and the expression
`$count($children[status = "true"]) >= 3`:

```jsonc
"$children": [
  {
    "lexId": "4",
    "label": "Merkmal 1",
    "status": "true"
  },
  {
    "lexId": "5",
    "label": "Merkmal 2",
    "status": "false"
  },
  {
    "lexId": "6",
    "label": "Merkmal 3",
    "status": "true"
  },
  {
    "lexId": "7",
    "label": "Merkmal 4",
    "status": "true"
  },
  {
    "lexId": "8",
    "label": "Merkmal 5",
    "status": "false"
  }
]
```

`$children[status = "true"]` selects the entries with lexIds `4`, `6` and `7`; `$count` of them is
`3`; `3 >= 3` is `true`, so the node's status is `true`.

:::caution[Address children by `lexId`, not by position]
`$children[0]` is the **first** child (JSONata array indices are zero-based), `$children[1]` the
second. `$children[lexId = "4"]` instead selects by identity. Positional expressions silently change
meaning when a child is inserted, removed or reordered — in a rulemap that outlives several
amendments, that is how an expression comes to encode a different rule than the one it was reviewed
as. Addressing by `lexId` is therefore RECOMMENDED wherever a specific child is meant.
:::

### Combination with Other Capabilities

A node using `operator: "DELEGATED"` carries exactly one combiner, but MAY carry `data`- and
`reaction`-role capabilities alongside it, in any order ([`CAP-16`](../08-validation/index.md#rule-cap-16)):

```jsonc
"2": {
  "id": "fcf02185-ffee-48a4-bf93-d2fb1b17944d",
  "operator": "DELEGATED",
  "label": "Härtefall liegt vor",
  "children": ["4", "5", "6"],
  "capabilities": [
    {
      "id": "ruml:text-reference",
      "payload": {
        "refs": [
          {
            "id": "text_sgb_xii_90",
            "type": "represents"
          }
        ]
      }
    },
    {
      "id": "ruml:expression",
      "payload": {
        "description": "Mindestens zwei der drei Härtefallmerkmale müssen vorliegen",
        "expression": "$count($children[status = \"true\"]) >= 2"
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "onTrue": {
          "operation": "createDocument",
          "ref": "haertefall_bescheid"
        }
      }
    }
  ]
}
```

The text reference supplies the norm the rule implements, the combiner decides the node, and the
action reacts to the decided status. Only the combiner influences the status.

### Custom Combiners

A node MAY delegate to a non-official combiner instead. The capability is declared at root with the
`combiner` role, since a parser cannot learn the role of a third-party capability from its id (see
[Chapter 4.1](4-1-concept.md)):

```jsonc
"capabilities": [
  {
    "id": "com.example/expression",
    "required": true,
    "role": "combiner"
  }
]
```

```jsonc
"1": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "operator": "DELEGATED",
  "label": "Gewichtete Gesamtbewertung",
  "children": ["2", "3", "4"],
  "capabilities": [
    {
      "id": "com.example/expression",
      "payload": {
        "description": "Gewichtete Punktsumme ab 27 Punkten",
        "expression": "weightedScore(children) >= 27"
      }
    }
  ]
}
```

The payload shape is the provider's, not this specification's — but the combiner contract in
[Chapter 3.6.4](../03-data-model/3-6-operators.md#364-the-delegated-operator) still binds it: a
boolean result, a prose `description`, an `undefined` result whenever a child is `undefined`, and no
short-circuiting. A capability declared `role: "decision"` decides a leaf from data and MUST NOT be
used here; it would be handed children it never reads.

### Node-Result Payload

The node result records what the expression saw, so the decision can be reconstructed from the
RUML-Result file alone (see [Chapter 5.1](../05-result-format/5-1-result-model.md)):

| Field        | Type   | Required | Description                                                                                                                   |
| ------------ | ------ | -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `expression` | String | Yes      | The evaluated expression                                                                                                      |
| `inputs`     | Object | Yes      | Resolved datapoint values referenced by the expression, keyed by DataPoint ID; an empty object when the expression reads none |
| `children`   | Array  | Yes      | The child results the expression saw, as `{ lexId, status }`, in `children` order                                             |
| `result`     | Enum   | Yes      | Computed result: `true`, `false`, `undefined`                                                                                 |

Additional fields are NOT permitted.

```jsonc
"1.2": {
  "lexId": "3",
  "status": "true",
  "evaluatedAt": "2024-01-15T10:00:04Z",
  "reason": "3 von 5 Merkmalen erfüllt (Schwelle: 3)",
  "capabilities": [
    {
      "id": "ruml:expression",
      "payload": {
        "expression": "$count($children[status = 'true']) >= 3",
        "inputs": {},
        "children": [
          {
            "lexId": "4",
            "status": "true"
          },
          {
            "lexId": "5",
            "status": "false"
          },
          {
            "lexId": "6",
            "status": "true"
          },
          {
            "lexId": "7",
            "status": "true"
          },
          {
            "lexId": "8",
            "status": "false"
          }
        ],
        "result": "true"
      }
    }
  ]
}
```

`inputs` is empty above because that expression reads only `$children`. An expression MAY also read
datapoints — they are addressed exactly as in `ruml:query` — and then the values that co-determined
the node MUST be recorded, or the result file would not explain the outcome:

```jsonc
"1.3": {
  "lexId": "9",
  "status": "true",
  "reason": "Fiktion: Antragsteller ist 67 Jahre alt",
  "capabilities": [
    {
      "id": "ruml:expression",
      "payload": {
        "expression": "dp_alter >= 65 or $count($children[status = 'true']) = 3",
        "inputs": {
          "dp_alter": 67
        },
        "children": [
          {
            "lexId": "10",
            "status": "true"
          },
          {
            "lexId": "11",
            "status": "false"
          },
          {
            "lexId": "12",
            "status": "false"
          }
        ],
        "result": "true"
      }
    }
  ]
}
```

Only one of the three children is `true`, so without `inputs` the recorded result would show a node
decided `true` against its own children with nothing to account for it. This is the case the field
exists for.

### Complete Example

A hardship check: at least two of three criteria must be met, and the applicant must be resident in
the Land.

**File 1: `haertefall.ruml`**

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_pflegegrad": {
            "name": "Pflegegrad",
            "type": "integer",
            "binding": {
              "type": "input"
            }
          },
          "dp_eigenanteil": {
            "name": "Monatlicher Eigenanteil",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            }
          },
          "dp_alleinlebend": {
            "name": "Alleinlebend",
            "type": "boolean",
            "binding": {
              "type": "input"
            }
          },
          "dp_wohnsitz": {
            "name": "Wohnsitz im Land",
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
      "id": "ruml:expression",
      "required": true
    }
  ],
  "metadata": {
    "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
    "version": "1.0.0",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z",
    "created": "2024-01-10T09:00:00Z",
    "modified": "2024-01-10T09:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
        "operator": "AND",
        "label": "Härtefallleistung",
        "children": ["2", "7"]
      },
      "2": {
        "id": "42d9431d-b7db-404f-bdf9-7ecdde505cce",
        "operator": "DELEGATED",
        "label": "Härtefall liegt vor",
        "children": ["3", "4", "5"],
        "capabilities": [
          {
            "id": "ruml:expression",
            "payload": {
              "description": "Mindestens zwei der drei Härtefallmerkmale müssen vorliegen",
              "expression": "$count($children[status = \"true\"]) >= 2"
            }
          }
        ]
      },
      "3": {
        "id": "52820488-2849-4487-842b-952dc3ba301d",
        "label": "Pflegegrad mindestens 3",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_pflegegrad >= 3"
            }
          }
        ]
      },
      "4": {
        "id": "48b34df4-06bb-4dc2-aeb7-807a146760f4",
        "label": "Eigenanteil über 800 EUR",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_eigenanteil > 800"
            }
          }
        ]
      },
      "5": {
        "id": "92f909f1-0097-4d9d-87d2-1734bf299d08",
        "label": "Alleinlebend",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_alleinlebend = true"
            }
          }
        ]
      },
      "7": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "label": "Wohnsitz im Land",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_wohnsitz = true"
            }
          }
        ]
      }
    }
  }
}
```

**File 2: `haertefall-fall-00123.ruml-result`**

Note that node `1.1.2` is `false` and yet no child is `ignored`: the `DELEGATED` operator evaluates
all of them, because the count would otherwise be taken over a partial set.

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "b6620b3c-4279-4a45-9115-c8bb2032d868"
  },
  "evaluation": {
    "id": "7f3d1c88-2b4e-4a19-9c5d-0e6f1a2b3c4d",
    "timestamp": "2024-01-15T10:00:00Z",
    "mode": "complete",
    "caseId": "Antrag-2024-00123",
    "capabilities": [
      {
        "id": "ruml:datapoints"
      },
      {
        "id": "ruml:query"
      },
      {
        "id": "ruml:expression"
      }
    ],
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "reason": "AND: alle Kinder true"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "reason": "2 von 3 Merkmalen erfüllt (Schwelle: 2)",
        "capabilities": [
          {
            "id": "ruml:expression",
            "payload": {
              "expression": "$count($children[status = \"true\"]) >= 2",
              "inputs": {},
              "children": [
                {
                  "lexId": "3",
                  "status": "true"
                },
                {
                  "lexId": "4",
                  "status": "false"
                },
                {
                  "lexId": "5",
                  "status": "true"
                }
              ],
              "result": "true"
            }
          }
        ]
      },
      "1.1.1": {
        "lexId": "3",
        "status": "true",
        "reason": "Pflegegrad 4 >= 3"
      },
      "1.1.2": {
        "lexId": "4",
        "status": "false",
        "reason": "Eigenanteil 640 EUR <= 800 EUR"
      },
      "1.1.3": {
        "lexId": "5",
        "status": "true",
        "reason": "Alleinlebend"
      },
      "1.2": {
        "lexId": "7",
        "status": "true",
        "reason": "Wohnsitz im Land"
      }
    }
  }
}
```

### Not Available via RUML-EXT (Sidecar)

`ruml:expression` MUST NOT be delivered in a RUML-EXT file, and its id is deliberately absent from
the RUML-EXT schema ([`CAP-37`](../08-validation/index.md#rule-cap-37)).

A RUML-EXT file extends nodes that already exist in the base file ([Chapter 4.5](4-5-ruml-ext.md)).
A base node with `operator: "DELEGATED"` and children already has its combiner (rule `OP-02`), and a
second one would violate rule `OP-02`; on a leaf node, `ruml:expression` lacks the children it
requires, and on any other node it violates rule `CAP-08`. A sidecar therefore has no node to which
it could validly add the entry. The restriction is a consequence of the binding rules rather than an
additional one.

This is the intended behaviour: `ruml:text-reference` or `ruml:context` add material **about** a
decision, while `ruml:expression` **is** the decision. What a rulemap decides belongs in the signed
and hashed base file, not in a companion file that may be absent.

### Planned Extension: Values from the Subtree

Threshold rules over a **count** of fulfilled children are covered by `$children[].status` alone.
Rules over a **sum** — point-based assessments, totalled amounts — additionally need a number per
node, which RUML does not yet carry.

The intended direction is that a node may declare a `ruml:datapoints` entry at node level whose
entries use `binding.type: "computed"`, determining a datapoint from that node's scope; the
determined value would then be readable on `$children[]` by its datapoint id. That extension is
**not** part of this chapter and not yet in the schema; the fields listed under _Expression Format_
are the complete set.
