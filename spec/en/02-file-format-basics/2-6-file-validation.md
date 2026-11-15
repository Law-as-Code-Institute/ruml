<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.6 File Validation

The structure of a RUML file is defined by the JSON Schema
[`ruml.schema.json`](../../../schemas/ruml.schema.json)
([draft 2020-12](https://json-schema.org/draft/2020-12)).

### When Loading a RUML File, the Following MUST Be Performed:

1. **Format check**:

- `$format` MUST be "RUML" ([`FMT-03`](../08-validation/index.md#rule-fmt-03))
- `$specVersion` MUST be a supported version ([`FMT-04`](../08-validation/index.md#rule-fmt-04), [`FMT-09`](../08-validation/index.md#rule-fmt-09))

2. **Structure check**:

- All required fields MUST be present
- Data types MUST conform to the specifications in Chapter 3.2 ([`FMT-13`](../08-validation/index.md#rule-fmt-13))

3. **Hash verification** (only when using the container format):

- Hash verification is performed at container level (see [Chapter 7](../07-container/index.md))
- If a hash is present, it MUST be verified; if there is a mismatch, processing MUST be refused

**Identifier check**:

- LexIDs **MUST** be unique; a reused modular node still has exactly one `nodes` entry
  ([`FMT-12`](../08-validation/index.md#rule-fmt-12))
- UUIDs **MUST** match the pattern ([`FMT-10`](../08-validation/index.md#rule-fmt-10))
- The `nodes` object **MUST** contain an entry with key `"1"` (root node) ([`FMT-08`](../08-validation/index.md#rule-fmt-08))

### Validation of RUML-EXT Files

When loading a RUML-EXT file (`.ruml-ext`, `$format: "RUML-EXT"`), a validator MUST additionally
check:

1. **Referential integrity of `$base`**: The `$base.id` MUST match the `metadata.id` of the
   referenced base RUML file, and `$base.hash` MUST match the current hash of the base file
   ([`CAP-24`](../08-validation/index.md#rule-cap-24)).
2. **UUID existence**: Every UUID in the `nodes` object of the EXT file MUST exist in the base RUML
   file. UUIDs without corresponding nodes in the base file MUST be treated as errors
   ([`CAP-26`](../08-validation/index.md#rule-cap-26)).

See [Chapter 4.5](../04-capabilities/4-5-ruml-ext.md) for the complete RUML-EXT specification.
