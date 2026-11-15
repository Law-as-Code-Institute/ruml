<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 3.5 Node Object

## 3.5 Node Object (Core Architecture)

### 3.5.1 Node Types by Role

In the flat map architecture, all nodes are stored directly in the `nodes` object. Node types are
derived from their **logical role** in the hierarchy, defined by `lexId` and `children` references:

| **Type** | **Logical Role** | **Description**                 | **Identification**                                |
| -------- | ---------------- | ------------------------------- | ------------------------------------------------- |
| root     | Root             | The topmost node of the rulemap | Has the key `"1"` in the `nodes` object (LexID 1) |
| parent   | Branch           | Node with its own children      | Has a non-empty `children` array                  |
| leaf     | Leaf             | Terminal node without children  | Has no `children` array                           |

The following rules apply to the node types:

- The root node **MUST** exist ([`FMT-08`](../08-validation/index.md#rule-fmt-08)).
- The root node **MUST NOT** appear in the `children` array of any node ([`NODE-05`](../08-validation/index.md#rule-node-05)).
- A `children` array **MUST NOT** be empty ([`NODE-06`](../08-validation/index.md#rule-node-06)).

**Important:** The type **MUST NOT** be explicitly stored, as it is derived from the structure
([`NODE-03`](../08-validation/index.md#rule-node-03)).

**Runtime status:** The evaluation status of a node (`pending`, `true`, `false`, `undefined`,
`ignored`) is computed at runtime and is NOT part of the node definition. Storage of evaluation
results occurs exclusively in a separate RUML Result file (`.ruml-result`) (see
[Chapter 5](../05-result-format/index.md)).

### 3.5.2 Required Fields of a Node

| Field   | Type     | Description                                                                                                                                                                       |
| ------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`    | `UUID`   | **MUST** be present ([`NODE-01`](../08-validation/index.md#rule-node-01)). **MUST** be unique within the file, also against `metadata.id` ([`NODE-08`](../08-validation/index.md#rule-node-08)). **MUST** conform to the format from 3.2.2 ([`FMT-10`](../08-validation/index.md#rule-fmt-10)). |
| `label` | `String` | **MUST** contain a human-readable label ([`NODE-01`](../08-validation/index.md#rule-node-01)). **MUST** have at least 1 character ([`NODE-09`](../08-validation/index.md#rule-node-09)).                                                                    |

**Note on LexID:** The LexID of a node is derived from the key in the `nodes` object (see
[3.2.1](3-2-data-types-and-formats.md)). A separate `lexId` field is NOT required and MUST NOT be
used ([`NODE-03`](../08-validation/index.md#rule-node-03)).

### 3.5.2a The `operator` Field

The `operator` field (type `Enum`) determines how a node combines the results of its children.

- A parent node **MUST** have an `operator`; it applies to ALL direct children ([`NODE-12`](../08-validation/index.md#rule-node-12)).
- A leaf node has nothing to combine. It **MUST NOT** have an `operator` unless `metadata.status` is
  `draft`; in a draft, a leaf node **MAY** have any operator, and an evaluator ignores it
  ([`NODE-07`](../08-validation/index.md#rule-node-07)).
- The value **MUST** be one of the operators defined in [3.6](3-6-operators.md) ([`OP-01`](../08-validation/index.md#rule-op-01)).

### 3.5.3 Optional Fields of a Node

A node MAY have any of the following fields; a parser MUST accept each of them, present or absent
([`NODE-07`](../08-validation/index.md#rule-node-07)).

| Field          | Type            | Description                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `children`     | `Array[String]` | **MAY** contain an ordered list of child references. Each entry **MUST** be a `LexID` reference (string, see [2.5](../02-file-format-basics/2-5-identifier-system.md)) ([`FMT-11`](../08-validation/index.md#rule-fmt-11)). Each referenced `LexID` **MUST** exist in the `nodes` object ([`NODE-10`](../08-validation/index.md#rule-node-10)). The same `LexID` **SHOULD NOT** appear more than once in one `children` array. The order is significant.                                     |
| `altText`      | `String`        | **MAY** contain an alternative/full text. **SHOULD** be used for UI display (tooltips, screen readers). If not set, `label` **SHOULD** be used.                                                                                                                                                                                                                                                                     |
| `description`  | `String`        | **MAY** contain a detailed description. MUST NOT exceed 10,000 characters ([`NODE-11`](../08-validation/index.md#rule-node-11)).                                                                                                                                                                                                                                                                                                                         |
| `capabilities` | `Array`         | **MAY** contain capability-specific data for this node, as an ordered list of `{ id, payload }` entries; each entry MUST have both fields ([`CAP-17`](../08-validation/index.md#rule-cap-17)). Every `id` MUST correspond to a capability declared in the file ([`CAP-15`](../08-validation/index.md#rule-cap-15)). Via `capabilities`, `ruml:query`, `ruml:actions`, and `ruml:ai-query` are provided, among others. See [Chapter 4.3](../04-capabilities/4-3-capabilities-node-field.md). |
| `metadata`     | `Object`        | **MAY** contain additional metadata. **SHOULD** be used for non-structural information.                                                                                                                                                                                                                                                                                                                             |
| `decisionMode` | `Enum`          | **MAY** define the combination mode for multiple decision-relevant capabilities. Only relevant for leaf nodes with more than one `decision` capability. Permitted values: `fallback`, `agreement`, `majority`. Default: `fallback`. See [Chapter 4.3](../04-capabilities/4-3-capabilities-node-field.md).                                                                                                           |
| `modular`      | `Boolean`       | Marks the node as a modular node (definition see [6.2](../06-modular-nodes/6-2-implementation.md#definition-of-modular-nodes)). A modular node **MUST** have `modular: true` ([`MOD-01`](../08-validation/index.md#rule-mod-01)); a node that is not modular **SHOULD NOT** have it.                                                                                                                                                                    |

**Important rules:**

- Restrictions for decision-relevant capabilities (`ruml:query`, `ruml:ai-query`) are defined in the
  respective capability specification (see [Chapter 4.8](../04-capabilities/4-8-ruml-query.md))
- The norm a node represents and the texts it refers to are provided via the `capabilities` entry
  with `id: "ruml:text-reference"` (anchors in `refs`, see
  [Chapter 4.12](../04-capabilities/4-12-ruml-text-reference.md))
- The `id` of every entry in a node's `capabilities` array MUST be declared in the root-level
  `capabilities` array of the same file (referential integrity, rule CAP-15 in chapter 08)
  ([`CAP-15`](../08-validation/index.md#rule-cap-15)). The complete specification is found in
  [Chapter 4.3](../04-capabilities/4-3-capabilities-node-field.md).

:::note[Capability-provided node extensions]
The following concepts are **not direct node fields**, but are provided via `capabilities`:

| Capability            | Node field                                       | Description                                                                                                            |
| --------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| `ruml:query`          | `capabilities` entry `id: "ruml:query"`          | Data-based query expression for leaf nodes — see [Chapter 4.8](../04-capabilities/4-8-ruml-query.md)                   |
| `ruml:actions`        | `capabilities` entry `id: "ruml:actions"`        | Actions for `onTrue`, `onFalse`, `onUndefined` — see [Chapter 4.10](../04-capabilities/4-10-ruml-actions.md)           |
| `ruml:ai-query`       | `capabilities` entry `id: "ruml:ai-query"`       | LLM-based decision — see [Chapter 4.9](../04-capabilities/4-9-ruml-ai-query.md)                                        |
| `ruml:text-reference` | `capabilities` entry `id: "ruml:text-reference"` | References to normative texts (laws, regulations) — see [Chapter 4.12](../04-capabilities/4-12-ruml-text-reference.md) |

:::

### 3.5.4 Node Positions (Paths)

Node positions (paths) are computed at runtime from the tree structure and are NOT part of the RUML
file. The hierarchical position of a node is derived entirely from the `children` arrays and the
`lexId` structure in the `nodes` object.

For modular nodes (see [Chapter 6](../06-modular-nodes/index.md)), the same node can be reached via
different paths in the tree. Paths are computed at runtime and used in the `results` object of the
RUML Result file (see [Chapter 5](../05-result-format/index.md)) as keys for evaluation results.

## Conformance tests

- [3.5 Node Object](../../../tests/03-data-model/3-5-node-object.test.yaml)
