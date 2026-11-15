<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.5 Identifier System

### LexID (Lexical Identifier)

Primary numeric identifier within a RUML file:

- **Format**: Positive integer, encoded as a JSON string (e.g. `"12"`)
- **Pattern**: `^[1-9][0-9]*$` ([`FMT-11`](../08-validation/index.md#rule-fmt-11))
- **Start**: MUST begin at 1 (root node) ([`FMT-08`](../08-validation/index.md#rule-fmt-08))
- **Uniqueness**: MUST be unique within the file ([`FMT-12`](../08-validation/index.md#rule-fmt-12))
- **Reuse**: A modular node (see
  [6.2](../06-modular-nodes/6-2-implementation.md#definition-of-modular-nodes)) exists once in
  `nodes`; its LexID stays unique

LexIDs are strings everywhere they appear — as `rulemap.nodes` keys and in `children`. The node map
is a JSON object, so its keys are strings by construction; using the same form for references keeps
a reference and its key directly comparable.

### UUID (Universally Unique Identifier)

Globally unique identifier for external referencing:

- **Format**: UUID v4 (randomly generated)
- **Pattern**: `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`
  ([`FMT-10`](../08-validation/index.md#rule-fmt-10))
- **Standard**: RFC 4122 Version 4
- **Entropy**: 122 bits cryptographically secure
- **Generation**: SHOULD use standard UUID library (e.g. `uuid` npm package, v4 function)

**Examples of valid UUIDs:**

```
e7c9a3f1-4b82-4d15-9a6c-3d8f2b01e794
a3f5c9e7-2d48-4b71-8f6a-1c3d0b92e475
b8d2e4f6-0a73-4c85-9b1e-5f7c2a34d098
c1e3a5f7-6b90-4d42-8c4a-7f2e3b01d563
```

## Conformance tests

- [2.5 Identifier System](../../../tests/02-file-format-basics/2-5-identifier-system.test.yaml)
