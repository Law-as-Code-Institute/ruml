<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.15 ruml:tree-reference

## 4.15 Capability `ruml:tree-reference`

### Overview

| Property               | Value                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------- |
| **Capability ID**      | `ruml:tree-reference`                                                                 |
| **Scope**              | Root-Level (declaration only) + Node-Level                                            |
| **Default `required`** | `false`                                                                               |
| **Node-Level**         | `payload.represents` and `payload.refersTo` of the node's `ruml:tree-reference` entry |
| **Role**               | `data`                                                                                |

This Capability lets a node point at a **node of another RUML file** — and with it at the subtree
below that node. The typical case is a decision rulemap whose rules rest on a law that is itself
available as a rulemap: the node for "articles of association notarised" points at the law's node
for § 2 (1) GmbHG instead of at the text of § 2 (1).

A node _represents_ at most one node of another file and _refers to_ any number of them. Neither is
evaluated: the referenced subtree does not influence the status of the node. To evaluate a
referenced subtree in place of a leaf, a node uses [`ruml:tree-include`](4-16-ruml-tree-include.md).

The referenced node brings its text with it: the law's nodes have their own
[`ruml:text-reference`](4-12-ruml-text-reference.md) anchors into the law's text, so following a
tree reference leads to the provision **and** to its wording. The text is anchored in exactly one
place — the law's file.

**Distinction:**

- [`ruml:text-reference`](4-12-ruml-text-reference.md) anchors **text elements** of the same RUML
  file; `ruml:tree-reference` points at **nodes** of other RUML files.
- [Modular nodes](../06-modular-nodes/index.md) reuse a subtree **within the same file**; a tree
  reference points into **another** file.

### Root-Level Declaration

```jsonc
"capabilities": [
  {
    "id": "ruml:tree-reference"
  }
]
```

