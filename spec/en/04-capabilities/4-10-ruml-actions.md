<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.10 ruml:actions

## 4.10 Capability `ruml:actions`

### Overview

| Property               | Value                                         |
| ---------------------- | --------------------------------------------- |
| **Capability ID**      | `ruml:actions`                                |
| **Scope**              | Node-Level (`capabilities` field on the node) |
| **Default `required`** | `false`                                       |
| **Role**               | `reaction`                                    |

This Capability provides action objects on nodes. Actions trigger operations based on the status of
a node. They do not make decisions but react to the truth value determined by Data Queries, AI
Queries, or operator logic.

### Use Cases

Actions can fundamentally trigger anything that a computer command can trigger. The following list
shows examples and is not exhaustive:

- Trigger other Rulemaps (e.g., detailed check after a positive result)
- Send notifications (email, SMS, push, messenger)
- Set and monitor deadlines (e.g., objection period after a notice)
- Trigger queries and data requests (e.g., request missing documents)
- Call external systems (APIs, webhooks, third-party systems)
- Create documents (notices, reports, protocols)
- Create or update case files (CRM, ERP, specialized procedures)
- Request human decisions (workflows, approval processes)
- Trigger payments or bookings
- Grant or revoke permissions
- Escalate, archive, or forward cases
- Write logging and audit trail entries

### Core Principle: Reaction to Node Status

Actions are defined via the `capabilities` entry with `id: "ruml:actions"` on a node and react to
its status:

| **Node Status** | **Meaning**                                    | **Example Action**         |
| --------------- | ---------------------------------------------- | -------------------------- |
| `true`          | Condition met                                  | Create approval document   |
| `false`         | Condition not met                              | Create rejection document  |
| `undefined`     | Evaluated but undecidable (e.g., missing data) | Send email requesting data |

### Embedding via Capability

Actions are provided via the `ruml:actions` Capability in the `capabilities` array of a node:

```jsonc
"1": {
  "id": "fcf02185-ffee-48a4-bf93-d2fb1b17944d",
  "label": "Einkommensprüfung",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_annual_income > 50000"
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "onTrue": {
          "operation": "createDocument",
          "ref": "approval_document_service"
        },
        "onFalse": {
          "operation": "sendNotification",
          "ref": "rejection_notification_service"
        }
      }
    }
  ]
}
```

**Rules:**

