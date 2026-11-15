<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 02. File Format Basics

This chapter defines what makes a file a RUML file: its encoding, the fields every root object
carries, and the rules for versioning, integrity, and identifiers. The data model those fields
describe follows in [Chapter 3](../03-data-model/index.md).

- [2.1 General Properties](2-1-general-properties.md) — Encoding, JSON well-formedness, file
  extensions
- [2.2 File Structure Overview](2-2-file-structure.md) — The root object: `$format`, `$specVersion`,
  `metadata`, `rulemap`
- [2.3 Versioning](2-3-versioning.md) — Spec version and document version, and how they differ
- [2.4 Integrity Assurance](2-4-integrity.md) — Hash algorithms and canonical representation
- [2.5 Identifier System](2-5-identifier-system.md) — LexIDs as map keys, UUIDs as global
  identifiers
- [2.6 File Validation](2-6-file-validation.md) — The checks a validator performs, and in what order
