<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.8 ruml:query

## 4.8 Capability `ruml:query`

### Overview

| Property               | Value                                                     |
| ---------------------- | --------------------------------------------------------- |
| **Capability ID**      | `ruml:query`                                              |
| **Scope**              | Node-Level (`capabilities` entry with `id: "ruml:query"`) |
| **Default `required`** | `false`                                                   |
| **Role**               | `decision`                                                |

This Capability defines data-based queries on Leaf-Nodes that determine their truth value. Queries
access DataPoints defined via the `ruml:datapoints` Capability (see
[Chapter 4.7](4-7-data-points.md)).

:::note[Distinction from other Capabilities]
For normative text references, `ruml:text-reference` is used (see
[Chapter 4.12](4-12-ruml-text-reference.md)). `ruml:query` covers exclusively data-based queries.
For AI-assisted decisions, the separate Capability `ruml:ai-query` is used (see
[Chapter 4.9](4-9-ruml-ai-query.md)).
:::

### Root-Level Declaration

To use `ruml:query`, the Capability MUST be declared in the root `capabilities` array
([`CAP-15`](../08-validation/index.md#rule-cap-15)):

```jsonc
"capabilities": [
  {
    "id": "ruml:query"
  }
]
```

**Note:** DataPoints are defined via the standalone `ruml:datapoints` Capability (see
[Chapter 4.7](4-7-data-points.md)). `ruml:query` accesses the data points defined there but does not
itself contain a `data` object.

### Node-Level Query

On Leaf-Nodes, the query is provided in the `capabilities` array of the node:

```jsonc
"1": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "label": "Einkommen ausreichend",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_annual_income > 50000"
      }
    }
  ]
}
```

#### Node-Level Query Fields

| **Field**     | **Type** | **Description**                                                                 |
| ------------- | -------- | ------------------------------------------------------------------------------- |
| `expression`  | String   | MUST contain a JSONata expression for computing the truth value ([`CAP-29`](../08-validation/index.md#rule-cap-29)) |
| `description` | String   | MAY contain a description of the query ([`CAP-29`](../08-validation/index.md#rule-cap-29))                          |

#### Expression Format

Expressions MUST be written in [JSONata](https://docs.jsonata.org/) 2.2.0.

The expression is evaluated against an input document: a JSON object that holds the value of each
DataPoint under the DataPoint's id. A DataPoint without a value has no entry.

A result of `true` or `false` is the status of the node. Any other result — including no result —
**MUST** yield status `undefined`.

```jsonc
"expression": "dp_annual_income > 50000"
```

### Evaluation Rules

- A node with a `ruml:query` entry in `capabilities` MUST NOT have a non-empty `children` array
- A node with a non-empty `children` array MUST NOT have a `ruml:query` entry in `capabilities`
  ([`CAP-07`](../08-validation/index.md#rule-cap-07))
- `ruml:query` determines the truth value of a Leaf-Node; Actions (the `ruml:actions` entry) react
  to the truth value — both are independent concepts
- All DataPoint IDs referenced in the expression MUST be defined in the `ruml:datapoints` Capability
  (referential integrity, [`DP-18`](../08-validation/index.md#rule-dp-18))

### Combination with Other Capabilities

A node can combine `ruml:query` with other Capabilities:

```jsonc
"1": {
  "id": "fcf02185-ffee-48a4-bf93-d2fb1b17944d",
  "label": "Einkommensprüfung",
  "capabilities": [
    {
      "id": "ruml:text-reference",
      "payload": {
        "refs": [
          {
            "id": "text_sgb_ii_11",
            "type": "refers-to"
          }
        ]
      }
    },
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
          "ref": "approval_service"
        },
        "onFalse": {
          "operation": "sendNotification",
          "ref": "rejection_service"
        }
      }
    }
  ]
}
```

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
            },
            "validation": {
              "required": true,
              "min": 0
            }
          },
          "dp_credit_score": {
            "name": "Bonitätsscore",
            "type": "number",
            "binding": {
              "type": "external",
              "ref": "schufa_api"
            }
          }
        }
      }
    },
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:text-reference",
      "payload": {
        "data": {
          "text_bgb_488": {
            "title": "§ 488 BGB – Darlehensvertrag",
            "uri": "/akn/de/act/1896-08-18/bgb#sec_488",
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "inForce",
            "type": "embedded",
            "text": "Durch den Darlehensvertrag wird der Darlehensgeber verpflichtet, dem Darlehensnehmer einen Geldbetrag in der vereinbarten Höhe zur Verfügung zu stellen. Der Darlehensnehmer ist verpflichtet, einen geschuldeten Zins zu zahlen und bei Fälligkeit das zur Verfügung gestellte Darlehen zurückzuzahlen."
          }
        }
      }
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
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
        "label": "Kreditprüfung",
        "capabilities": [
          {
            "id": "ruml:text-reference",
            "payload": {
              "refs": [
                {
                  "id": "text_bgb_488",
                  "type": "refers-to"
                }
              ]
            }
          }
        ],
        "children": ["2", "3"]
      },
      "2": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Einkommen ausreichend",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "description": "Mindesteinkommensgrenze",
              "expression": "dp_annual_income > 50000"
            }
          }
        ]
      },
      "3": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "label": "Bonität ausreichend",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_credit_score >= 600"
            }
          }
        ]
      }
    }
  }
}
```

### Delivery via RUML-EXT (Sidecar)

When `ruml:query` is delivered via a RUML-EXT file, the node-level queries are provided in the
`nodes` object (keyed by UUID):

```jsonc
{
  "$format": "RUML-EXT",
  "$specVersion": "1.0",
  "$base": {
    "id": "7812e8d0-bd75-437e-9c20-e4f8fb028ced",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "capabilities": [
    {
      "id": "ruml:query"
    }
  ],
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "ruml:query": {
        "expression": "dp_annual_income > 50000"
      }
    }
  }
}
```
