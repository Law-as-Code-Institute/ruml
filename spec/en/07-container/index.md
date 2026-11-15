<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 07. RUML Container

This chapter defines the **RUML Container Format** — the packaging format for RUML files that
enables integrity assurance, digital signatures, and encryption.

| Section                                     | Content                                          |
| ------------------------------------------- | ------------------------------------------------ |
| [7.1 Overview](7-1-overview.md)             | Dual-mode concept, use cases                     |
| [7.2 Container Structure](7-2-structure.md) | ZIP layout, file types, manifest                 |
| [7.3 Hash Layer](7-3-hashing.md)            | Integrity verification, canonical representation |
| [7.4 Signature Layer](7-4-signatures.md)    | Detached signatures, format registry             |
| [7.5 Encryption Layer](7-5-encryption.md)   | File encryption, format registry                 |
| [7.6 Processing Order](7-6-processing.md)   | Hash → Signature → Encryption                    |
| [7.7 Versioning](7-7-versioning.md)         | Multiple versions in a container                 |
