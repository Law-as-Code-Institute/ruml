<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.6 Parser Obligations

The obligations of parsers and tools that process RUML or RUML-EXT files are defined in the chapters
they concern and catalogued, with references to those chapters, in
[Chapter 8](../08-validation/index.md); the parser obligations of the capability system are in
[Chapter 8.7](../08-validation/index.md#87-capability-rules). This section adds the order in which a
parser reads a file. That order cannot be observed from outside, so it has no rule id.

The order of the capability entries of a node is defined in
[Chapter 4.3](4-3-capabilities-node-field.md#field-order); at the root, it is not significant.

### Early Reading of the `capabilities` Array

A parser MUST read and evaluate the `capabilities` array **before** processing the `rulemap` or
other structural fields of the file. This ensures fail-fast behavior for `required: true`
capabilities.

:::note[Recommended Parse Order]
1. Read and validate `$format` and `$specVersion`
2. Read the `capabilities` array and check whether each capability is known
3. On unknown `required: true` capability: abort
4. Process remaining fields
:::

### Note on Tool Implementations

:::warning[Validation Tools]
A validation tool MUST check every rule of the layers `schema` and `semantic` in
[Chapter 8](../08-validation/index.md) ([`CAP-28`](../08-validation/index.md#rule-cap-28)). A tool that only checks the core structure
and ignores the `capabilities` system is not a complete RUML validator.
:::
