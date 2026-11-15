<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.3 Capability Data on Nodes

### Overview

Each node MAY carry its own `capabilities` field — independent of the identically named
`capabilities` array at root level (see [Chapter 4.2](4-2-capabilities-field.md)). It contains the
extension data for the capabilities applicable to this node.

The field is part of the optional fields of the node object (see
[Chapter 3.5.3](../03-data-model/3-5-node-object.md)) and is subject to the same general rules: it
does not need to be present; its absence has no effect on core processing.

### Structure

```jsonc
"capabilities": [
  {
    "id": "ruml:query",
    "payload": {/* ... */}
  },
  {
    "id": "ruml:draft/ai-annotations",
    "payload": {/* ... */}
  }
]
```

- **`id`:** A capability ID that is declared in the root-level `capabilities` array.
- **`payload`:** An object whose inner structure is defined by the respective capability
  specification.

Both fields are required: every entry MUST contain `id` and `payload` ([`CAP-17`](../08-validation/index.md#rule-cap-17)). A capability
without node-level data, such as `ruml:protocol`, therefore MUST NOT appear in a node's
`capabilities` array ([`CAP-18`](../08-validation/index.md#rule-cap-18)).

### Referential Integrity

The `id` of each entry in a node's `capabilities` array MUST be a capability ID that is declared in
the root-level `capabilities` array ([`CAP-15`](../08-validation/index.md#rule-cap-15)).

:::warning[Invalid Capability Reference]
If a node's `capabilities` array contains an entry whose `id` is **not** declared in the root-level
`capabilities` array, the parser MUST treat this as a validation error ([`CAP-15`](../08-validation/index.md#rule-cap-15)). This rule
applies regardless of whether the parser knows the capability's content or not.
:::

**Invalid** — `org.ruml.test/decision` is not declared in the root `capabilities` array:

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "org.ruml.test/data",
      "role": "data"
    }
  ],
  "metadata": {
    "id": "fa906bd6-24f1-47f3-8ad5-ae3d5c745b56",
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
        "label": "Anspruch auf Schadensersatz",
        "capabilities": [
          {
            "id": "org.ruml.test/decision",
            "payload": {
              "result": "true"
            }
          }
        ]
      }
    }
  }
}
```

**Valid** — capability correctly declared:

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "com.example/review-notes",
      "role": "data"
    }
  ],
  "metadata": {
    "id": "dc456c3b-cfa6-44a8-9617-cb5119bbe1ee",
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
        "label": "Anspruch auf Schadensersatz",
        "capabilities": [
          {
            "id": "com.example/review-notes",
            "payload": {
              "status": "pending"
            }
          }
        ]
      }
    }
  }
}
```

### Applicability to Node Types

The `capabilities` field MAY appear on any node type: root node, parent node, and leaf node
([`CAP-16`](../08-validation/index.md#rule-cap-16)).

**Restriction for decision-relevant capabilities:** Capabilities with the `decision` role MUST NOT
be applied to anything other than leaf nodes ([`CAP-07`](../08-validation/index.md#rule-cap-07)). The status of root and parent nodes is
determined exclusively by the tree structure and operators (see
[Chapter 3.6](../03-data-model/3-6-operators.md)). The role of each capability is defined in its
specification (see [Chapter 4.1](4-1-concept.md)).

Capabilities with the `data` or `reaction` role MAY appear on any node type ([`CAP-16`](../08-validation/index.md#rule-cap-16)).

Likewise, it MAY appear on modular nodes (`modular: true`) and on nodes within modular subtrees. For
modular nodes, the `capabilities` data applies to **all instantiations** of the node (see
[Chapter 3.5.3](../03-data-model/3-5-node-object.md)).

### Repeated Capability IDs

Unlike the root-level array, whose ids are unique (see
[Chapter 4.2](4-2-capabilities-field.md#uniqueness)), a node's `capabilities` array MAY contain the
same `id` more than once if the capability's role allows it (see [Chapter 4.1](4-1-concept.md)):

| **Role**   | **Same `id` more than once on a node**                                                                    |
| ---------- | --------------------------------------------------------------------------------------------------------- |
| `data`     | MUST NOT. One entry carries all of the node's data for that capability.                                   |
| `decision` | MAY, e.g. two `ruml:query` entries with different expressions; `decisionMode` combines their results.     |
| `combiner` | MUST NOT. A node carries at most one combiner anyway ([`OP-02`](../08-validation/index.md#rule-op-02)).                                      |
| `reaction` | MAY, e.g. two `ruml:actions` entries; they are processed in list order (see [Field Order](#field-order)). |

The rule counts entries with the same `id`, not entries with the same role: a node MAY carry
`ruml:text-reference` and `ruml:context` side by side. The schema enforces it for the official
`data` capabilities; for `ruml:draft/` and third-party ids the role comes from the root-level
declaration, so the check is a parser obligation ([`CAP-06`](../08-validation/index.md#rule-cap-06)).

### Payload Type

The `payload` MUST be an object ([`CAP-17`](../08-validation/index.md#rule-cap-17)). Arrays, primitive values, and `null` MUST NOT be
used; a capability that carries a list places it in a named field of the object. The object's inner
structure is defined by the capability specification.

```jsonc
"capabilities": [
  {
    "id": "com.example/review-notes",
    "payload": {
      "status": "approved",
      "reviewer": "rechtsabteilung"
    }
  },
  {
    "id": "ruml:draft/ai-annotations",
    "payload": {
      "annotations": [
        {
          "type": "confidence",
          "value": 0.92
        },
        {
          "type": "source",
          "value": "gpt-4o"
        }
      ]
    }
  }
]
```

### Complete Node Example

The following example shows a leaf node with two different capability extensions:

```jsonc
"2": {
  "id": "f32b5875-2557-499a-a9b5-bd5efdeab0fd",
  "label": "Volljährigkeit nachgewiesen",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_age >= 18"
      }
    },
    {
      "id": "ruml:draft/ai-annotations",
      "payload": {
        "confidence": 0.97,
        "lastReviewed": "2024-09-15",
        "reviewer": "llm-assistant-v2"
      }
    }
  ]
}
```

### Combination Mode (`decisionMode`)

If a leaf node contains multiple capabilities with the `decision` role, the optional `decisionMode`
field on the node determines how the results are combined:

| `decisionMode` | Behavior                                                                                                                                                                                                                                                                                            |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fallback`     | Capabilities are evaluated in list order. The first definitive answer (`true`/`false`) determines the node status. On `undefined`, the next decision capability is evaluated; if none gives a definitive answer, the result is `undefined`. This is the **default** when `decisionMode` is not set. |
| `agreement`    | All decision capabilities MUST agree. All MUST be evaluated. On disagreement (e.g., one returns `true`, another returns `false`), the result is `undefined`.                                                                                                                                        |
| `majority`     | Majority vote across all decision capabilities. All MUST be evaluated. On a tie, the result is `undefined`.                                                                                                                                                                                         |

Example:

```jsonc
"3": {
  "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
  "label": "Antragsteller volljährig",
  "decisionMode": "fallback",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_age >= 18"
      }
    },
    {
      "id": "ruml:ai-query",
      "payload": {
        "model": "fast",
        "prompt": "Ist der Antragsteller volljährig?"
      }
    }
  ]
}
```

**Rules:**

- `decisionMode` is an optional field on the node object (see
  [Chapter 3.5.3](../03-data-model/3-5-node-object.md)), NOT in the `capabilities` array.
- `decisionMode` only has an effect on leaf nodes. On parent nodes it MUST be ignored
  ([`CAP-19`](../08-validation/index.md#rule-cap-19)).
- If a leaf node has exactly one `decision` capability, `decisionMode` is irrelevant and SHOULD NOT
  be set.
- With `fallback`, the order of entries in the `capabilities` list determines the evaluation order.
  Authors SHOULD place the preferred decision capability first.

### Field Order

The `capabilities` list is ordered and the order is significant: capabilities are processed in list
order, and tools MUST preserve it when reading and writing a file and MUST NOT reorder the entries —
for example to sort them by capability ID ([`CAP-20`](../08-validation/index.md#rule-cap-20)). Reordering entries is a change to the
document, not a formatting choice — with `decisionMode: "fallback"` it changes which capability
decides the node.

### Relationship to `metadata` at Node Level

The optional `metadata` field of a node (see [Chapter 3.5.3](../03-data-model/3-5-node-object.md))
is intended for **non-structural** information not associated with any capability. The
`capabilities` field is intended for **declared, capability-bound** extension data. Both fields MAY
be present simultaneously.

```jsonc
"4": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "label": "Ausnahmetatbestand",
  "metadata": {
    "author": "Dr. Müller",
    "lastEditedBy": "validator-bot"
  },
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_age >= 18"
      }
    }
  ]
}
```

## Conformance tests

- [4.3 Capability Data on Nodes](../../../tests/04-capabilities/4-3-capabilities-node-field.test.yaml)
