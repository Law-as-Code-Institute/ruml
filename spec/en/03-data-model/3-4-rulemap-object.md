<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.4 Rulemap Object

The rulemap is the core of a RUML file and contains the hierarchical rule logic in a flat map
structure with `LexID` references.

### 3.4.1 Required Fields

| Field   | Type     | Description                                                                                                                                                                                                                                                                   |
| ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `nodes` | `Object` | **MUST** contain all nodes of the rulemap as a flat map. Keys are the LexIDs as strings (e.g., `"1"`, `"42"`). Values **MUST** be node objects according to [3.5](3-5-node-object.md) ([`NODE-02`](../08-validation/index.md#rule-node-02)). **MUST** contain an entry with key `"1"` (root node) ([`FMT-08`](../08-validation/index.md#rule-fmt-08)). |

**Structure example:**

```jsonc
"rulemap": {
  "nodes": {
    "1": {
      "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
      "operator": "AND",
      "label": "Credit worthiness check",
      "children": ["2", "3"]
    },
    "2": {
      "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
      "label": "Income verification"
    },
    "3": {
      "id": "95f566ad-b37c-4a18-b004-e83274d0fe83",
      "label": "Credit score check"
    }
  }
}
```

**Notes on structure:**

- The key IS the LexID — a separate `lexId` field in the node object is NOT required
- Direct lookup via `children` references: `nodes[String(childLexId)]`

### 3.4.2 Scope of the Rulemap Object

The `rulemap` object is the **structural layer** — it carries the decision tree and nothing else.
Descriptive information about the document (`title`, `description`, authors, status, identifiers, …)
lives in `metadata` (see [Chapter 3.3](3-3-metadata-object.md)); extensions live in `capabilities`
(see [Chapter 4](../04-capabilities/index.md)). `rulemap` therefore currently has exactly one field,
`nodes`; the object is retained (rather than hoisting `nodes` to the root) to keep this
structure/metadata/capabilities separation explicit and to provide a home for future tree-level
settings.
