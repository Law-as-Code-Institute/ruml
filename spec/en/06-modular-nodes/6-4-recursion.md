<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.4 Recursion

Modular nodes **MAY** contain themselves as a child (recursion). ([`MOD-02`](../08-validation/index.md#rule-mod-02)) This enables
modeling of processes with unknown iteration depth, such as contract negotiations.

---

### Structure of Recursive Nodes

A recursive node is a modular node that contains its own `lexId` in the `children` array:

```jsonc
"4": {
  "id": "7d3f2a91-5c6e-4b8a-9f1d-2e4c6a8b0d13",
  "modular": true,
  "operator": "XOR",
  "label": "Verhandlungsrunde",
  "children": [
    "5",
    "6",
    "4" // ← self-reference
  ]
}
```

---

### Safe Recursion

Recursion can lead to infinite loops. Safe recursion is **ONLY** possible when **BOTH** conditions
are met:

1. The operator of the recursive node is `XOR` or `NOT_XOR`
2. The recursive self-reference is **NOT** positioned as the first child

**Rationale:** With `XOR`/`NOT_XOR`, evaluation terminates as soon as a child becomes `true`. If a
non-recursive child (exit condition) before the self-reference becomes `true`, evaluation ends — the
recursion is not entered.

---

### Maximum Recursion Depth

Implementations MUST define a maximum recursion depth to prevent infinite loops and MUST return
`undefined` for a node result above the maximum recursion depth.

| Aspect                 | Requirement                                                                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Default maximum        | 500 levels                                                                                                                               |
| Configurability        | **SHOULD** be configurable                                                                                                               |
| Behavior on exceedance | Node receives status `undefined` with a reason of type `error` (see [5.0](../05-result-format/5-0-status-types.md)); the error is logged |

The recursion depth of a node instance counts the self-references on its path: the first instance of
a recursive node has depth 0, and each time the node contains itself, the depth grows by 1. In the
[complete example](#complete-example) below:

| Path      | Instance                             | Recursion depth |
| --------- | ------------------------------------ | --------------- |
| `1.2`     | Negotiation round (lexId 4), round 1 | 0               |
| `1.2.3`   | Negotiation round (lexId 4), round 2 | 1               |
| `1.2.3.3` | Negotiation round (lexId 4), round 3 | 2               |

With a maximum of _n_, instances up to depth _n_ are evaluated; an instance at depth _n_ + 1 is the
one that receives status `undefined`. The recursion depth is not the depth of the path: nodes above
the recursive node do not count.

---

### Complete Example

**Use case:** Contract negotiation with any number of rounds

**Structure:**

```
Root (AND, lexId: 1)
├── Vertragsfähigkeit geprüft (Leaf, lexId: 2)
└── Verhandlungsrunde (XOR, lexId: 4, modular, recursive)
    ├── Angebot angenommen (Leaf, lexId: 5)
    ├── Verhandlung abgebrochen (Leaf, lexId: 6)
    └── [Recursion → lexId: 4]
```

---

**RUML file (static):**

```jsonc
"rulemap": {
  "nodes": {
    "1": {
      "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
      "operator": "AND",
      "label": "Vertragsabschluss",
      "children": ["2", "4"]
    },
    "2": {
      "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
      "label": "Vertragsfähigkeit geprüft",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_legal_capacity = true"
          }
        }
      ]
    },
    "4": {
      "id": "7d3f2a91-5c6e-4b8a-9f1d-2e4c6a8b0d13",
      "modular": true,
      "operator": "XOR",
      "label": "Verhandlungsrunde",
      "children": ["5", "6", "4"]
    },
    "5": {
      "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
      "label": "Angebot angenommen",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_offer_accepted = true"
          }
        }
      ]
    },
    "6": {
      "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
      "label": "Verhandlung abgebrochen",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_negotiation_cancelled = true"
          }
        }
      ]
    }
  }
}
```

**Evaluation result after two negotiation rounds:**

Scenario: First round — no result, second round — offer accepted.

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d9c7e5c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e"
  },
  "evaluation": {
    "id": "20453004-30ad-4a39-9be3-0c687754948f",
    "timestamp": "2024-01-15T10:00:00Z",
    "mode": "optimized",
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "reason": "AND: alle Kinder true"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "reason": "Vertragsfähigkeit bestätigt"
      },
      "1.2": {
        "lexId": "4",
        "status": "true",
        "reason": "XOR: Kind 1.2.3 ist true (Rekursion betreten)"
      },
      "1.2.1": {
        "lexId": "5",
        "status": "false",
        "reason": "Angebot nicht angenommen"
      },
      "1.2.2": {
        "lexId": "6",
        "status": "false",
        "reason": "Verhandlung nicht abgebrochen"
      },
      "1.2.3": {
        "lexId": "4",
        "status": "true",
        "reason": "XOR: Angebot angenommen (Rekursionsebene 1)"
      },
      "1.2.3.1": {
        "lexId": "5",
        "status": "true",
        "reason": "Angebot angenommen"
      },
      "1.2.3.2": {
        "lexId": "6",
        "status": "ignored",
        "reason": {
          "type": "shortCircuit",
          "trigger": "Knoten 1.2.3.1 wurde true",
          "operator": "XOR",
          "mode": "optimized"
        }
      },
      "1.2.3.3": {
        "lexId": "4",
        "status": "ignored",
        "reason": {
          "type": "shortCircuit",
          "trigger": "Knoten 1.2.3.1 wurde true",
          "operator": "XOR",
          "mode": "optimized"
        }
      }
    }
  }
}
```

**Note:** The paths `1.2.3`, `1.2.3.1`, `1.2.3.2` and `1.2.3.3` in the `results` object are
dynamically generated — they are computed at runtime from the tree structure.

---

### UI Representation

Implementations **SHOULD** visually distinguish recursive nodes:

| Aspect              | Recommendation                                 |
| ------------------- | ---------------------------------------------- |
| **Symbol**          | Special icon to identify recursive nodes       |
| **Expansion**       | Click on symbol opens the next recursion level |
| **Depth indicator** | Display of the current recursion depth         |
| **Maximum warning** | Warning when approaching the maximum depth     |

---

### Validation Rules

| Rule                                     | Description                                                                                                                                                                                                                                                            |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Self-reference only with `modular: true` | A node without `modular: true` **MUST NOT** reference itself ([`MOD-01`](../08-validation/index.md#rule-mod-01))                                                                                                                                                                                           |
| Operator recommendation                  | Recursive nodes **SHOULD NOT** use the operator `AND`, `NOT_AND`, `OR`, or `NOT_OR`, as this can lead to potentially unresolvable decision logic                                                                                                                       |
| Runtime warning                          | Implementations **MUST** issue a warning when a recursive node operates with `AND`, `NOT_AND`, `OR`, or `NOT_OR`. This warning is not cycle detection (depth limit, see Maximum Recursion Depth), but an indication of semantically blocked evaluation ([`MOD-03`](../08-validation/index.md#rule-mod-03)) |
| Position of self-reference               | The self-reference **MUST NOT** be at position 0 in the `children` array ([`MOD-04`](../08-validation/index.md#rule-mod-04))                                                                                                                                                                               |
| At least one exit condition              | Recursive nodes **MUST** have at least one non-recursive child ([`MOD-05`](../08-validation/index.md#rule-mod-05))                                                                                                                                                                                         |

**Note:** The validation of these rules is defined in Chapter 8.
