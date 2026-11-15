<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.4 Conformance

This specification defines conformance for four roles: RUML files, RUML parsers, RUML producers and
RUML evaluators.

### Conformant RUML File

A RUML file is conformant if it:

- Satisfies the structural requirements of Chapters 2 and 3.
- Satisfies the referential-integrity requirements for any declared capabilities
  ([Chapter 4](../04-capabilities/index.md)).
- Satisfies the invariants defined in this specification.

A file delivered with a sidecar (`.ruml-ext`) or evaluation result (`.ruml-result`) MUST also
conform to the corresponding format definitions in [Chapter 4.5](../04-capabilities/4-5-ruml-ext.md)
and [Chapter 5](../05-result-format/index.md).

### Conformant Parser

A parser is conformant if it:

- Reads without error every conformant RUML file whose `$specVersion` it accepts
  ([Chapter 2.3](../02-file-format-basics/2-3-versioning.md)) and whose required capabilities it
  implements.
- Performs the structural validation described in
  [Chapter 2.6](../02-file-format-basics/2-6-file-validation.md) and
  [Chapter 3.8](../03-data-model/3-8-integrity-validation.md).
- Reads the `capabilities` array first, as
  [Chapter 4.6](../04-capabilities/4-6-parser-obligations.md) requires, and implements the parser
  obligations catalogued in [Chapter 8.7](../08-validation/index.md#87-capability-rules).
- Processes the RUML Container Format according to [Chapter 7.6](../07-container/7-6-processing.md)
  when a container is presented.
- Rejects any file containing a capability declared with `required: true` that it does not implement
  ([`CAP-01`](../08-validation/index.md#rule-cap-01)).

A parser MAY additionally implement capability-specific processing for any capability it recognizes.
Capability-specific processing rules are stated in each capability specification.

### Conformant Producer

A producer is conformant if it:

- Produces only files that are conformant in the sense above.
- Sets `$specVersion` to a version the producer actually targets.
- Never emits an `undefined` operator in any status other than `draft`.
- Declares every used capability in the root `capabilities` array.

### Conformant Evaluator

An evaluator determines the result of a rulemap. An evaluator is conformant if it:

- Is a conformant parser.
- Evaluates the operators as [Chapter 3.6](../03-data-model/3-6-operators.md) defines, and modular
  nodes as [Chapter 6](../06-modular-nodes/index.md) defines.
- Evaluates every decision capability it implements as the specification of that capability defines.
- Writes a result that conforms to [Chapter 5](../05-result-format/index.md) and carries the version
  that [Chapter 2.3](../02-file-format-basics/2-3-versioning.md) requires.

### Validation Tool

A validation tool is a conformant parser that additionally checks every rule of the catalogue in
[Chapter 8](../08-validation/index.md) whose layer is `schema` or `semantic` ([`CAP-28`](../08-validation/index.md#rule-cap-28)).

### Conformance Levels

This specification does not define multiple conformance levels. A file, parser, producer or
evaluator either conforms or it does not.
