<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.1 Scope

RUML (Rulemapping Logic Format) is an open, JSON-based file format for the machine-readable
representation of decision logic over normative texts.

### What This Specification Defines

This specification defines:

- The structure of a RUML file (Chapters 2–3) — JSON layout, identifier systems, metadata fields,
  and the hierarchical node model with its operators.
- The capability extension mechanism (Chapter 4) — declaration, transport, and validation of
  optional or proprietary functionality.
- The RUML Result Format (Chapter 5) — the separate file format for evaluation results.
- The modular-nodes mechanism (Chapter 6) — node reuse across multiple positions, including
  recursive structures.
- The RUML Container Format (Chapter 7) — packaging for integrity assurance, digital signatures, and
  encryption.
- The validation requirements for conforming parsers (Chapter 8).

### What This Specification Does Not Define

This specification does not define:

- Runtime evaluation algorithms beyond what the data model requires.
- Tool behavior beyond the stated conformance rules.
- Deployment, distribution, or storage infrastructure.
- Governance models, certification procedures, or organizational processes around RUML files.
- The motivation, applicability, or value of using RUML in any specific domain or organization.

### Two-Layer Model

| Layer                               | Content                                                                                                            | Purpose                                                           |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| **RUML Core** (Chapters 2–3)        | Decision tree, operators, labels, metadata                                                                         | Structural representation of regulations                          |
| **RUML + Capabilities** (Chapter 4) | Official `ruml:` capabilities (see [Chapter 4.4](../04-capabilities/4-4-namespaces.md)) and third-party extensions | Decision-making, execution, materials, and third-party extensions |

The RUML Core is **structurally self-contained**: a RUML file without capabilities contains all
information needed to represent the rule structure and its normative-text anchoring. Applying a
rulemap to a concrete case — supplying input data, evaluating leaf-node conditions, triggering
actions — is enabled by capabilities (Chapter 4) and the runtime environment.
