<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# RUML – Rulemapping Logic Format

RUML is an open, JSON-based file format for the machine-executable representation of legal decision
logic. This specification defines the format: its structure, its extension mechanism, and the
requirements an implementation must satisfy to be conformant.

RUML stands for Rulemapping Logic. The format does not mark up legislative text; it holds the
decision logic as an artifact of its own and references the wording.

## Status of This Document

**Version 1.0.0 / November 15, 2026**

Published by Law as Code Institut GmbH. Rulemapping Group GmbH holds the rights to this
specification.

## License

This specification is licensed under
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
It may be copied, redistributed, translated and adapted, including for commercial purposes, provided
the rights holder is credited and adaptations are distributed under the same license.

Attribution:

> RUML – Rulemapping Logic Format, version 1.0.0, © Rulemapping Group GmbH, published
> by Law as Code Institut GmbH, licensed under CC BY-SA 4.0.

The license covers the document, not the format. Building a runtime environment, producing,
processing or exchanging RUML files requires no license and no permission. The ShareAlike condition
applies to adaptations of this text. It does not extend to software that implements the format, nor
to rulemaps created in it; rulemaps remain with their authors.

The JSON Schemas, the conformance tests and the examples are licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Authoritative Version

The English version is authoritative. The German version is a translation. Where the two differ, the
English wording governs.

## How to Cite

> Rulemapping Group GmbH: RUML – Rulemapping Logic Format. Version 1.0.0. Law as Code
> Institut GmbH, November 15, 2026.
>
> https://ruml.org/1.0.0/

A reference to a single provision names the chapter: _RUML 1.0.0, Chapter 4.6 (Parser
Obligations)._

## Versions and Addresses

|                |                                                      |
| -------------- | ---------------------------------------------------- |
| This version   | `https://ruml.org/1.0.0/` |
| Latest version | `https://ruml.org/`                                  |
| Change history | [Change history](change-history.md)                  |

A published version stays available unchanged at its version address. A citation or a reference in
another document uses the version address, not the latest one.

The format carries its own versioning in the `$specVersion` field. That is a separate matter,
governed by [Chapter 2.3](02-file-format-basics/2-3-versioning.md).

## Trademark

RUML is a trademark of Rulemapping Group GmbH; an application for registration as an EU trade mark
has been filed. Referring to the format is free: statements such as “supports RUML” or
“RUML-compatible” are permitted where they are accurate. Files, software and services that do not
conform to this specification may not be labelled RUML. An adapted or derived version of this
specification may not be called RUML.

## Structure of This Specification

| Chapter                                                | Subject                                                                 |
| ------------------------------------------------------ | ----------------------------------------------------------------------- |
| [1 Introduction](01-introduction/index.md)             | Scope, notation, terminology, conformance                               |
| [2 File Format Basics](02-file-format-basics/index.md) | JSON layout, versioning, integrity, identifiers                         |
| [3 Data Model](03-data-model/index.md)                 | Metadata, rulemap, nodes, operators                                     |
| [4 Capabilities](04-capabilities/index.md)             | Extension mechanism, `ruml:` capabilities, third-party namespaces       |
| [5 Result Format](05-result-format/index.md)           | RUML-Result                                                             |
| [6 Modular Nodes](06-modular-nodes/index.md)           | Reuse, recursion, nesting                                               |
| [7 Container](07-container/index.md)                   | Packaging, hashing, signatures, encryption                              |
| [8 Validation](08-validation/index.md)                 | Rule catalogue for conformant parsers                                   |
| [Appendix](appendix/index.md)                          | A. Spec Test Suite: conformance suite and runner contract (informative) |

**Where to start.** A first reader begins with [Chapter 1.1](01-introduction/1-1-introduction.md)
(Scope) and [1.4](01-introduction/1-4-conformance.md) (Conformance). An implementer building a
runtime environment reads Chapters [2](02-file-format-basics/index.md), [3](03-data-model/index.md),
[4](04-capabilities/index.md), [5](05-result-format/index.md), [6](06-modular-nodes/index.md),
[7](07-container/index.md) and [8](08-validation/index.md) together and checks the implementation
against the conformance suite in [Appendix A](appendix/A-spec-tests/index.md). How RUML relates to Akoma
Ntoso, DMN and LegalRuleML is set out in
[Chapter 1.5](01-introduction/1-5-relationship-to-other-standards.md).

## Feedback

Errors, ambiguities and contradictions in this specification can be reported through
[law-as-code.org/contact](https://law-as-code.org/contact) or as an issue on
[GitHub](https://github.com/Law-as-Code-Institute/ruml/issues). Proposals for changes to the
specification text are welcome the same way; pull requests are not accepted at present.