- Actions MAY be defined on any node (Leaf-Nodes and Parent-Nodes) ([`CAP-34`](../08-validation/index.md#rule-cap-34))
- On Leaf-Nodes without a `decision` capability (`ruml:query` or `ruml:ai-query`), the node status
  is always `undefined`. Only an `onUndefined` handler can trigger in this case; `onTrue` and
  `onFalse` handlers will never fire.
- On Parent-Nodes, `ruml:actions` MAY stand alone; the status is derived from the operator logic of
  the children ([`CAP-34`](../08-validation/index.md#rule-cap-34))

### Trigger Condition for Actions

Actions are only triggered when the respective node was actually evaluated during the current
traversal. Nodes that were not reached due to a prior evaluation abort do not trigger actions —
regardless of their status.

**Example:**

```
Node 1 (AND)
├── Node 2: Evaluated → true
├── Node 3: Evaluated → undefined (data missing) → Action is triggered
├── Node 4: Not reached (evaluation stopped at Node 3) → No action
└── Node 5: Not reached → No action
```

In this example, only the `onUndefined` action of Node 3 is triggered, not those of Node 4 or Node
5, even though their status is also `undefined`.

**Note:** The details on evaluation order and abort behavior are specified in Chapter 5 (Decision
Status).

### Structure

```jsonc
"1": {
  "id": "7baae662-0b5c-44bb-9a2b-802074fe5d0f",
  "label": "Bescheiderstellung",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_application_complete = true"
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "description": "Erstellt den entsprechenden Bescheid basierend auf der Entscheidung",
        "onTrue": {
          "operation": "createDocument",
          "ref": "approval_document_service",
          "config": {
            "template": "approval-letter",
            "format": "pdf"
          }
        },
        "onFalse": {
          "operation": "createDocument",
          "ref": "rejection_document_service",
          "config": {
            "template": "rejection-letter",
            "format": "pdf"
          }
        },
        "onUndefined": {
          "operation": "sendNotification",
          "ref": "email_service",
          "config": {
            "template": "missing-data-request",
            "channel": "email"
          }
        }
      }
    }
  ]
}
```

### Actions Object Fields

| **Field**     | **Type** | **Description**                                         |
| ------------- | -------- | ------------------------------------------------------- |
| `description` | String   | MAY describe which actions are executed ([`CAP-35`](../08-validation/index.md#rule-cap-35)) |
| `onTrue`      | Object   | MAY define the action for status `true`                 |
| `onFalse`     | Object   | MAY define the action for status `false`                |
| `onUndefined` | Object   | MAY define the action for status `undefined`            |

**Note:** At least one of the fields `onTrue`, `onFalse`, or `onUndefined` MUST be present
([`CAP-35`](../08-validation/index.md#rule-cap-35)).

### Action Object

Each action object (`onTrue`, `onFalse`, `onUndefined`) has the following structure:

```jsonc
"onTrue": {
  "operation": "createDocument",
  "ref": "document_service",
  "config": {
    "template": "approval-letter",
    "format": "pdf"
  }
}
```

| **Field**   | **Type** | **Description**                                                         |
| ----------- | -------- | ----------------------------------------------------------------------- |
| `operation` | String   | MUST specify the type of action ([`CAP-35`](../08-validation/index.md#rule-cap-35))                         |
| `ref`       | String   | MUST contain a symbolic reference to the implementation ([`CAP-35`](../08-validation/index.md#rule-cap-35)) |
| `config`    | Object   | MAY contain configuration hints for the action ([`CAP-35`](../08-validation/index.md#rule-cap-35))          |

### Operations

The `operation` field specifies the type of action. The following list is not exhaustive and MAY be
extended by implementations:

| **Operation**      | **Description**                                   |
| ------------------ | ------------------------------------------------- |
| `triggerRulemap`   | Process another Rulemap                           |
| `sendNotification` | Send a notification (email, SMS, push, messenger) |
| `requestData`      | Trigger a query or data request                   |
| `callWebhook`      | Call a webhook or external API                    |
| `triggerProcess`   | Start an external process                         |
| `createDocument`   | Generate a document (notice, report, protocol)    |
| `createCase`       | Create or update a case file                      |
| `requestDecision`  | Request a human decision                          |
| `initiatePayment`  | Trigger a payment or booking                      |
| `managePermission` | Grant or revoke a permission                      |
| `archive`          | Archive a case                                    |
| `writeAuditLog`    | Write a logging or audit trail entry              |

**Note:** Implementations MAY define additional operations ([`CAP-35`](../08-validation/index.md#rule-cap-35)). The RUML specification
does not prescribe a closed list.

### Symbolic Reference

The `ref` field contains a symbolic reference that is resolved by the tool at runtime.

**Tool Workflow:**

1. When loading the RUML file, the tool collects all actions with `ref`
2. The tool displays an overview: "The following actions need to be configured:"
3. For each `ref`, the tool enables assignment to a concrete implementation
4. The implementation details (email servers, API endpoints, etc.) are stored in the tool
   configuration, NOT in the RUML file

### Complete Example

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_annual_income": {
            "name": "Jahreseinkommen",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            }
          },
          "dp_applicant_email": {
            "name": "E-Mail des Antragstellers",
            "type": "email",
            "binding": {
              "type": "input"
            }
          },
          "dp_documents_complete": {
            "name": "Unterlagen vollständig",
            "type": "boolean",
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
    "title": "Förderantrag",
    "version": "1.0.0",
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
        "operator": "AND",
        "label": "Förderantrag",
        "children": ["2", "3"],
        "capabilities": [
          {
            "id": "ruml:actions",
            "payload": {
              "description": "Erstellt und versendet den Bescheid basierend auf dem Gesamtergebnis",
              "onTrue": {
                "operation": "createDocument",
                "ref": "document_service",
                "config": {
                  "template": "approval-letter",
                  "format": "pdf"
                }
              },
              "onFalse": {
                "operation": "sendNotification",
                "ref": "notification_service",
                "config": {
                  "recipient": "dp_applicant_email",
                  "template": "application-rejected",
                  "channel": "email"
                }
              },
              "onUndefined": {
                "operation": "requestDecision",
                "ref": "manual_review_workflow",
                "config": {
                  "recipient": "role:case-worker",
                  "deadline": "P3D",
                  "responseOptions": ["approve", "reject"]
                }
              }
            }
          }
        ]
      },
      "2": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Einkommensgrenze",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_annual_income < 50000"
            }
          }
        ]
      },
      "3": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "label": "Dokumentenprüfung",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_documents_complete = true"
            }
          }
        ]
      }
    }
  }
}
```

### Security Notes

- Recipients and endpoints are specified as symbolic references
- Concrete email addresses, API keys, or server URLs are stored in the tool configuration, NOT in
  the RUML file
- **Exception:** When a DataPoint is referenced as a recipient (e.g.,
  `"recipient": "dp_applicant_email"`), the value is obtained at runtime from the DataPoint

### Delivery via Sidecar (RUML-EXT)

```jsonc
{
  // ...
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "ruml:actions": {
        "onTrue": {
          "operation": "createDocument",
          "ref": "document_service",
          "config": {
            "template": "credit-approval",
            "format": "pdf"
          }
        }
      }
    }
  }
}
```

### Applicability

- `ruml:actions` MAY be used on any node type — Leaf-Nodes and Parent-Nodes ([`CAP-34`](../08-validation/index.md#rule-cap-34)).
- Actions only fire when the node was actually evaluated during traversal.

### Distinction Between Specification and Runtime

The RUML specification defines exclusively the declaration of actions — which action should be
triggered under which condition. Execution, assignment of result artifacts to the evaluation
process, error handling, and tracking are the responsibility of the runtime environment.
