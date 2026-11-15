<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 3.1 Architecture Principles

The RUML data model defines the structure for machine-readable regulations and decision logic. The
architecture is based on a hierarchical **parent-to-child relationship**, where each node
exclusively stores information about its direct children.

## 3.1 Fundamental Architecture Principles

**The RUML architecture MUST follow these fundamental principles:**

1. **Unidirectional relationships:** Nodes **MUST NOT** know any nodes other than their direct
   children. Nodes **MUST NOT** store information about their parent nodes ([`NODE-03`](../08-validation/index.md#rule-node-03)).
2. **One operator per node:** Each parent node **MUST** have exactly ONE operator type that applies
   to ALL its direct children.
3. **Ordered hierarchy:** The order of children in the children array of parent nodes **MUST** be
   significant and **MUST** be considered in execution logic ([`NODE-04`](../08-validation/index.md#rule-node-04)).
4. **LexID as primary identifier:** Nodes **MUST** be identified within the RUML via numeric LexIDs
   ([`FMT-11`](../08-validation/index.md#rule-fmt-11)).
5. **Flat map structure:** All nodes **MUST** be defined in a central `nodes` object
   ([`NODE-02`](../08-validation/index.md#rule-node-02)). Parent-child relationships **MUST** be established via LexID references in the
   `children` array, NOT through embedded objects ([`FMT-11`](../08-validation/index.md#rule-fmt-11)). This enables multiple referencing
   of the same LexID for modular nodes (see [Chapter 6](../06-modular-nodes/index.md)).
