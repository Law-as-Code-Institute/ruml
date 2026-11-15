<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 03. Data Model

This chapter is the structural core of the specification. It defines the flat node map that holds a
rulemap, the fields every node carries, and the operators that combine child results. Everything a
capability later adds attaches to the objects defined here.

- [3.1 Architecture Principles](3-1-architecture-principles.md) — Flat map, key is the identifier,
  no derived state in the file
- [3.2 Data Types and Formats](3-2-data-types-and-formats.md) — Timestamps, hashes, UUIDs, and the
  map structures
- [3.3 Metadata Object](3-3-metadata-object.md) — Document identity, status, validity, and
  authorship
- [3.4 Rulemap Object](3-4-rulemap-object.md) — The `nodes` map and its root entry
- [3.5 Node Object](3-5-node-object.md) — Required and optional node fields, and the parent/leaf
  distinction
- [3.6 Operators](3-6-operators.md) — `AND`, `OR`, `XOR` and their negated forms
- [3.7 Structure Example](3-7-structure-example.md) — A complete rulemap, annotated
- [3.8 Integrity Validation](3-8-integrity-validation.md) — Structural checks across the node map
