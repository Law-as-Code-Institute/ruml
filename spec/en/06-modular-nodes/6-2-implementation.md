<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.2 Implementation

---

### Definition of Modular Nodes

A node is **modular** if it is referenced more than once: its `lexId` appears more than once in the
`children` arrays of the rulemap, under different parent nodes or twice under the same one. The
self-reference of a recursive node counts as one of these references (see [6.4](6-4-recursion.md)).

- A modular node exists exactly once in the `nodes` object
- A modular node **MUST** have `modular: true` ([`MOD-01`](../08-validation/index.md#rule-mod-01))
- A node that is not modular **SHOULD NOT** have `modular: true`

---

**Identification of children:**

- Whether a node is part of a modular subtree is derived from the tree structure and determined at
  runtime

---

**Example of multiple referencing:**

```jsonc
"rulemap": {
  "nodes": {
    "1": {
      "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
      "operator": "AND",
      "label": "Hauptprüfung",
      "children": ["2", "8", "10"]
    },
    "2": {
      "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
      "label": "Antragsteller volljährig",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_age >= 18"
          }
        }
      ]
    },
    "8": {
      "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
      "modular": true,
      "operator": "AND",
      "label": "Standardprüfung Bonität",
      "children": ["9", "11"]
    },
    "9": {
      "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
      "label": "Einkommensprüfung",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_income > 30000"
          }
        }
      ]
    },
    "10": {
      "id": "42d9431d-b7db-404f-bdf9-7ecdde505cce",
      "operator": "OR",
      "label": "Alternative Prüfungen",
      "children": ["8", "12"]
    },
    "11": {
      "id": "52820488-2849-4487-842b-952dc3ba301d",
      "label": "Schufa-Score",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_schufa >= 600"
          }
        }
      ]
    },
    "12": {
      "id": "48b34df4-06bb-4dc2-aeb7-807a146760f4",
      "label": "Bürgschaft vorhanden",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_guarantor = true"
          }
        }
      ]
    }
  }
}
```

---

**Note on the example:** The `lexId: 8` (Standardprüfung Bonität) is referenced twice — once by node
1 (`children: [2, 8, 10]`) and once by node 10 (`children: [8, 12]`). The node itself exists only
once in the `nodes` object.

---

**Missing** `modular` flag for multiple referencing:

_Invalid_

```jsonc
"nodes": {
  "1": {
    "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
    "operator": "AND",
    "label": "Antrag",
    "children": ["2", "3"]
  },
  "2": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "operator": "AND",
    "label": "Antrag A",
    "children": ["5"]
  },
  "3": {
    "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
    "operator": "AND",
    "label": "Antrag B",
    "children": ["5"]
  },
  "5": {
    // 'modular' is not set
    "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
    "label": "Mehrfach referenziert"
  }
}
```

---

**Note on text anchors for modular nodes:**

The anchors of the node-level `ruml:text-reference` capability (see
[Chapter 4.12](../04-capabilities/4-12-ruml-text-reference.md#node-level-anchors)) behave
differently for modular nodes than the path-dependent evaluation: they are a property of the **node
definition**, not of the instantiation.

This means: A modular node marks the same norm with its `represents` anchor at all its usage
locations. When the same verification node is used at two positions in the rule tree, its anchors
apply equally at both locations — they always name the same paragraph, section, or sentence of the
source text.

**Rationale:** Since a modular node conceptually represents a rule check that is reused at multiple
locations, it is always based on one legal basis. Different anchors per instance would contradict
the concept of modular reuse.

## Conformance tests

- [6.2 Implementation](../../../tests/06-modular-nodes/6-2-implementation.test.yaml)
