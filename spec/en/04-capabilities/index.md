<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 04. Capabilities

This chapter defines the extension mechanism of RUML: the **Capabilities System**.

Capabilities enable enriching RUML files with optional or proprietary functionalities without
modifying the core specification. Parsers can safely reject unknown capabilities (if required) or
ignore them (if optional) — silent data loss or unnoticed corruption is excluded.

---

### Sections of This Chapter

| Section                                                        | Content                                                            |
| -------------------------------------------------------------- | ------------------------------------------------------------------ |
| [4.1 Concept](4-1-concept.md)                                  | Motivation, design philosophy, delivery modes                      |
| [4.2 Capability Declaration](4-2-capabilities-field.md)        | Root-level declaration, entry format, parser obligations           |
| [4.3 Capability Data at Nodes](4-3-capabilities-node-field.md) | Node-level extension data, referential integrity                   |
| ~~4.4 RUML Container Format~~                                  | Moved to [Chapter 7](../07-container/index.md)                     |
| [4.4 Namespaces](4-4-namespaces.md)                            | Capability ID conventions, prefix table, syntax rules              |
| [4.5 RUML-EXT Format](4-5-ruml-ext.md)                         | Sidecar file `.ruml-ext`, `$base` reference, hash verification     |
| [4.6 Parser Obligations](4-6-parser-obligations.md)            | Parse order and requirements for validation tools                  |
| [4.7 `ruml:datapoints`](4-7-data-points.md)                    | Typed data point definitions as capability                         |
| [4.8 `ruml:query`](4-8-ruml-query.md)                          | Data-based query expressions as capability                         |
| [4.9 `ruml:ai-query`](4-9-ruml-ai-query.md)                    | AI-powered decisions as capability                                 |
| [4.10 `ruml:actions`](4-10-ruml-actions.md)                    | Actions as capability                                              |
| [4.11 `ruml:context`](4-11-ruml-context.md)                    | Context materials as capability                                    |
| [4.12 `ruml:text-reference`](4-12-ruml-text-reference.md)      | Normative text references as capability                            |
| [4.13 `ruml:protocol`](4-13-ruml-protocol.md)                  | Evaluation protocol (audit trail) as capability                    |
| [4.14 `ruml:expression`](4-14-ruml-expression.md)              | Combination expression for the `DELEGATED` operator                |
| [4.15 `ruml:tree-reference`](4-15-ruml-tree-reference.md)      | References to nodes and subtrees of other RUML files as capability |
| [4.16 `ruml:tree-include`](4-16-ruml-tree-include.md)          | Evaluation of a node of another RUML file in place of a leaf node  |
