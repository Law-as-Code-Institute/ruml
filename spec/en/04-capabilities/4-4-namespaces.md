<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.4 Namespaces for Capability IDs

### Purpose

Capability IDs MUST be globally unique to prevent collisions between capabilities from different
providers. A namespace mechanism based on prefixes ensures this uniqueness.

Each capability ID consists of a **prefix** and a **local name**, separated by a defined delimiter.

### Prefix Table

| Prefix              | Delimiter | Owner                   | Normativity     | Description                                                     |
| ------------------- | --------- | ----------------------- | --------------- | --------------------------------------------------------------- |
| `ruml:`             | `:`       | RUML Specification Body | Normative       | Official capabilities of the RUML specification — reserved      |
| `ruml:draft/`       | `:` + `/` | RUML Specification Body | Experimental    | Experimental capabilities; MAY change without notice            |
| `<reverse-domain>/` | `.` + `/` | Third party             | Vendor-specific | Arbitrary third parties following the reverse-domain convention |

A parser MUST verify that every capability ID conforms to one of these prefixes. It MUST treat an ID
without a recognizable prefix pattern as an error ([`CAP-21`](../08-validation/index.md#rule-cap-21)).

:::warning[Namespace Reservation]
The prefix `ruml:` is **reserved**. Third parties MUST NOT use this prefix for their own
capabilities. A parser MUST reject a file that contains a `ruml:` id that is neither defined by this
specification version nor a `ruml:draft/` id, whatever the value of `required`.
:::

### Official Capabilities (`ruml:`)

Capabilities under the `ruml:` prefix (without `draft/`) are part of the RUML specification. They
MUST be documented in an official capability registry and follow the versioning rules of the
specification (see [Chapter 2.3](../02-file-format-basics/2-3-versioning.md)).

#### Official Capability Registry

The following `ruml:` capabilities are defined in the current specification:

| Capability ID         | Scope                     | Description                                                        | Specification                               |
| --------------------- | ------------------------- | ------------------------------------------------------------------ | ------------------------------------------- |
| `ruml:datapoints`     | Root (`data`)             | DataPoints schema (data definitions) and binding hints             | [Chapter 4.7](4-7-data-points.md)           |
| `ruml:query`          | Node                      | Data-based query expression (leaf nodes)                           | [Chapter 4.8](4-8-ruml-query.md)            |
| `ruml:ai-query`       | Node                      | AI-powered decisions (LLM-based)                                   | [Chapter 4.9](4-9-ruml-ai-query.md)         |
| `ruml:actions`        | Node                      | Action objects on any node (reactions to status)                   | [Chapter 4.10](4-10-ruml-actions.md)        |
| `ruml:context`        | Root (`data`) + Node      | Context map (context materials) and node references                | [Chapter 4.11](4-11-ruml-context.md)        |
| `ruml:text-reference` | Root (`data`) + Node      | Texts map (legal texts/norms) and node references                  | [Chapter 4.12](4-12-ruml-text-reference.md) |
| `ruml:protocol`       | Root (declaration)        | Evaluation protocol (audit trail) written into the result file     | [Chapter 4.13](4-13-ruml-protocol.md)       |
| `ruml:expression`     | Root (declaration) + Node | Combination expression for the `DELEGATED` operator (parent nodes) | [Chapter 4.14](4-14-ruml-expression.md)     |
| `ruml:tree-reference` | Root (declaration) + Node | References to nodes, and their subtrees, of other RUML files       | [Chapter 4.15](4-15-ruml-tree-reference.md) |
| `ruml:tree-include`   | Root (declaration) + Node | Evaluates a node of another RUML file in place of a leaf node      | [Chapter 4.16](4-16-ruml-tree-include.md)   |

### Experimental Capabilities (`ruml:draft/`)

Capabilities under the `ruml:draft/` prefix are in draft status:

- MAY change in name, structure, or semantics without notice.
- SHOULD NOT be used with `required: true` in production files.
- MAY be promoted to official `ruml:` capabilities or discarded in future versions.

:::note[Upgrade Path]
When a `ruml:draft/` capability becomes stable, it receives a new ID without `draft/`. Files using
the draft capability must be migrated manually.
:::

### Third-Party Capabilities (Reverse Domain)

All capabilities outside the `ruml:` namespace follow the reverse-domain convention:

```
com.example/review-notes
io.acme.legaltools/citation-style
org.myproject/custom-operator
```

The format is: `<reverse-domain>/<local-name>`

- The reverse-domain part MUST reflect a valid domain hierarchy owned by the provider.
- The local name MUST be at least one character long.
- The root-level entry MUST declare the role the rulemap expects the capability to play (see
  [Chapter 4.1](4-1-concept.md); [`CAP-03`](../08-validation/index.md#rule-cap-03)). A parser that implements the capability rejects the
  file if the declared role differs from its implementation ([`CAP-04`](../08-validation/index.md#rule-cap-04)).

### Syntax Rules

| Rule           | Description                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------- |
| Character set  | Allowed: `[a-z0-9_-]`, plus the delimiters from the prefix table and `/` (as hierarchy separator) |
| Minimum length | At least 1 character                                                                              |
| Maximum length | MUST NOT exceed 128 characters                                                                    |
| Case           | Lower case only; upper-case letters are NOT allowed                                               |
| Whitespace     | NOT allowed                                                                                       |

### Valid and Invalid Examples

```
// VALID
"ruml:query"
"ruml:draft/ai-annotations"
"com.example/review-notes"
"com.example/priority"
"io.acme/v2/legal-refs"
"de.justiz.nrw/aktenzeichen"

// INVALID — whitespace
"com.example/my capability"

// INVALID — upper case
"com.example/Review-Notes"

// INVALID — reserved prefix for third parties
"ruml:my-vendor-extension"

// INVALID — no domain, no delimiter
"layout"
"myextension"

// INVALID — empty local name
"com.example/"
```
