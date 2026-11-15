<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 5.1 Result Model and Storage

### 5.1.1 Basic Concept

After completion of an evaluation, the results MAY be stored persistently. Evaluation results MUST
be stored in a separate RUML result file (`.ruml-result`). Embedding evaluation results in a RUML
file (`.ruml`) is NOT permitted.

---

**Contents of an evaluation result:**

A complete evaluation result SHOULD contain the following information:

- **Metadata:** ID, timestamp, evaluation mode used, case reference
- **Node status:** The final status of each evaluated node (`true`, `false`, `undefined`,
  `ignored`). Nodes with status `pending` are NOT stored — a missing entry in the `results` object
  implicitly means `pending`.
- **Justifications:** Explanations for the respective result
- **Capability results:** Capability-specific evaluation data per node (e.g., query results,
  triggered actions)
- **Active capabilities:** Declaration of the capabilities used during evaluation

---

### 5.1.2 RUML Result File

The evaluation result is stored in a separate file that references the RUML structure.

---

**File extension:** `.ruml-result`

**Structure:**

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d9c7e5c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e"
  },
  "evaluation": {
    "id": "17175dae-2a30-4757-b146-71bdb114eea6",
    "timestamp": "2024-01-15T10:00:00Z",
    "mode": "complete",
    "caseId": "Fall-2024-00123",
    "capabilities": [
      {
        "id": "ruml:datapoints"
      },
      {
        "id": "ruml:query"
      },
      {
        "id": "ruml:actions"
      }
    ],
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "reason": "AND: alle Kinder true"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "reason": "Alter 25 >= 18"
      },
      "1.2": {
        "lexId": "3",
        "status": "true",
        "reason": "XOR: genau ein Kind true"
      },
      "1.2.1": {
        "lexId": "4",
        "status": "true",
        "reason": "Einkommen 35000 <= 40000"
      },
      "1.2.2": {
        "lexId": "5",
        "status": "false",
        "reason": "Kein Härtefall"
      },
      "1.3": {
        "lexId": "6",
        "status": "true",
        "reason": "Wohnsitz BY == BY"
      }
    }
  }
}
```

---

**Required fields in the rumlReference object:**

| Field | Type | Description                    |
| ----- | ---- | ------------------------------ |
| `id`  | UUID | ID of the referenced RUML file |

**Optional fields in the rumlReference object:**

| Field  | Type   | Description                                                                                                                                                                            |
| ------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hash` | String | Hash of the referenced RUML file for integrity verification. When present, the tool verifies it; when absent, the RUML structure cannot be integrity-checked and the tool SHOULD warn. |

---

**Required fields in the evaluation object:**

| Field       | Type     | Description                                    |
| ----------- | -------- | ---------------------------------------------- |
| `id`        | UUID     | Unique ID of the evaluation result             |
| `timestamp` | DateTime | Time of evaluation completion                  |
| `mode`      | Enum     | Evaluation mode used (`optimized`, `complete`) |
| `results`   | Object   | Results per node instance, indexed by path     |

---

**Optional fields in the evaluation object:**

| Field            | Type     | Description                                                                                                                                                                                                                                                                                                                                                                           |
| ---------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `caseId`         | String   | External case reference (e.g., file reference number)                                                                                                                                                                                                                                                                                                                                 |
| `userId`         | String   | ID of the evaluating user                                                                                                                                                                                                                                                                                                                                                             |
| `toolId`         | String   | ID of the executing tool                                                                                                                                                                                                                                                                                                                                                              |
| `toolVersion`    | String   | Version of the executing tool                                                                                                                                                                                                                                                                                                                                                         |
| `startTimestamp` | DateTime | Time of evaluation start                                                                                                                                                                                                                                                                                                                                                              |
| `capabilities`   | Array    | MAY declare the capabilities active during evaluation as entries of `{ id, payload? }`; their order is not significant. Capability-specific fields (e.g., model version, configuration) MAY be included in the entry's `payload`. For `ruml:protocol`, the entry's `payload` carries the recorded evaluation protocol (see [Chapter 4.13](../04-capabilities/4-13-ruml-protocol.md)). |

