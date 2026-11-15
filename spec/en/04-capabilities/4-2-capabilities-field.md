<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.2 Capability Declaration

### Overview

The `capabilities` field is an optional list at the root level of a RUML file. It declares all
capabilities used in the file, one entry each.

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [],
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
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Anspruch auf Schadensersatz"
      }
    }
  }
}
```

### Positioning in the Root Object

The `capabilities` field MAY be present in the root object of a RUML file.

:::note[Relationship to Root Structure]
The complete root object structure is defined in
[Chapter 2.2](../02-file-format-basics/2-2-file-structure.md). The `capabilities` field extends the
optional root fields by one entry.:::

### Entry Format

Each entry names its capability in `id` (following the namespace convention in
[Chapter 4.4](4-4-namespaces.md)) and carries the following fields:

```jsonc
"capabilities": [
  {
    "id": "ruml:ai-query",
    "required": true
  },
  {
    "id": "com.example/custom-actions",
    "role": "reaction"
  }
]
```

| Field      | Type    | Required                  | Description                                                                                                                                                                                                                                    |
| ---------- | ------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`       | String  | MUST                      | The capability ID (see [Chapter 4.4](4-4-namespaces.md)). MUST NOT appear more than once in the array (see [Uniqueness](#uniqueness)) ([`CAP-09`](../08-validation/index.md#rule-cap-09), [`CAP-10`](../08-validation/index.md#rule-cap-10)).                                                                          |
| `required` | Boolean | MAY                       | If `true`: parser MUST know this capability, otherwise it MUST reject the file. If `false` or absent: ignoring is permitted. Default: `false`; `ruml:expression` MUST declare `true` ([Chapter 4.14](4-14-ruml-expression.md)) ([`CAP-11`](../08-validation/index.md#rule-cap-11)) |
| `payload`  | Object  | MAY                       | Everything capability-specific. Its structure is defined by the respective capability specification; the two conventional sub-fields are described below ([`CAP-09`](../08-validation/index.md#rule-cap-09)).                                                                      |
| `role`     | String  | MUST for non-official ids | The role the rulemap expects this capability to play: `data`, `decision`, `combiner` or `reaction` (see [Chapter 4.1](4-1-concept.md#capability-roles), which also defines the rules for declaring it) ([`CAP-03`](../08-validation/index.md#rule-cap-03)).                        |

A capability entry with no special properties consists of `id` alone.

**Conventional `payload` sub-fields:**

| Sub-field        | Type         | Description                                                                                                                                                                                             |
| ---------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `payload.data`   | Object (Map) | Root-level artifact data as a map structure (key = ID). Used by capabilities that provide named objects (e.g., DataPoints, Context, Texts). See [section "The `data` field"](#the-data-field) below.    |
| `payload.config` | Object       | Global configuration for this capability. Used by capabilities that require runtime parameters (e.g., `systemPrompt` for `ruml:ai-query`). See [section "The `config` field"](#the-config-field) below. |

#### The `data` Field

The optional `data` field inside an entry's `payload` transports **root-level artifact data** as a
map structure (key = ID, value = object). It is used by capabilities that provide named objects —
e.g., DataPoint definitions, context materials, or legal texts.

**Capabilities with `data` field:**

- `ruml:datapoints` — DataPoint definitions (key = DataPoint ID)
- `ruml:context` — Context objects (key = context ID)
- `ruml:text-reference` — Legal texts (key = text ID)

**Rules:**

1. The `data` field MUST be a map structure (object with named keys) ([`CAP-12`](../08-validation/index.md#rule-cap-12)).
2. A parser that does not implement the capability and finds `required: false` MUST ignore the
   `data` field ([`CAP-02`](../08-validation/index.md#rule-cap-02)).
3. A parser that knows the capability MUST validate the `data` field according to the capability
   specification ([`CAP-13`](../08-validation/index.md#rule-cap-13)).

```jsonc
"capabilities": [
  {
    "id": "ruml:context",
    "payload": {
      "data": {
        "ctx_guidance": {
          "title": "Leitfaden zur Prüfung",
          "category": "administrativeGuidance",
          "type": "url",
          "url": "https://example.com/leitfaden",
          "timestamp": "2024-01-01T00:00:00Z"
        }
      }
    }
  },
  {
    "id": "ruml:datapoints",
    "payload": {
      "data": {
        "dp_annual_income": {
          "name": "Jahreseinkommen",
          "type": "currency",
          "unit": "EUR",
          "binding": {
            "type": "input"
          }
        }
      }
    }
  }
]
```

#### The `config` Field

The optional `config` field inside an entry's `payload` transports **global configuration** that
applies to all executions of this capability within the file. Unlike `data`, it does not contain
named artifacts but runtime parameters.

**Rules:**

1. The structure of `config` is defined by the respective capability specification.
2. A parser that does not implement the capability and finds `required: false` MUST ignore the
   `config` field ([`CAP-02`](../08-validation/index.md#rule-cap-02)).
3. A parser that knows the capability MUST validate the `config` field according to the capability
   specification ([`CAP-13`](../08-validation/index.md#rule-cap-13)).
4. A `payload` MAY contain `data`, `config`, or both — but usage is determined by the capability
   specification ([`CAP-12`](../08-validation/index.md#rule-cap-12)).

### Parser Behavior for `required: true`

If a capability has `required: true` and the parser does not implement it ([`CAP-01`](../08-validation/index.md#rule-cap-01)):

1. The parser MUST emit an error naming the unknown capability ID.
2. The parser MUST NOT partially process the file while silently discarding the unknown
   `capabilities` data under any circumstances.

```
Error: Unknown required capability 'com.example/custom-actions'.
       This file cannot be correctly processed without support for this capability.
```

### Parser Behavior for `required: false`

If a capability has `required: false` or no `required` and the parser does not implement it
([`CAP-02`](../08-validation/index.md#rule-cap-02)):

1. The parser MUST NOT abort processing because of this capability.
2. The parser SHOULD emit a warning naming the unknown capability ID.
3. The parser MUST ignore the corresponding `capabilities` fields on nodes.

A `ruml:` id that this specification version does not define is not covered by [`CAP-01`](../08-validation/index.md#rule-cap-01) and
[`CAP-02`](../08-validation/index.md#rule-cap-02): a parser rejects a file that contains it, whatever the value of `required`
([Chapter 4.4](4-4-namespaces.md)).

### Uniqueness

Each `id` MUST NOT appear more than once in the `capabilities` array. A parser MUST treat a
duplicate `id` as a validation error ([`CAP-10`](../08-validation/index.md#rule-cap-10)). The schema enforces this only for the built-in
`ruml:` capabilities; for `ruml:draft/` and third-party ids the check is a parser obligation,
because the schema cannot enforce uniqueness over an open id space.

The rule applies to the root-level array. Whether a node may carry the same id more than once
depends on the capability's role (see
[Chapter 4.3](4-3-capabilities-node-field.md#repeated-capability-ids)).

### Absence of the Field

If `capabilities` is absent from the root object or is an empty array:

- The file uses no capabilities.
- The `capabilities` field MUST be absent on all nodes. If a node nevertheless contains a
  `capabilities` field, the parser MUST treat this as a validation error ([`CAP-14`](../08-validation/index.md#rule-cap-14)).

:::warning[No Implicit Capabilities]
A node MUST NOT populate the `capabilities` field without the corresponding capability being
declared in the root object — regardless of whether the parser knows the capability or not
([`CAP-15`](../08-validation/index.md#rule-cap-15)).:::

### Complete Example

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_damage": {
            "name": "Schadenshöhe",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            }
          },
          "dp_causality": {
            "name": "Kausalität gegeben",
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
      "id": "com.example/review-notes",
      "required": true,
      "role": "data"
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "created": "2024-06-01T00:00:00Z",
    "modified": "2024-06-01T00:00:00Z",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "operator": "AND",
        "label": "Anspruch auf Schadensersatz",
        "children": ["2", "3"],
        "capabilities": [
          {
            "id": "com.example/review-notes",
            "payload": {
              "status": "reviewed",
              "reviewer": "rechtsabteilung"
            }
          }
        ]
      },
      "2": {
        "id": "8fc54c7d-7f60-410e-9493-4f1eecfb1af8",
        "label": "Schaden entstanden",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_damage > 0"
            }
          },
          {
            "id": "com.example/review-notes",
            "payload": {
              "status": "pending"
            }
          }
        ]
      },
      "3": {
        "id": "56b5b9db-b791-4fe5-abb0-a05cb0847db6",
        "label": "Kausalität gegeben",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_causality = true"
            }
          }
        ]
      }
    }
  }
}
```

## Conformance tests

- [4.2 Capability Declaration](../../../tests/04-capabilities/4-2-capabilities-field.test.yaml)
