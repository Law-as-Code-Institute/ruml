<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.16 ruml:tree-include

## 4.16 Capability `ruml:tree-include`

### Overview

| Property               | Value                                                 |
| ---------------------- | ----------------------------------------------------- |
| **Capability ID**      | `ruml:tree-include`                                   |
| **Scope**              | Root-Level (declaration only) + Node-Level            |
| **Default `required`** | `false`                                               |
| **Node-Level**         | `payload.uri` of the node's `ruml:tree-include` entry |
| **Role**               | `decision`                                            |

This Capability makes a leaf node a **placeholder** for the subtree of a node of another RUML file:
the referenced subtree is evaluated in place of the leaf, and its status becomes the status of the
leaf.

It complements [`ruml:tree-reference`](4-15-ruml-tree-reference.md), which only points at nodes of
other files. Both use the same [node anchors](4-15-ruml-tree-reference.md#node-anchors); they are
two capabilities because a capability has exactly one role (see
[Chapter 4.1](4-1-concept.md#capability-roles)).

**Why "include":** the name describes the relation from the including node's view — the referenced
subtree is part of this rulemap at exactly this position without being copied, like Akoma Ntoso
`componentRef`, XInclude or DITA `conref`.

**Distinction from modular nodes:** [modular nodes](../06-modular-nodes/index.md) reuse a subtree
**within the same file**. `ruml:tree-include` evaluates the referenced subtree like an instance of a
modular node whose definition lives in **another** file.

### Root-Level Declaration

```jsonc
"capabilities": [
  {
    "id": "ruml:tree-include"
  }
]
```

The root-level entry MUST NOT have a payload ([`TREE-01`](../08-validation/index.md#rule-tree-01)).

### Node-Level: The Included Node

```jsonc
{
  "id": "ruml:tree-include",
  "payload": {
    "uri": "https://rulemapping.org/rulemapping/gmbhg:2025-01-01#node/6e51c5a6-f7ff-43e1-b211-c70bd69937d7"
  }
}
```

| **Field** | **Type** | **Required** | **Description**                                                                                                 |
| --------- | -------- | ------------ | --------------------------------------------------------------------------------------------------------------- |
| `uri`     | String   | **MUST**     | A [node anchor](4-15-ruml-tree-reference.md#node-anchors) to the included node: `<ruml-version-uri>#node/<id>`. |

**Validation rules:**

- The payload **MUST** contain `uri` and **MUST NOT** contain other fields ([`TREE-01`](../08-validation/index.md#rule-tree-01)), and
  `uri` **MUST** be a node anchor ([`TREE-02`](../08-validation/index.md#rule-tree-02)).
- A node with `ruml:tree-include` **MUST NOT** have children ([`CAP-07`](../08-validation/index.md#rule-cap-07)).
- A node with `ruml:tree-include` **MUST NOT** have `represents` in its `ruml:tree-reference`
  ([`TREE-08`](../08-validation/index.md#rule-tree-08)): a node that includes another node already stands for it.
- The node anchor rules of [Chapter 4.15](4-15-ruml-tree-reference.md#node-anchors) apply: one
  immutable version, the same version for all node anchors into one file ([`TREE-06`](../08-validation/index.md#rule-tree-06)), and the
  target node exists in that version ([`TREE-04`](../08-validation/index.md#rule-tree-04)).
- Inclusions **MUST NOT** form a cycle across files ([`TREE-09`](../08-validation/index.md#rule-tree-09)): file A includes a node of B,
  and B includes a node of A — directly or through further files.

### Including Several Subtrees

To include several subtrees, a rulemap uses several placeholder nodes. The tree then defines
everything the combination needs: the order is the child order, the combination is the parent's
operator, a negation is a parent node with a `NOT_…` operator (see
[Chapter 3.6](../03-data-model/3-6-operators.md)), and every include has its own label, explanation,
text references and result.

```
"Company validly founded"                       AND
├── "Articles of association notarised"        include → gmbhg:2025-01-01#node/6e51…
├── "Share capital at least EUR 25,000"        include → gmbhg:2025-01-01#node/7791…
└── "Entered in the commercial register"       (own logic)
```

As with modular nodes, reuse is visible as a node in the tree, not as hidden extra children.

### Evaluation

A tool resolves the included node (see
[Resolution and Display](4-15-ruml-tree-reference.md#resolution-and-display)), evaluates it with its
subtree under the rules of the referenced file, and uses the resulting status as the result of the
capability. If the leaf has further `decision` capabilities, `decisionMode` combines their results
(see [Chapter 4.3](4-3-capabilities-node-field.md)).

**Not defined in this version:** how the included subtree obtains its inputs — the data points and
questions its leaves evaluate — is not defined in this version of the specification. Under
consideration are inputs shared with the including file by data point id, inputs namespaced per
referenced file, and an explicit binding per include.

A tool that cannot evaluate an inclusion — because it does not support `ruml:tree-include`, or
because the referenced version or node cannot be loaded — **MUST** use `undefined` as its result
(see [Chapter 5.0](../05-result-format/5-0-status-types.md)); it **MUST NOT** treat the node as
fulfilled.

**Behavior for modular nodes:** an inclusion on a modular node (`modular: true`) applies to **all
instantiations**.

## Conformance tests

- [4.16 ruml:tree-include](../../../tests/04-capabilities/4-16-ruml-tree-include.test.yaml)
