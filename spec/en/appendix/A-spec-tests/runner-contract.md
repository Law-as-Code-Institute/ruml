<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Runner Contract

This document describes how to implement a test runner from the spec-test suite.

The conformance test ZIP file contains a number of YAML files describing the various tests. In
addition, there are fixtures (i.e., ruml and ruml-result files) that are referenced by the YAML
files.

The ZIP file has the following layout:

```
spec-tests/
  rule-catalogue.md            the validation rules (chapter 08), in the ZIP only
  runner-contract.md           this document
  schema/spec-test.schema.json JSON Schema for every *.test.yaml
  schemas/                     the JSON Schemas of the format: ruml.schema.json, ruml-ext.schema.json
                               and ruml-result.schema.json, as published with this release
  cases/<chapter>/             descriptors and fixtures, mirroring the spec's chapter directories
```

A runner can discover all test-cases by evaluating the glob `cases/**/*.test.yaml`. Inside the
test-cases the references to fixtures are relative to the directory of the test-case file.

Descriptors are named after the spec section page they test — `<page>.test.yaml`
(`3-6-operators.test.yaml`), or `<page>--<suffix>.test.yaml` (`3-6-operators--and.test.yaml`) when a
section's tests are split over several files — with its fixtures in the sibling directory
`<page>.fixtures/`. The `title` of a split descriptor is the page title followed by a qualifier in
parentheses (`3.6 Operators (AND)`). Related tests within a file share a name prefix (`and--`,
`not-xor--`, …).

File extensions:

| Extension      | Content                                                            |
| -------------- | ------------------------------------------------------------------ |
| `.ruml`        | a RUML document (`$format: "RUML"`)                                |
| `.ruml-result` | a RUML evaluation result (`$format: "RUML-Result"`), per spec §2.2 |
| `.test.yaml`   | a test descriptor (as described in `schema/spec-test.schema.json`  |

## Descriptor shape

A descriptor holds one or more tests. `kind` is required on every test and selects what it asserts:
`evaluation` or `validation`.

```yaml
spec: ["3.6"] # spec sections this file covers, one entry each
tests:
  - name: ... # unique within the file
    kind: validation # or: evaluation
    # ...
```

The following types of tests exist:

## kind: validation

Example:

```yaml
test:
  - name: "wrong-format-discriminator"
    kind: "validation"
    spec: ["2.2"]
    description: '`$format` is `"RMLX"` instead of the required `"RUML"`.'
    ruml: "2-2-file-structure.fixtures/reject-wrong-format-discriminator.ruml"
    layer: "schema"
    expect: "reject" # or "accept"
    rules: ["FMT-03"]
    at: ["/$format"]
    # optional:
    warnings: ["NODE-03"]
    # optional
    covers: ["CAP-15"]
```

The fields `name`, `spec`, `description`, `layer` and `covers` are purely informative and described
in `schema/spec-test.schema.json`.

A runner implementing these tests MUST

- resolve the file referenced in the `ruml`-property,
- parse the contents
- if `expect` is `accept` then it MUST fail if the parser throws an error, otherwise succeed
- if `expect` is `reject`
  - it MUST fail if the parser throws NO error.
  - it CAN fail if the parser does not provide codes specified in the `rule` property.
  - it CAN fail if the parser does not provide the location specified in the `at` property.
  - it CAN fail if the parser does not provide the warnings specified in the `warnings` property.

A `.ruml` fixture used by a validation test is named `accept-…` or `reject-…` after the outcome its
case expects, so a directory listing shows at a glance which documents are valid RUML and which are
not. Nothing enforces it — a runner reads the descriptor's `ruml` field, not the file name — but the
prefix is how the fixtures in `cases/` are named.

## kind: evaluation

Example:

```yaml
test:
  - name: and--short-circuit
    kind: evaluation
    spec: ["3.6"]
    description: >-
      AND stops at the first false child in `optimized` mode. The later leaves are never reached, so
      they produce no result of their own — and their `inputs` entries go unused, which is not an
      error.
    ruml: 3-6-operators.fixtures/and.ruml
    expect: 3-6-operators.fixtures/and--short-circuit.ruml-result
    run:
      evaluationId: 39d467ac-8e6a-4fa5-bb36-eebbf6aec1a7
      frozenClock: "2026-08-20T12:00:00.000Z"
      mode: optimized
    inputs:
      "1.1": { lexId: "2", status: "false" }
      "1.2": { lexId: "3", status: "true" }
      "1.3": { lexId: "4", status: "true" }
```

The `name`, `spec`, and `description` fields are purely informative and described in
`schema/spec-test.schema.json`.

A runner implementing these tests must:

- resolve, load and parse the file referenced via `ruml`.
- resolve, load and parse the file referenced via `expect`
- evaluate the RUML with the evaluation mode specified by `run.mode`, setting the value of the leaf
  nodes to the values specified in `input`
  - the key of the `input` object is the path to the leaf node. `1.2.4` means: The fourth child of
    the second child of the root node.
  - the `lexId` matches the `lexId` of that node and CAN be used to ensure the correctness of the
    test-runner.
  - The `status` is `"true"`, `"false"` or `"undefined"` and represents the value of the leaf node.
- during the evaluation, simulate a frozen time and a fixed UUID, if the test specifies
  `run.frozenClock` or `run.evaluationId`
  - simulate a frozen time: every `evaluatedAt` and `evaluation.timestamp` value is
    `run.frozenClock`.
  - use `run.evaluationId` as the UUID of the evaluation, so that `evaluation.id` is
    `run.evaluationId`.
- perform a structural comparison of the RUML-result to the parsed result referenced in `expect`.
- the test MUST fail if and only if the RUML-result is different from the expected result.

### Comparison

- object key order is insignificant;
- an absent field and a `null` field are equivalent;
- the timestamp fields `timestamp`, `evaluatedAt` and `startTimestamp` are compared as instants, not
  as strings: `2026-08-20T12:00:00Z` and `2026-08-20T12:00:00.000+00:00` are equal;
- The runner MAY compare the string `reason` of `true` and `false` nodes and the `message` of the
  reason of `undefined` nodes, but they are **not** defined by the specification. They come from
  this suite.

## Test capabilities

Some fixtures use capabilities outside the `ruml:` namespace, to test how a parser handles
non-official capabilities. There is one per role, with the id `org.ruml.test/<role>`. A runner MUST
let its parser recognize each of them with the role given here. Otherwise the parser rejects any
fixture that declares one of them `required: true` (rule `CAP-01`), or compares a declared role
against the wrong implementation (rule `CAP-04`).

| Capability id            | Role       | Behavior                                                                                                                                                                                                                  | Payload example                                  |
| ------------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `org.ruml.test/data`     | `data`     | none; the suite reads no data from it                                                                                                                                                                                     | `{ "status": "pending" }`                        |
| `org.ruml.test/decision` | `decision` | the leaf's status is the `result` field of the node payload: `"true"`, `"false"` or `"undefined"`                                                                                                                         | `{ "result": "true" }`                           |
| `org.ruml.test/combiner` | `combiner` | the node's status is the status of the child at position `pickChildResult` of the node payload, counted from 1 like the `inputs` paths; `undefined` if that child does not exist or any child is `undefined` (see §3.6.4) | `{ "description": "...", "pickChildResult": 1 }` |