The root-level entry MUST NOT have a payload ([`TREE-01`](../08-validation/index.md#rule-tree-01)). As for every capability, a file whose
nodes have `ruml:tree-reference` entries MUST declare it at the root (see
[Chapter 4.3](4-3-capabilities-node-field.md)) ([`CAP-15`](../08-validation/index.md#rule-cap-15)).

### Node-Level: References

```jsonc
{
  "id": "ruml:tree-reference",
  "payload": {
    "represents": {
      "uri": "https://rulemapping.org/rulemapping/gmbhg:2025-01-01#node/6e51c5a6-f7ff-43e1-b211-c70bd69937d7"
    },
    "refersTo": [
      {
        "uri": "https://rulemapping.org/rulemapping/gmbhg:2025-01-01#node/7791005b-3d30-455b-a538-6d96f04680d9"
      }
    ]
  }
}
```

| **Field**    | **Type**      | **Required** | **Description**                                                                                                                                  |
| ------------ | ------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `represents` | Object        | **MAY**      | The node of another RUML file this node stands for.                                                                                              |
| `refersTo`   | Array[Object] | **MAY**      | [Node anchors](#node-anchors) to nodes of other RUML files this node refers to. **MUST** contain at least one entry if present ([`TREE-01`](../08-validation/index.md#rule-tree-01)). |

**Validation rules:**

- The payload **MUST** contain `represents`, `refersTo` or both, and **MUST NOT** contain other
  fields; `represents` and every `refersTo` entry **MUST** have exactly `uri` ([`TREE-01`](../08-validation/index.md#rule-tree-01)).
- Every `uri` **MUST** be a node anchor ([`TREE-02`](../08-validation/index.md#rule-tree-02)). A same-document reference (`#node/…`) is
  not a node anchor — reuse within one file is what [modular nodes](../06-modular-nodes/index.md)
  are for.
- The same `uri` **MUST NOT** appear twice in `refersTo` ([`TREE-03`](../08-validation/index.md#rule-tree-03)).
- The target node **MUST** exist in the referenced version of the file ([`TREE-04`](../08-validation/index.md#rule-tree-04)).

Tree references **MAY** form cycles across files; they are not evaluated ([`TREE-05`](../08-validation/index.md#rule-tree-05)).

### Node Anchors

A node anchor consists of the URI of **one specific version** of a RUML file, followed by a fragment
that names a node inside it:

```
node-anchor      = ruml-version-uri "#node/" uuid
ruml-version-uri = <absolute URI of an immutable RUML version: a published tag or a content digest>
```

- **Version:** the RUML URI **MUST** identify one immutable version — a published version tag
  (`…/gmbhg:2025-01-01`) or a content digest (`…/gmbhg@sha3-256:…`). An anchor without a version
  **MUST NOT** appear in an exported or exchanged RUML file ([`TREE-06`](../08-validation/index.md#rule-tree-06); see
  [Working Anchors](#working-anchors)).
- **Node:** `node/<uuid>` addresses a node by its `id` and, with it, the subtree below it.
- **One version per file:** all node anchors of one RUML file that point into the same other RUML
  file **MUST** use the same version of it ([`TREE-06`](../08-validation/index.md#rule-tree-06)). Moving to a new version of the law
  rewrites the version in the anchors; because node ids stay (see
  [Stable Node Identity](#stable-node-identity)), the fragments stay the same.

The catalog at `rulemapping.org` provides such URIs (`https://rulemapping.org/<org>/<name>:<tag>`);
any other URI that identifies an immutable RUML version is equally valid.

[`ruml:tree-include`](4-16-ruml-tree-include.md) uses the same node anchors.

#### Working Anchors

While RUML files are being written, they often link to each other before any of them is published. A
tool **MAY** therefore hold **working anchors**, which name the target file by its `metadata.id`
without a version and resolve to its current state:

```
working-anchor = "urn:uuid:" metadata-id "#node/" uuid
```

`urn:uuid:5b0e7c8d-2f41-4a9e-8c3b-1d6f0e2a7b95#node/6e51c5a6-f7ff-43e1-b211-c70bd69937d7`

Working anchors exist only in a tool's working state. When a RUML file is exported or exchanged, the
tool **MUST** replace every working anchor with a node anchor to a published version of its target;
if a target has no published version, the export **MUST** fail. A working anchor stays valid while
the target file is edited, as long as the target node keeps its `id`.

### Resolution and Display

A tool resolves a node anchor by loading the referenced version of the file (from a
[bundled file](#bundling-for-export) first) and selecting the node whose `id` equals the fragment's
`<id>`. That node and its subtree are the referenced content.

- **Texts:** the referenced nodes keep their own `ruml:text-reference` anchors, which resolve within
  the referenced file. A tool **SHOULD** show the texts of the referenced subtree together with it;
  the referencing node needs no text anchors of its own for them. It **MAY** have its own
  `ruml:text-reference` anchors in addition ([`TREE-07`](../08-validation/index.md#rule-tree-07)).
- **Display:** a tool **MAY** show the referenced subtree read-only at the referencing node. The
  referenced subtree is never copied into the referencing file.

### Bundling for Export

A RUML file whose node anchors point into other RUML files can be exported as a container
([Chapter 7](../07-container/index.md)) that also holds those files, each with its version URI in
the manifest entry's `uri` field
([Bundled RUML Files](../07-container/7-2-structure.md#bundled-ruml-files)). A parser **MUST**
resolve a node anchor against the bundled RUML file whose manifest `uri` equals the anchor's RUML
URI before fetching it from elsewhere. Nothing is copied into the referencing file; the container's
integrity and signature layers cover the bundled files like any other file.

### Stable Node Identity

Node anchors name node `id` values, so they survive a new version of the referenced file only if its
nodes keep their ids.

- A rulemap that other files may reference **SHOULD** keep a node's `id` unchanged across versions
  as long as the node stands for the same thing.
- A rulemap that represents a law **SHOULD** use, as the `id` of a node that anchors an element of
  its own text, that element's [`GUID`](4-12-ruml-text-reference.md#element-identity-guid) —
  provided it is a lowercase UUID v4 and unique among the file's node ids. Node identity then
  follows text identity, which survives renumbering.

**Behavior for modular nodes:** a tree reference on a modular node (`modular: true`) applies to
**all instantiations**, regardless of where the node appears in the rule tree.

## Conformance tests

- [4.15 ruml:tree-reference](../../../tests/04-capabilities/4-15-ruml-tree-reference.test.yaml)
