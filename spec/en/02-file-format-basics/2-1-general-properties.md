<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.1 General Properties

### File Extension

- **Primary**: `.ruml`
- **Evaluation results**: `.ruml-result` (see [Section 2.2](2-2-file-structure.md))
- **Capability extensions**: `.ruml-ext` (see [Chapter 4.5](../04-capabilities/4-5-ruml-ext.md))
- **Container**: `.rumlc` (ZIP, see [Chapter 7](../07-container/index.md)) — for compression,
  signature, and encryption

### MIME Type

- **Current**: `application/x-ruml`
- **Future** (after IANA registration): `application/vnd.rulemapping.ruml+json`

### Character Encoding

- **MUST**: UTF-8 ([`FMT-01`](../08-validation/index.md#rule-fmt-01))
- Other encodings are NOT permitted

### JSON Conformity

- RUML files MUST be valid JSON according to [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)
  ([`FMT-02`](../08-validation/index.md#rule-fmt-02))
- Pretty-printing with indentation is RECOMMENDED for human readability
- Compact representation (minified) is permitted
- Canonical representation MUST follow RFC 8785 for hash computation at container level (see
  [Chapter 7](../07-container/index.md))

### File Sizes

- No inherent size limitations
- Implementations SHOULD be able to handle files up to 100 MB
- Compression is RECOMMENDED for larger files

## Conformance tests

- [2.1 General Properties](../../../tests/02-file-format-basics/2-1-general-properties.test.yaml)
