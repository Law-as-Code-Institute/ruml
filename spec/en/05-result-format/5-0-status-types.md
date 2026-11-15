<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 5.0 Node Status

Each node that has a result MUST have one of the following four statuses. The status is a **runtime
concept** — it is not stored in the RUML file but in the associated RUML result file
(`.ruml-result`, see [Section 5.1](5-1-result-model.md)).

| Status      | Description      | Semantics                                                                                            |
| ----------- | ---------------- | ---------------------------------------------------------------------------------------------------- |
| `true`      | Fulfilled        | The condition of the node is fulfilled.                                                              |
| `false`     | Not fulfilled    | The condition of the node is not fulfilled.                                                          |
| `undefined` | Not determinable | The evaluation was performed, but the result could not be unambiguously determined.                  |
| `ignored`   | Skipped          | The evaluation was intentionally skipped (e.g., due to short-circuit evaluation or manual decision). |

Each node result MUST also provide a reason for its status; the fields of the reason depend on the
status.

Nodes MUST NOT be included in the result before they have been evaluated or ignored.

### true

`true` indicates that the condition of the node is fulfilled:

- **For leaf nodes:** The decision-relevant capabilities yield `true`
- **For parent nodes:** The operator logic over the child results yields `true`

#### Reason

Required. A string with a human-readable justification:

_Node 1.1 – true_

```jsonc
"1.1": {
  "lexId": "2",
  "status": "true",
  "reason": "Age 34 >= 18",
  "capabilities": [/* ... */]
}
```

### false

`false` indicates that the condition of the node is not fulfilled:

- **For leaf nodes:** The decision-relevant capabilities yield `false`
- **For parent nodes:** The operator logic over the child results yields `false`

#### Reason

Required. A string with a human-readable justification:

_Node 1.4 – false_

```jsonc
"1.4": {
  "lexId": "3",
  "status": "false",
  "reason": "Credit score 540 < 600",
  "capabilities": [/* ... */]
}
```

### undefined

`undefined` indicates that an evaluation was performed but no unambiguous result could be
determined. Typical causes:

- **Missing data:** Required input data for the evaluation is not available
- **Technical errors:** API errors, timeouts, or system failures during evaluation
- **Logical undecidability:** Contradictory rules or data
- **Capability without result:** A decision-relevant capability could not determine an unambiguous
  result

**Important:** `undefined` means "evaluation performed, but no result possible" — not "evaluation
not performed".

#### Reason

Required. An object with the following fields, all required:

| Field     | Type   | Description                                          |
| --------- | ------ | ---------------------------------------------------- |
| `type`    | Enum   | Cause of the `undefined` status, see the table below |
| `message` | String | Human-readable explanation (non-empty)               |

Additional fields are NOT permitted.

The `type` field MUST have one of the following values.

| Value     | Cause                                                                                                                                                                        |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error`   | A technical error prevented a result, e.g. a failed API call, a timeout, or a node deeper than the maximum recursion depth (see [6.4](../06-modular-nodes/6-4-recursion.md)) |
| `default` | Any other cause, e.g. missing data                                                                                                                                           |

_Node 1.3.2.2 – error: deeper than the maximum recursion depth_

```jsonc
"1.3.2.2": {
  "lexId": "8",
  "status": "undefined",
  "reason": {
    "type": "error",
    "message": "Recursion depth 2 exceeds the maximum recursion depth of 1"
  }
}
```

_Node 1.2 – default: missing data_

```jsonc
"1.2": {
  "lexId": "4",
  "status": "undefined",
  "reason": {
    "type": "default",
    "message": "dp_income is missing"
  },
  "capabilities": [/* ... */]
}
```

### ignored

`ignored` differs from `undefined` in that the evaluation was **intentionally not performed**.
Typical causes:

- **Short-circuit evaluation in optimized mode** (see chapter
  [3.6 Operators](../03-data-model/3-6-operators.md))
- **Manual skip:** A user intentionally skipped the evaluation
- **Conditional deactivation:** The node was deactivated due to preconditions

#### Reason

Required. An object with the following fields, all required:

| Field      | Type   | Description                                                                                                                                                                                                                                                                                                                                                                    |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`     | Enum   | Cause of the skip, see the table below                                                                                                                                                                                                                                                                                                                                         |
| `trigger`  | String | Identifier of the sibling or node that caused the skip (non-empty)                                                                                                                                                                                                                                                                                                             |
| `operator` | Enum   | Operator of the parent node; tools use it to display the result. With `type: "shortCircuit"`, it MUST be `AND`, `XOR`, `NOT_AND`, `NOT_XOR` or `undefined`: `OR`, `NOT_OR` and `DELEGATED` MUST NOT short-circuit (see [Chapter 3.6.2](../03-data-model/3-6-operators.md#362-or-and-not_or) and [Chapter 3.6.4](../03-data-model/3-6-operators.md#364-the-delegated-operator)) |
| `mode`     | Enum   | Evaluation mode under which the node was skipped: `optimized`, `complete`                                                                                                                                                                                                                                                                                                      |

Additional fields are NOT permitted.

The `type` field MUST have one of the following values.

| Value                     | Cause                                           |
| ------------------------- | ----------------------------------------------- |
| `shortCircuit`            | Short-circuit evaluation by the parent operator |
| `manualSkip`              | A user intentionally skipped the node           |
| `conditionalDeactivation` | The node was deactivated due to preconditions   |

_Node 1.5 – shortCircuit: the parent's AND is already false because of node 1.4_

```jsonc
"1.5": {
  "lexId": "5",
  "status": "ignored",
  "reason": {
    "type": "shortCircuit",
    "trigger": "1.4",
    "operator": "AND",
    "mode": "optimized"
  }
}
```

**Important:** `ignored` means "intentionally not evaluated" — not "error during evaluation". An
`ignored` node is NOT included in the operator calculation of the parent node.
