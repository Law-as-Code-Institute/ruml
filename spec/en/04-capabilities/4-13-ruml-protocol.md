<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.13 ruml:protocol

## 4.13 Capability `ruml:protocol`

### Overview

| Property               | Value                         |
| ---------------------- | ----------------------------- |
| **Capability ID**      | `ruml:protocol`               |
| **Scope**              | Root-Level (declaration only) |
| **Default `required`** | `false`                       |
| **Role**               | `reaction`                    |

This Capability requests an **evaluation protocol**: a chronological, machine-readable record of
everything the engine did during an evaluation — written into the RUML-Result file (see
[Chapter 5](../05-result-format/index.md)). It provides full traceability for audit purposes,
including events that never appear in a node result: data resolution, warnings, aborts,
short-circuit skips.

The protocol **complements** the per-node results: node results hold the detailed outcome per node
(status, capability details), the protocol holds the **sequence** of the run.

### Root-Level Declaration

```jsonc
"capabilities": [
  {
    "id": "ruml:protocol",
    "required": true,
    "payload": {
      "config": {
        "level": "standard"
      }
    }
  }
]
```

There is no `data` object and no node-level payload — the capability is a directive to the
evaluating engine. `ruml:protocol` MUST NOT appear in a node's `capabilities` array, neither inline
nor in a RUML-EXT file ([`CAP-18`](../08-validation/index.md#rule-cap-18)).

**Semantics:**

- If `ruml:protocol` is declared, the engine SHOULD write a protocol into the result.
- If declared with `required: true`, the engine MUST write a protocol. An engine that cannot produce
  one MUST NOT evaluate the file.
- Engines MAY write a protocol even when the capability is not declared.

**Configuration (`config`):**

| **Field** | **Type** | **Description**                                                                                               |
| --------- | -------- | ------------------------------------------------------------------------------------------------------------- |
| `level`   | Enum     | MAY specify the verbosity: `standard` (default) or `verbose`. See the event vocabulary below ([`CAP-36`](../08-validation/index.md#rule-cap-36)). |

### Protocol Format: CloudEvents

The protocol is stored in the RUML-Result file inside the `evaluation.capabilities` entry with
`id: "ruml:protocol"` — consistent with how all capability-produced data appears in results:

| **Field** | **Type** | **Description**                                                                                                                                                                                                                     |
| --------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `level`   | Enum     | The verbosity level the protocol was recorded at (`standard` or `verbose`)                                                                                                                                                          |
| `events`  | Array    | The protocol: a JSON array conforming to the [CloudEvents v1.0 JSON Batch Format](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md) (standalone media type: `application/cloudevents-batch+json`) |

Each entry in `events` is a CloudEvent; RUML defines the following profile on top of CloudEvents
v1.0:

| **Attribute** | **CloudEvents**          | **RUML profile**                                                                                            |
| ------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `specversion` | required                 | MUST be `"1.0"`                                                                                             |
| `id`          | required                 | MUST be unique within the protocol (CloudEvents: `source` + `id` unique)                                    |
| `source`      | required (URI-reference) | MUST identify the evaluating engine (and SHOULD include its version); an absolute URI is RECOMMENDED        |
| `type`        | required                 | MUST be one of the `ruml.*` event types below, or a custom type that does NOT use the `ruml.` prefix        |
| `time`        | optional in CloudEvents  | **REQUIRED** in this profile (RFC 3339)                                                                     |
| `subject`     | optional                 | The node **path** or datapoint ID the event refers to, where applicable                                     |
| `data`        | optional                 | Event payload as a direct JSON value (no `datacontenttype` ⇒ treated as `application/json` per CloudEvents) |

**Ordering:** CloudEvents does not define event ordering. In this profile, **the array order is
normative**: events MUST appear in the order the engine produced them. `time` alone is not
sufficient (multiple events may share a timestamp).

**Note on `type` naming:** CloudEvents recommends reverse-DNS type prefixes; this profile
deliberately uses the short `ruml.` prefix for specification-defined events. Implementation-specific
events MUST use a distinct prefix of their own.

### Event Vocabulary

| **Type**                    | **Level** | **`subject`** | **`data`**                                                    |
| --------------------------- | --------- | ------------- | ------------------------------------------------------------- |
| `ruml.evaluation.started`   | standard  | —             | `{ "mode": … }`                                               |
| `ruml.evaluation.completed` | standard  | —             | MAY contain summary values                                    |
| `ruml.evaluation.aborted`   | standard  | —             | `{ "reason": … }`                                             |
| `ruml.node.evaluated`       | standard  | node path     | `{ "lexId": …, "status": …, "capability"?: …, "reason"?: … }` |
| `ruml.node.skipped`         | verbose   | node path     | `{ "lexId": …, "cause": "shortCircuit" }`                     |
| `ruml.datapoint.resolved`   | verbose   | datapoint ID  | `{ "binding": …, "value"?: … }`                               |
| `ruml.action.triggered`     | standard  | node path     | `{ "operation": …, "trigger": …, "status": … }`               |
| `ruml.warning`              | standard  | optional      | `{ "message": …, "code"?: … }`                                |
| `ruml.error`                | standard  | optional      | `{ "message": …, "code"?: … }`                                |

`standard` events MUST be written at both levels; `verbose` events MUST NOT be written at
`level: "standard"`. Implementations MAY define additional event types (own prefix).

**Sensitive data:** the values of datapoints declared `sensitive: true` (see
[Chapter 4.7](4-7-data-points.md)) MUST NOT appear in the protocol — neither in `data.value` nor in
messages.

### Example

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934"
  },
  "evaluation": {
    "id": "d8129e0c-cf2e-4ef9-b7b6-fa8b206d5517",
    "timestamp": "2024-01-15T10:00:05Z",
    "mode": "complete",
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "reason": "Child 1.1 is true"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "reason": "ruml:query yields true for dp_annual_income 50000"
      }
    },
    "capabilities": [
      {
        "id": "ruml:protocol",
        "payload": {
          "level": "verbose",
          "events": [
            {
              "specversion": "1.0",
              "id": "0001",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.evaluation.started",
              "time": "2024-01-15T10:00:00Z",
              "data": {
                "mode": "complete"
              }
            },
            {
              "specversion": "1.0",
              "id": "0002",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.datapoint.resolved",
              "time": "2024-01-15T10:00:01Z",
              "subject": "dp_annual_income",
              "data": {
                "binding": "input",
                "value": 50000
              }
            },
            {
              "specversion": "1.0",
              "id": "0003",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.node.evaluated",
              "time": "2024-01-15T10:00:02Z",
              "subject": "1.1",
              "data": {
                "lexId": "2",
                "status": "true",
                "capability": "ruml:query"
              }
            },
            {
              "specversion": "1.0",
              "id": "0004",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.node.evaluated",
              "time": "2024-01-15T10:00:03Z",
              "subject": "1",
              "data": {
                "lexId": "1",
                "status": "true"
              }
            },
            {
              "specversion": "1.0",
              "id": "0005",
              "source": "https://engines.example.com/rms-engine/2.3.1",
              "type": "ruml.evaluation.completed",
              "time": "2024-01-15T10:00:05Z"
            }
          ]
        }
      }
    ]
  }
}
```

### Engine Obligations

| ID    | Requirement                                                                                                                                                                                                                        |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PT-01 | If `ruml:protocol` is declared with `required: true`, the engine MUST write the protocol into `payload.events` of the `evaluation.capabilities` entry with `id: "ruml:protocol"`; an engine that cannot MUST NOT evaluate the file |
| PT-02 | Every protocol entry MUST conform to CloudEvents v1.0 (JSON format); the array order MUST be the order of occurrence                                                                                                               |
| PT-03 | `time` MUST be present on every event (RFC 3339)                                                                                                                                                                                   |
| PT-04 | Values of `sensitive` datapoints MUST NOT appear in the protocol                                                                                                                                                                   |
| PT-05 | Implementation-specific event types MUST NOT use the `ruml.` prefix                                                                                                                                                                |
