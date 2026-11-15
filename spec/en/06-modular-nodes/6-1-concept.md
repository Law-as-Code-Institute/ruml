<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.1 Concept

Modular nodes are reusable structures within a rulemap — either individual leaf nodes or nodes with
children (subtrees). A modular node exists exactly once in the `nodes` object and is reused at
several places in the rulemap. When a node is modular is defined in
[6.2](6-2-implementation.md#definition-of-modular-nodes).

**Use Cases:**

- **Reusable checks:** A verification subtree is used at multiple points in the rulemap — centrally
  defined, consistent, and maintenance-efficient
- **Standardized sub-processes:** Frequently required decision logic only needs to be defined once
- **Recursive structures:** Cycles such as offer → rejection → new offer can be traversed any number
  of times
