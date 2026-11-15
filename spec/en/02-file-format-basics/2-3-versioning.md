<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.3 Versioning

### Format Version vs. Content Version

RUML distinguishes two independent version levels:

| **Level**            | **Field**          | **Description**                          | **Example**         |
| -------------------- | ------------------ | ---------------------------------------- | ------------------- |
| **Format version**   | `$specVersion`     | Version of the RUML specification        | "1.0", "1.1", "2.0" |
| **Document version** | `metadata.version` | Version of the content of this RUML file | "2024.1.0", "1.0.0" |

### Semantic Versioning for Format Version

The format version follows Semantic Versioning:

- **MAJOR**: Incompatible changes (1.0 → 2.0)
- **MINOR**: [Backward-compatible](#the-specversion-field) extensions (1.0 → 1.1)
- **PATCH**: Bug fixes in the specification (1.0.0 → 1.0.1)

:::note[Backward compatibility]
Within a MAJOR version, new versions of the specification keep the schemas and the evaluation
behavior backward-compatible: RUML files, RUML-Ext files and RUML Result files that are valid under
one version stay valid under later MINOR and PATCH versions, and a RUML file evaluates, together
with its RUML-Ext files, to the same result. Only a new MAJOR version can break this.
:::

### The `$specVersion` Field

The `$specVersion` field consists of MAJOR and MINOR only; a PATCH version bump does not change it.
It defines the version of the specification the file conforms to. The schemas list the versions a
file may declare, in the `enum` of `$specVersion` ([`FMT-04`](../08-validation/index.md#rule-fmt-04)).

The version of a parser or evaluator is the highest version of the specification it implements.

Parser requirements:

- A parser MUST accept a file whose `$specVersion` has its MAJOR version and a MINOR version up to
  its own ([`FMT-09`](../08-validation/index.md#rule-fmt-09)).
- A parser MUST reject a file whose `$specVersion` has a higher MINOR version or a different MAJOR
  version with a clear error message ([`FMT-09`](../08-validation/index.md#rule-fmt-09)).

Evaluator requirements:

- The input version of an evaluation is the highest `$specVersion` among the RUML file and its
  RUML-Ext files.
- If the input version has an earlier MINOR version than their own, evaluators MUST produce the same
  result as an evaluator that implements the input version.
- The result MUST have the input version as its `$specVersion`, not the evaluator's version.
