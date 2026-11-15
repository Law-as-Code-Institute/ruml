<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 05. RUML Result Format

Evaluation results MUST be stored in a separate RUML result file (`.ruml-result`). When loading a
RUML result file, actions are **NOT** re-triggered — the stored result serves exclusively for
documentation purposes.

This chapter describes the format of the RUML result file (`.ruml-result`), in which evaluation
results of a rulemap are stored. Its structure is defined by the JSON Schema
[`ruml-result.schema.json`](../../../schemas/ruml-result.schema.json)
([draft 2020-12](https://json-schema.org/draft/2020-12)).

- [5.0 Node Status](5-0-status-types.md) — The possible node statuses (`true`, `false`, `undefined`,
  `ignored`)
- [5.1 Result Model and Storage](5-1-result-model.md) — RUML result file, integrity assurance, and
  examples
