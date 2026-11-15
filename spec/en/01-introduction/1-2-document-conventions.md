<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.2 Document Conventions

### Requirement Levels (RFC 2119)

This specification uses the keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** as defined in
[RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) to indicate requirement levels:

| Keyword                              | Meaning                                                         |
| ------------------------------------ | --------------------------------------------------------------- |
| **MUST** / **REQUIRED** / **SHALL**  | Absolute requirement                                            |
| **MUST NOT** / **SHALL NOT**         | Absolute prohibition                                            |
| **SHOULD** / **RECOMMENDED**         | Strong recommendation; deviation requires a justified reason    |
| **SHOULD NOT** / **NOT RECOMMENDED** | Strong recommendation against; use only with a justified reason |
| **MAY** / **OPTIONAL**               | Truly optional                                                  |

The keywords are normative only when they appear in uppercase.

### Notation

| Convention       | Form                                                                             | Example            |
| ---------------- | -------------------------------------------------------------------------------- | ------------------ |
| JSON example     | Fenced code block with `json` highlighting                                       | `"lexId": "1"`     |
| Placeholder      | Angle brackets                                                                   | `<lexId>`          |
| Optional element | Marked `[optional]`                                                              | `field [optional]` |
| Repetition       | Three dots                                                                       | `..., ...`         |
| Pattern          | Regular expression (ECMA-262)                                                    | `^[1-9][0-9]*$`    |
| Field type       | Refers to types in [Chapter 3.2](../03-data-model/3-2-data-types-and-formats.md) | `UUID`, `DateTime` |

### Naming Conventions

RUML distinguishes schema-defined fields from user-defined identifiers by case style:

- **Schema-defined fields** use camel case — e.g. `lexId`, `id`, `children`, `containerPath`,
  `validFrom`, `documentType`, `decisionMode`, `expression`, `onTrue`.
- **User-defined identifiers** use snake case — e.g. DataPoint IDs (`dp_annual_income`), Context IDs
  (`ctx_court_ruling`), and Text IDs (`text_bgb_823`) ([`DP-02`](../08-validation/index.md#rule-dp-02)).
- **Implementation-defined identifiers**, such as references to actions or AI models, SHOULD use
  snake case — e.g. `document_service`, `manual_review_workflow`.

Tools SHOULD follow this convention when generating new identifiers. Capability IDs follow their own
namespace convention defined in [Chapter 4.4](../04-capabilities/4-4-namespaces.md).