---

**The `results` property**

The results property MUST contain one node result for each node evalution, indexed by its path and
for each node that has been ignored because of a short-circuit in optimized mode (see
[Chapter 3.6](../03-data-model/3-6-operators.md#evaluation-mode)). Child nodes of ignored nodes MUST
NOT be part of the `results` object.

The key of the nodes objects MUST be a dot-separated list of one-based array indexes in the
`children`-array of each node.

| Path    | Node                                                 |
| ------- | ---------------------------------------------------- |
| `1`     | The root node                                        |
| `1.2`   | The second child of the root node                    |
| `1.2.1` | The first child of the second child of the root node |

**Structure of a node result:**

```jsonc
"results": {
  "1": {
    "lexId": "1",
    "status": "true",
    "evaluatedAt": "2024-01-15T10:00:01Z",
    "reason": "Alle Voraussetzungen erfüllt",
    "capabilities": [
      {
        "id": "ruml:query",
        "payload": {
          "expression": "dp_age >= 18",
          "inputs": {
            "dp_age": 25
          },
          "result": "true"
        }
      },
      {
        "id": "ruml:actions",
        "payload": {
          "triggered": [
            {
              "id": "notify-approval",
              "trigger": "onTrue",
              "operation": "sendNotification",
              "timestamp": "2024-01-15T10:00:02Z",
              "status": "success"
            }
          ]
        }
      }
    ]
  }
}
```

---

**Fields of a node result:**

| Field          | Type             | Required | Description                                                                                                                                  |
| -------------- | ---------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `lexId`        | String           | Yes      | The `lexId` of the node to which this result refers (pattern `^[1-9][0-9]*$`)                                                                |
| `status`       | Enum             | Yes      | Final status: `true`, `false`, `undefined`, `ignored`. `pending` is not a valid value — pending nodes do not appear in the `results` object. |
| `evaluatedAt`  | DateTime         | No       | Time at which this node was evaluated                                                                                                        |
| `reason`       | String or Object | Yes      | Reason for the status; its shape depends on `status`, see [Chapter 5.0](5-0-status-types.md)                                                 |
| `capabilities` | Array            | No       | Capability-specific evaluation results as ordered entries of `{ id, payload? }`; each `id` is a capability active during evaluation.         |

**Node-result payload of `ruml:query`:**

| Field        | Type   | Required | Description                                                                                                              |
| ------------ | ------ | -------- | ------------------------------------------------------------------------------------------------------------------------ |
| `expression` | String | Yes      | The evaluated query expression (non-empty, see [Chapter 4.8](../04-capabilities/4-8-ruml-query.md))                      |
| `inputs`     | Object | Yes      | Resolved input values referenced by the expression, keyed by DataPoint ID                                                |
| `result`     | Enum   | Yes      | Computed result of the expression: `true`, `false`, `undefined` — the same string values as `status`, written as strings |

Additional fields are NOT permitted.

**Node-result payload of `ruml:expression`:**

| Field        | Type   | Required | Description                                                                                                         |
| ------------ | ------ | -------- | ------------------------------------------------------------------------------------------------------------------- |
| `expression` | String | Yes      | The evaluated expression (non-empty, see [Chapter 4.14](../04-capabilities/4-14-ruml-expression.md))                |
| `inputs`     | Object | Yes      | Resolved datapoint values referenced by the expression, keyed by DataPoint ID; empty when it reads none             |
| `children`   | Array  | Yes      | The child results the expression saw, as `{ lexId, status }`, in `children` order; each status is `true` or `false` |
| `result`     | Enum   | Yes      | Computed result of the expression: `true`, `false`, `undefined`                                                     |

Additional fields are NOT permitted. Recording the child statuses is what makes the decision
reproducible: unlike a logical operator, the rule is not implied by the operator name. The payload
is written only when the expression ran; a node that is `undefined` because a child is `undefined`
carries no `ruml:expression` payload.

---

**Path-based indexing and modular nodes:**

The `results` object uses the **path** as key, not the `lexId`. This design decision enables correct
handling of modular nodes (see [Chapter 6](../06-modular-nodes/index.md)):

- **Regular nodes:** Have exactly one path and therefore exactly one entry in `results`
- **Modular nodes:** Can be referenced at multiple locations in the tree. Each instance has its own
  path and can have a **different result**. Therefore, each instance receives its own entry in
  `results`.

**Example of a modular node with different results:**

```jsonc
"results": {
  "1": {
    "lexId": "1",
    "status": "false",
    "reason": "AND: Kind 1.2 false"
  },
  "1.1": {
    "lexId": "8",
    "status": "true",
    "reason": "Bonität ausreichend"
  },
  "1.2": {
    "lexId": "2",
    "status": "false",
    "reason": "AND: Kind 1.2.1 false"
  },
  "1.2.1": {
    "lexId": "8",
    "status": "false",
    "reason": "Bonität nicht ausreichend"
  }
}
```

In this example, the node with `lexId: 8` is referenced at two locations (paths `1.1` and `1.2.1`)
and has different results (`true` vs. `false`).

---

**Behavior on loading:**

1. Tool loads the RUML result file
2. Tool loads the referenced RUML file using `rumlReference.id`
3. If `rumlReference.hash` is present: tool verifies the hash of the RUML file against it
4. If hash matches (or no hash is present and the RUML file is found): use the RUML file
5. If hash mismatch: tool MUST issue a warning that the rule structure cannot be reconstructed
6. If `rumlReference.hash` is absent: the tool MAY use the RUML file but SHOULD warn that its
   integrity cannot be verified
7. If the referenced RUML file is missing: tool MUST issue a warning that the rule structure cannot
   be reconstructed

---

### 5.1.3 Integrity Assurance

For legally relevant proceedings, the integrity of results MUST be guaranteed. Integrity assurance
of RUML result files is handled at the container level (see Chapter 7).

---

**Hash requirements:**

| Hash          | Purpose                                          | Calculation                 |
| ------------- | ------------------------------------------------ | --------------------------- |
| **RUML hash** | Ensures that the structure has not been modified | As defined in Chapter 3.2.4 |

---

**Verification:**

When loading a RUML result file, implementations SHOULD:

1. Verify the RUML hash against the referenced RUML file
2. In case of discrepancies: warn the user and document the discrepancy

---

### 5.1.4 Application Scenarios

| Scenario                | Description                                                                            |
| ----------------------- | -------------------------------------------------------------------------------------- |
| Mass proceedings        | A rulemap is evaluated for many cases — each case receives its own `.ruml-result` file |
| Case management systems | Results are integrated into existing case file structures                              |
| Long-term archival      | Separation of structure and instance for audit-proof storage                           |
| Versioned rulemaps      | Multiple results can reference different versions of the same rulemap                  |
| Tenant separation       | Results can be stored separately per tenant                                            |
| Individual case review  | Individual cases are also stored as `.ruml-result` files                               |

---

### 5.1.5 Complete Example

The following example shows a RUML file and the associated RUML result file. The rulemap checks the
prerequisites for a funding application.

---

**File 1: `foerderantrag.ruml`**

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_age": {
            "name": "Alter des Antragstellers",
            "type": "integer",
            "binding": {
              "type": "input"
            }
          },
          "dp_income": {
            "name": "Jahreseinkommen",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            }
          },
          "dp_hardship": {
            "name": "Härtefall anerkannt",
            "type": "boolean",
            "binding": {
              "type": "input"
            }
          },
          "dp_state": {
            "name": "Bundesland des Wohnsitzes",
            "type": "string",
            "binding": {
              "type": "input"
            }
          }
        }
      }
    },
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:actions"
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z",
    "created": "2024-01-10T09:00:00Z",
    "modified": "2024-01-10T09:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
        "operator": "AND",
        "label": "Fördervoraussetzungen",
        "children": ["2", "3", "6"]
      },
      "2": {
        "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
        "label": "Antragsteller volljährig",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_age >= 18"
            }
          }
        ]
      },
      "3": {
        "id": "42d9431d-b7db-404f-bdf9-7ecdde505cce",
        "operator": "XOR",
        "label": "Einkommensprüfung",
        "children": ["4", "5"]
      },
      "4": {
        "id": "52820488-2849-4487-842b-952dc3ba301d",
        "label": "Einkommen unter Grenze",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_income <= 40000"
            }
          }
        ]
      },
      "5": {
        "id": "48b34df4-06bb-4dc2-aeb7-807a146760f4",
        "label": "Härtefall anerkannt",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_hardship = true"
            }
          }
        ]
      },
      "6": {
        "id": "92f909f1-0097-4d9d-87d2-1734bf299d08",
        "label": "Wohnsitz in Bayern",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_state = \"BY\""
            }
          },
          {
            "id": "ruml:actions",
            "payload": {
              "onFalse": {
                "operation": "sendNotification",
                "ref": "notification_service",
                "config": {
                  "template": "antrag-falsches-bundesland",
                  "channel": "email"
                }
              }
            }
          }
        ]
      }
    }
  }
}
```

---

**File 2: `foerderantrag-fall-00456.ruml-result`**

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d9c7e5c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e"
  },
  "evaluation": {
    "id": "7f3d1c88-2b4e-4a19-9c5d-0e6f1a2b3c4d",
    "timestamp": "2024-01-15T10:00:00Z",
    "mode": "optimized",
    "caseId": "Antrag-2024-00456",
    "capabilities": [
      {
        "id": "ruml:datapoints"
      },
      {
        "id": "ruml:query"
      },
      {
        "id": "ruml:actions"
      }
    ],
    "results": {
      "1": {
        "lexId": "1",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:04Z",
        "reason": "Alle Voraussetzungen erfüllt (AND: alle Kinder true)"
      },
      "1.1": {
        "lexId": "2",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:01Z",
        "reason": "Alter 25 >= 18",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_age >= 18",
              "inputs": {
                "dp_age": 25
              },
              "result": "true"
            }
          }
        ]
      },
      "1.2": {
        "lexId": "3",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:02Z",
        "reason": "XOR erfüllt: Einkommen unter Grenze"
      },
      "1.2.1": {
        "lexId": "4",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:02Z",
        "reason": "Einkommen 35000 <= 40000",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_income <= 40000",
              "inputs": {
                "dp_income": 35000
              },
              "result": "true"
            }
          }
        ]
      },
      "1.2.2": {
        "lexId": "5",
        "status": "ignored",
        "reason": {
          "type": "shortCircuit",
          "trigger": "Knoten 1.2.1 (lexId: 4) wurde true",
          "operator": "XOR",
          "mode": "optimized"
        }
      },
      "1.3": {
        "lexId": "6",
        "status": "true",
        "evaluatedAt": "2024-01-15T10:00:03Z",
        "reason": "Wohnsitz BY == BY",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_state = \"BY\"",
              "inputs": {
                "dp_state": "BY"
              },
              "result": "true"
            }
          }
        ]
      }
    }
  }
}
```

---

**Explanation of the evaluation flow:**

1. Node 1.1 (Applicant of legal age): Age 25 >= 18 -> `true`
2. Node 1.2.1 (Income below threshold): 35,000 <= 40,000 -> `true`
3. Node 1.2.2 (Hardship case): Not evaluated (short-circuit), since node 1.2.1 is already `true` and
   the parent operator is `XOR` -> `ignored`
4. Node 1.2 (Income check): XOR with `true`, `ignored` -> `true`
5. Node 1.3 (Residence): BY == BY -> `true`
6. Node 1 (Root): AND with `true`, `true`, `true` -> `true`

---

**Notable aspects:**

- The RUML file contains exclusively the rule structure — no evaluation results
- The `results` object in the `.ruml-result` file uses the **path** as string key
- Each node result contains the `lexId` as a required field to enable mapping to the node object
- For modular nodes (see [Chapter 6](../06-modular-nodes/index.md)), multiple entries with different
  paths but the same `lexId` exist
- Node 1.2.2 demonstrates the `ignored` status through short-circuit evaluation in `optimized` mode
- Capability-specific evaluation data (e.g., query expressions and input values) are documented in
  the `capabilities` object of the respective node result
