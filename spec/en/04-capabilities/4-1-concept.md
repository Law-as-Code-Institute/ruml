<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.1 Concept

### What Capabilities Provide

The RUML core structure (Chapters 1–3) serves to represent regulations and laws as machine-readable
decision trees — with nodes, operators, legal references, and metadata. This structure is complete
and stable, but intentionally passive: it describes _what_ should be evaluated, not _how_ the
evaluation is performed.

Capabilities fulfill two roles:

**1. Decision-Making Ability** — They make a rulemap executable. They define:

- **What** decisions are based on — e.g., typed data points (`ruml:datapoints`), data-based queries
  (`ruml:query`), AI models (`ruml:ai-query`)
- **How** decisions are made — expressions, prompts, external bindings
- **What happens next** — triggered actions (`ruml:actions`)
- **What the decision relies on** — normative texts (`ruml:text-reference`), nodes of other rulemaps
  (`ruml:tree-reference`, `ruml:tree-include`), context materials (`ruml:context`)

**2. Extensibility** — The capabilities system additionally provides a controlled, interoperable
mechanism for declaring and transporting additional information without modifying the core
structure:

- Domain-specific metadata relevant only to a particular legal system
- Experimental extensions not yet part of the open specification
- Third-party annotations maintained alongside the RUML core

### Two-Layer Model

RUML follows a deliberate two-layer model:

| Layer                               | Content                                                                                                                                                                        | Purpose                                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| **RUML Core** (Chapters 1–3)        | Decision tree, operators, labels, metadata                                                                                                                                     | Structural representation of regulations and laws; stable, passive, certifiable |
| **RUML + Capabilities** (Chapter 4) | `ruml:datapoints`, `ruml:query`, `ruml:ai-query`, `ruml:actions`, `ruml:text-reference`, `ruml:tree-reference`, `ruml:tree-include`, `ruml:context` and proprietary extensions | Decision-making ability, execution logic, materials, and third-party extensions |

The RUML Core is **structurally self-contained**: a RUML file without capabilities contains all
information needed to represent the rule structure and its normative-text anchoring. Applying a
rulemap to a concrete case — supplying input data, evaluating leaf-node conditions, triggering
actions — is enabled by capabilities (Chapter 4) and the runtime environment.

### The Two Delivery Modes

Capability data can be introduced into a RUML document ecosystem in two ways:

#### Inline Mode (embedded)

The capability is declared in the `capabilities` array of the RUML file, and the extension data is
stored directly as a `capabilities` field on the affected nodes or as part of the declaration at the
root level.

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_age": {
            "name": "Alter des Antragstellers",
            "type": "integer",
            "binding": {
              "type": "input"
            }
          },
          "dp_income": {
            "name": "Jahreseinkommen",
            "type": "number",
            "binding": {
              "type": "input"
            }
          }
        }
      }
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
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
        "operator": "AND",
        "label": "Kreditwürdigkeit prüfen",
        "children": ["2", "3"]
      },
      "2": {
        "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
        "label": "Mindestalter erfüllt",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_age >= 18"
            }
          }
        ]
      },
      "3": {
        "id": "42d9431d-b7db-404f-bdf9-7ecdde505cce",
        "label": "Einkommen ausreichend",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_income >= 30000"
            }
          }
        ]
      }
    }
  }
}
```

#### Sidecar Mode (RUML-EXT)

The extension data is stored in a separate `.ruml-ext` file linked to the original RUML file via a
`$base` reference (UUID + hash).

### Fail-Fast on Unknown Capabilities

Each capability declares via `required` whether it is mandatory for correct processing:

- `required: true` — The parser **MUST** support this capability. If it does not recognize it, it
  **MUST** reject the file ([`CAP-01`](../08-validation/index.md#rule-cap-01)).
- `required: false` — The parser **MUST** accept the file and ignore this capability
  ([`CAP-02`](../08-validation/index.md#rule-cap-02)). It **SHOULD** emit a warning.

A parser **MUST NOT** silently accept a file with an unknown `required: true` capability
([`CAP-01`](../08-validation/index.md#rule-cap-01)). Silently discarding extension data would lead to seemingly correct but incomplete
processing.

### Capability Roles

Each capability has exactly one **role**, specified in the respective capability specification. The
role determines

- whether a capability can occur once or multiple times on a node,
- how the capability is evaluated, and
- how the result affects the rulemap.

The role of each official `ruml:` capability is defined in this specification.

`ruml:draft/` and reverse-domain capabilities are extension points of this specification. Their role
is defined by the parser and evaluator that implement them, not by this specification.

The root-level entry of such a capability MUST declare the role the rulemap expects in its `role`
field (see [Chapter 4.2](4-2-capabilities-field.md); [`CAP-03`](../08-validation/index.md#rule-cap-03)). The declaration makes the role
visible in the file and lets tools check it:

- A parser that implements the capability MUST reject the file if the declared role differs from the
  implemented one ([`CAP-04`](../08-validation/index.md#rule-cap-04)).
- A parser that does not implement the capability applies the role-based rules below to the declared
  role.

An official `ruml:` capability MUST NOT declare `role` ([`CAP-05`](../08-validation/index.md#rule-cap-05)).

#### `data`

- **Restrictions:** None
- **Multiplicity:** Each id of a `data` capability MUST NOT occur more than once on a node
  ([`CAP-06`](../08-validation/index.md#rule-cap-06)).
- **Examples:** `ruml:datapoints`, `ruml:text-reference`, `ruml:tree-reference`, `ruml:context`

Provides input data or materials, but does not output directly.

#### `decision`

- **Restrictions:** Capabilities with the `decision` role MUST NOT be applied to nodes with children
  ([`CAP-07`](../08-validation/index.md#rule-cap-07)).
- **Multiplicity:** IDs of a `decision` capability, MAY occur multiple times on each node
  ([`CAP-06`](../08-validation/index.md#rule-cap-06)).
- **Examples:** `ruml:query`, `ruml:ai-query`, `ruml:tree-include`

Determines the status of a leaf node. It MUST return `true`, `false`, or `undefined`. If a leaf node
contains multiple `decision` capabilities, the `decisionMode` field on the node determines how the
results are combined (see [Chapter 4.3](4-3-capabilities-node-field.md)).

#### `combiner`

- **Restrictions:** Capabilities with the `combiner` role MUST NOT be applied to a node whose
  operator is not `DELEGATED` ([`CAP-08`](../08-validation/index.md#rule-cap-08)).
- **Multiplicity:** A node with a `DELEGATED` operator and children MUST have exactly one capability
  of role `combiner` ([`OP-02`](../08-validation/index.md#rule-op-02)).
- **Examples:** `ruml:expression`

Determines the status of a parent node based on the node status of its children. It can be used in
cases where the other built-in operators are not enough. It MUST return `true`, `false`, or
`undefined`.

#### `reaction`

- **Restrictions:** None
- **Multiplicity:** IDs of a `reaction` capability, MAY occur multiple times on each node
  ([`CAP-06`](../08-validation/index.md#rule-cap-06)).
- **Examples:** `ruml:actions`

A capability has exactly one role. A provider that wants to offer the same logic as a leaf
`decision` and as a `combiner` — such as one expression language usable in both places — registers
two capability ids, one per role. The role is documented in the overview table of the capability
specification.

### Signing of Capabilities

When capabilities are provided inline in the `capabilities` array, they are **part of the file** and
are included when signing. A RUML file with inline capabilities can thus be fully certified. The
signature protects both the core structure and the extended artifacts.
