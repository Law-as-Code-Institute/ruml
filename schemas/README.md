<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# RUML JSON Schemas

The machine-readable structural layer of the RUML specification, and the source of truth for the
shape of RUML documents. Implementations derive their models and validators from these files.

| File                      | Validates                                             |
| ------------------------- | ----------------------------------------------------- |
| `ruml.schema.json`        | `.ruml` documents (the rulemap file format)           |
| `ruml-result.schema.json` | `.ruml-result` documents (evaluation results)         |
| `ruml-ext.schema.json`    | `.ruml-ext` documents (capability extension sidecars) |

Draft 2020-12. Validate with any conforming validator; the conditional (`if`/`then`) constraints
need one that implements them, e.g. AJV `Ajv2020` with `{ strict: false }` plus `ajv-formats`.

The spec additionally defines semantic rules that no JSON Schema dialect can express —
cross-reference resolution, sibling comparisons, JSONata parseability. Those are normative prose,
enforced in each implementation.

Full specification: https://github.com/Law-as-Code-Institute/ruml
