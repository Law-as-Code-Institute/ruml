<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.3 Terminology

This section defines the terms used in this specification. Each term is summarized here; the
normative definition is in the chapter cited.

### Roles

| Term                     | Definition                                               | Defined in                |
| ------------------------ | -------------------------------------------------------- | ------------------------- |
| **Parser**               | Software that reads a RUML file.                         | [1.4](1-4-conformance.md) |
| **Producer**             | Software that writes a RUML file.                        | [1.4](1-4-conformance.md) |
| **Evaluator**            | Software that determines the result of a rulemap.        | [1.4](1-4-conformance.md) |
| **Validation tool**      | A parser that checks every `schema` and `semantic` rule. | [1.4](1-4-conformance.md) |
| **Tool, implementation** | Software in any of these roles.                          | [1.4](1-4-conformance.md) |

### Identifiers

| Term      | Definition                                                                            | Defined in                                                                                  |
| --------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **LexID** | Identifier of a node within a RUML file: a positive integer encoded as a string.      | [2.5](../02-file-format-basics/2-5-identifier-system.md#lexid-lexical-identifier)           |
| **UUID**  | Globally unique identifier (UUID v4) of a RUML file (`metadata.id`) and of each node. | [2.5](../02-file-format-basics/2-5-identifier-system.md#uuid-universally-unique-identifier) |

### Structural Elements

| Term             | Definition                        | Defined in                                                                   |
| ---------------- | --------------------------------- | ---------------------------------------------------------------------------- |
| **Node**         | Element of the RUML hierarchy.    | [3.5](../03-data-model/3-5-node-object.md)                                   |
| **Root Node**    | The topmost node, with LexID `1`. | [3.5.1](../03-data-model/3-5-node-object.md#351-node-types-by-role)          |
| **Parent Node**  | Node with `children`.             | [3.5.1](../03-data-model/3-5-node-object.md#351-node-types-by-role)          |
| **Leaf Node**    | Node without `children`.          | [3.5.1](../03-data-model/3-5-node-object.md#351-node-types-by-role)          |
| **Modular Node** | A reusable Node                   | [6.2](../06-modular-nodes/6-2-implementation.md#definition-of-modular-nodes) |

### Normative Text Anchoring

| Term             | Definition                                                                                                                          | Defined in                                                                |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Anchor**       | Link from a node to a text of the same RUML file, or one of its elements: the norm the node `represents`, or a text it `refers-to`. | [4.12](../04-capabilities/4-12-ruml-text-reference.md#node-level-anchors) |
| **documentType** | Kind of text a RUML file encodes, such as `"law"` or `"regulation"`.                                                                | [3.3.6](../03-data-model/3-3-metadata-object.md#336-documenttype-values)  |

### Operators

| Term                                 | Definition                                                               | Defined in                                                            |
| ------------------------------------ | ------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **AND**                              | Conjunction - all children MUST be `true`.                               | [3.6.1](../03-data-model/3-6-operators.md#361-and-and-not_and)        |
| **OR**                               | Disjunction - at least one child MUST be `true`.                         | [3.6.2](../03-data-model/3-6-operators.md#362-or-and-not_or)          |
| **XOR**                              | Disjunction over children constructed so that at most one can be `true`. | [3.6.3](../03-data-model/3-6-operators.md#363-xor-and-not_xor)        |
| **NOT_AND**, **NOT_OR**, **NOT_XOR** | Negations of the corresponding operators.                                |                                                                       |
| **DELEGATED**                        | Combination defined by a capability carried in the node.                 | [3.6.4](../03-data-model/3-6-operators.md#364-the-delegated-operator) |
| **undefined**                        | Placeholder operator; permitted only in `draft`.                         | [3.6.5](../03-data-model/3-6-operators.md#365-the-undefined-operator) |

### Capabilities

| Term                     | Definition                                                                                                              | Defined in                                                |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| **Capability**           | Declared extension that adds functionality without changing the core structure.                                         | [4.1](../04-capabilities/4-1-concept.md)                  |
| **Capability role**      | Function that a capability fulfills in a rulemap, such as `decision` or `data`.                                         | [4.1](../04-capabilities/4-1-concept.md#capability-roles) |
| **Capability namespace** | Id prefix that determines ownership: `ruml:` (reserved), `ruml:draft/` (experimental), or reverse-domain (third party). | [4.4](../04-capabilities/4-4-namespaces.md#prefix-table)  |

### Status

| Term                | Definition                                                                          | Defined in                                                         |
| ------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Document status** | Validity state of a RUML file, such as `draft` or `inForce`.                        | [3.3.3](../03-data-model/3-3-metadata-object.md#333-status-values) |
| **Node status**     | Evaluation state of a node, such as `true` or `false`; not stored in the RUML file. | [5.0](../05-result-format/5-0-status-types.md)                     |

### File Formats and Integrity

| Term                 | Definition                                                      | Defined in                                                                  |
| -------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **RUML file**        | Primary content file (`.ruml`).                                 | [2.2](../02-file-format-basics/2-2-file-structure.md#format-identification) |
| **RUML-EXT**         | Sidecar file (`.ruml-ext`) carrying capability data separately. | [4.5](../04-capabilities/4-5-ruml-ext.md)                                   |
| **RUML Result file** | File (`.ruml-result`) holding evaluation results.               | [5](../05-result-format/index.md)                                           |
| **Container**        | ZIP package providing integrity, signatures, and encryption.    | [7](../07-container/index.md)                                               |
| **Hash**             | Integrity check value of the form `{algorithm}:{value}`.        | [7.3](../07-container/7-3-hashing.md)                                       |
