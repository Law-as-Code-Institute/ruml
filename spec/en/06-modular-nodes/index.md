<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 06. Modular Nodes

A modular node is defined once and referenced from several places in the tree, so a subtree that
several rules depend on is maintained in one location. This chapter defines how such nodes are
declared, how they evaluate when reached by more than one path, and the limits that keep a rulemap
finite.

- [6.1 Concept](6-1-concept.md) — What a modular node is, and when to use one
- [6.2 Implementation](6-2-implementation.md) — Declaring `modular: true` and referencing it
- [6.3 Evaluation and Copy Behavior](6-3-evaluation.md) — Why results are indexed by path, not by
  LexID
- [6.4 Recursion](6-4-recursion.md) — Self-reference, the operators it requires, and termination
- [6.5 Nesting](6-5-nesting.md) — Modular nodes inside modular nodes
