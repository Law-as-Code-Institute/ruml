<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.2 File Structure Overview

### Root Object Structure

Every RUML file MUST have a JSON object as its root element ([`FMT-02`](../08-validation/index.md#rule-fmt-02)):

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [/* ... */],
  "metadata": {/* ... */},
  "rulemap": {/* ... */}
}
```

### Format Identification

- The `$format` field MUST have one of the following values:
  - `"RUML"` — regular content file (this specification)
  - `"RUML-Result"` — separate evaluation result file (see
    [Chapter 5.1](../05-result-format/5-1-result-model.md))
  - `"RUML-EXT"` — capability extension overlay (sidecar file); has a different root structure
    without `metadata` and `rulemap` (see [Chapter 4.5](../04-capabilities/4-5-ruml-ext.md))
- The `$specVersion` field MUST specify the format version
  ([2.3](./2-3-versioning.md#the-specversion-field))
- These fields MUST be the first two fields in the root object ([`FMT-05`](../08-validation/index.md#rule-fmt-05))
- For `"RUML-Result"`, a `rumlReference` object MUST additionally be present (see
  [Chapter 5.1](../05-result-format/5-1-result-model.md))

### Required Fields in the Root Object

| **Field**      | **Type** | **Description**                                                                                    |
| -------------- | -------- | -------------------------------------------------------------------------------------------------- |
| `$format`      | String   | MUST be `"RUML"` ([`FMT-03`](../08-validation/index.md#rule-fmt-03))                                                                   |
| `$specVersion` | String   | MUST specify the format version ([2.3](./2-3-versioning.md#the-specversion-field)) ([`FMT-04`](../08-validation/index.md#rule-fmt-04)) |
| `metadata`     | Object   | MUST contain the metadata defined in Chapter 3.3 ([`FMT-06`](../08-validation/index.md#rule-fmt-06))                                   |
| `rulemap`      | Object   | MUST contain the rulemap structure defined in Chapter 3.4 ([`FMT-06`](../08-validation/index.md#rule-fmt-06))                          |

### Optional Fields in the Root Object

| **Field**      | **Type** | **Description**                                                                                                                                                                                                    |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `capabilities` | Array    | MAY declare the capabilities this file uses, as a list of entries; their order is not significant. Each entry carries its own data in its `payload` (see [Chapter 4](../04-capabilities/index.md)) ([`FMT-06`](../08-validation/index.md#rule-fmt-06)) |

The root object MUST NOT have fields other than these ([`FMT-07`](../08-validation/index.md#rule-fmt-07)).

### Minimal Valid File

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z",
    "status": "draft"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Root"
      }
    }
  }
}
```

**Notes:**

- The `nodes` object is the only required field in the `rulemap`
- The root node **MUST** have the key `"1"` in the `nodes` object (LexID 1) ([`FMT-08`](../08-validation/index.md#rule-fmt-08))
- Every node **MUST** have an `id` (UUID v4) ([`NODE-01`](../08-validation/index.md#rule-node-01))
- Integrity assurance (hash, signature) is provided at container level (see
  [Chapter 7](../07-container/index.md))

### RUML Result Format

The RUML Result Format is used for separate storage of evaluation results:

- **File extension**: `.ruml-result`
- **Format identification**: `$format` MUST have the value `"RUML-Result"`
- **Structure**: See [Chapter 5.1](../05-result-format/5-1-result-model.md)

The RUML Result Format enables the separation of rule structure and evaluation results. This is
particularly suitable for mass procedures, case file systems, and long-term archiving.

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "evaluation": {/* ... */}
}
```

## Conformance tests

- [2.2 File Structure Overview](../../../tests/02-file-format-basics/2-2-file-structure.test.yaml)
