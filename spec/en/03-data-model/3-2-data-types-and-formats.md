<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.2 Data Types and Formats

### 3.2.1 LexID

See [Chapter 2.5](../02-file-format-basics/2-5-identifier-system.md#lexid-lexical-identifier) for
the complete definition.

### 3.2.2 UUID

See
[Chapter 2.5](../02-file-format-basics/2-5-identifier-system.md#uuid-universally-unique-identifier)
for the complete definition.

### 3.2.3 Additional Data Types

| **Type**   | **Format**  | **Example**                     | **Validation**                                                                                                                                                       |
| ---------- | ----------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `String`   | UTF-8       | `"Bundesministerium"`           | MUST be UTF-8 encoded ([`FMT-01`](../08-validation/index.md#rule-fmt-01)).                                                                                                                               |
| `Number`   | JSON Number | `42`, `3.14`, `1000.50`         | MUST be a JSON-conformant number (IEEE 754 double) ([`FMT-13`](../08-validation/index.md#rule-fmt-13)). MAY represent integer or decimal values.                                                         |
| `Boolean`  | Boolean     | `true`, `false`                 | MUST be a JSON Boolean (`true` or `false`) ([`FMT-13`](../08-validation/index.md#rule-fmt-13)).                                                                                                          |
| `DateTime` | RFC 3339    | `"2024-01-01T12:00:00+01:00"`   | MUST be a `date-time` as defined in [RFC 3339, section 5.6](https://www.rfc-editor.org/rfc/rfc3339#section-5.6), the JSON Schema format `date-time` ([`FMT-13`](../08-validation/index.md#rule-fmt-13)). |
| `Enum`     | String      | `"draft"`, `"inForce"`, `"AND"` | MUST be a value defined in the specification ([`FMT-13`](../08-validation/index.md#rule-fmt-13)). Permitted values are documented in the respective field.                                               |
| `Object`   | JSON Object | `{"key": "value"}`              | MUST be a JSON object ([`FMT-13`](../08-validation/index.md#rule-fmt-13)).                                                                                                                               |
| `Array`    | JSON Array  | `[1, 2, 3]`                     | MUST be a valid JSON Array ([`FMT-13`](../08-validation/index.md#rule-fmt-13)).                                                                                                                          |

### 3.2.4 Hash Format

Hashing and integrity assurance of the RUML file are a responsibility of the RUML container (see
[Chapter 7](../07-container/index.md)). The RUML JSON file contains no hash of itself. The hashes it
may contain belong to other content: `derivedFrom.originalHash` ([3.3](3-3-metadata-object.md)), the
`hash` of a context entry ([4.11](../04-capabilities/4-11-ruml-context.md)) and the `digest` of a
text entry ([4.12](../04-capabilities/4-12-ruml-text-reference.md)).

**Hash format (reference for container level):**

Hashes in RUML use the extended format:

```
"{algorithm}:{value}"
```

**Example:**

```
"sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
```

**Supported algorithms:**

| **Algorithm** | **Usage**                                         | **Format**                |
| ------------- | ------------------------------------------------- | ------------------------- |
| `sha3-256`    | MUST be used for all new containers               | 64 hexadecimal characters |
| `sha256`      | MAY be used for backward compatibility            | 64 hexadecimal characters |
| `blake3`      | MAY be used for performance-critical applications | 64 hexadecimal characters |

**Canonical JSON representation:**

For consistent hash computation at container level, the RUML file MUST be canonicalized.
Canonicalization MUST implement RFC 8785 (JSON Canonicalization Scheme). Details on the computation
procedure see [Chapter 7](../07-container/index.md).

**Authenticity and legal binding:**

Hashes alone guarantee **no authenticity** and **no legal binding**. These guarantees are achieved
through signatures at container level (see [Chapter 7](../07-container/index.md)).

### 3.2.5 Integrity Assurance

Integrity assurance — including hashing, signatures, and timestamps — is handled entirely at
container level (see [Chapter 7](../07-container/index.md)). Inline fields such as `metadata.hash`
or `metadata.integrity` are **no longer part of the RUML data model**.

### 3.2.6 RUML File Structure (Top-Level)

The top-level structure of a RUML file is defined in
[Chapter 2.2](../02-file-format-basics/2-2-file-structure.md).

**Design principle: Key = identifier for map structures**

RUML consistently uses the principle that for map structures (JSON objects), the **key itself serves
as the identifier**. An entry therefore **MUST NOT** repeat its own key as a field: a node carries
no `lexId` field, and text, datapoint, and context objects carry no id field of their own
([`FMT-14`](../08-validation/index.md#rule-fmt-14), [`NODE-03`](../08-validation/index.md#rule-node-03)).

Other identifiers on the entry are unaffected. A node is keyed by its LexID but still carries a
REQUIRED `id` holding its UUID (see
[Chapter 2.5](../02-file-format-basics/2-5-identifier-system.md)) — a distinct identifier, not a
copy of the key ([`NODE-01`](../08-validation/index.md#rule-node-01)).

This principle applies to all map structures in RUML:

`nodes` – Key is the LexID (e.g., `"1"`, `"42"`)

`capabilities[{id: "ruml:text-reference"}].data` – Key is the text ID (e.g., `"text_bgb_823"`,
`"text_sgb_12_21"`)

`capabilities[].data` – Key is the artifact ID (e.g., `"ctx_bgh_2024"`, `"dp_monthly_income"`) for
the data of `ruml:datapoints`, `ruml:context`, etc.

**Benefits:** No redundancy, guaranteed uniqueness through JSON key semantics, simpler validation.

## Conformance tests

- [3.2 Data Types and Formats](../../../tests/03-data-model/3-2-data-types-and-formats.test.yaml)
