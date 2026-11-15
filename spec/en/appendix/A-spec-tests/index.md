<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# A. Spec Test Suite

A language-agnostic conformance suite for this specification: each test is a RUML input document
plus an expected outcome. An implementation can be checked against the suite without running any
code from this repository — every test is data.

Every test is one of two kinds:

- **Validation tests** assert whether a document is accepted or rejected, and — when rejected —
  which rule ids (see [Chapter 08 — Validation](../../08-validation/index.md)) must be reported.
- **Evaluation tests** assert the result of evaluating a document: given a set of leaf statuses, an
  implementation must produce a specific `RUML-Result` document.

Each spec section links to its own tests from a line at the end of that section's page.

## Download the test-suite

[Download the spec-test suite (.zip)](https://ruml.org/spec-tests.zip) — every `.ruml`, `.ruml-result` and
`.test.yaml` file under `cases/`, plus the descriptor schema, the rule catalogue (chapter 08) and
the [Runner Contract](runner-contract.md), so an implementation can be tested against the suite
directly.
