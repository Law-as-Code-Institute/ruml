<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.9 ruml:ai-query

## 4.9 Capability `ruml:ai-query`

### Overview

| Property               | Value                                         |
| ---------------------- | --------------------------------------------- |
| **Capability ID**      | `ruml:ai-query`                               |
| **Scope**              | Node-Level (`capabilities` field on the node) |
| **Default `required`** | `false`                                       |
| **Role**               | `decision`                                    |

The `ruml:ai-query` Capability extends Leaf-Nodes with LLM-based evaluation. The tree structure of
the Rulemap narrows the question to the point where the LLM answers a clearly defined check — the
result MUST be `true`, `false`, or `undefined`. The evaluation is not deterministic to the same
degree as a `ruml:query` expression, but through the narrowly scoped question and configurable
parameters (e.g., `temperature`), a high degree of reproducibility can be achieved.

When a node contains both `ruml:query` and `ruml:ai-query`, the `decisionMode` field on the node
determines how the results are combined (see [Chapter 4.3](4-3-capabilities-node-field.md)). In the
default mode `fallback`, `ruml:ai-query` is only executed when `ruml:query` returns `undefined`.

### Data Structure on the Node

The `payload` of the `ruml:ai-query` entry in a node's `capabilities` array has the following
structure:

```jsonc
"payload": {
  "model": "strong",
  "prompt": "Prüfe anhand der bereitgestellten Unterlagen, ob eine Härtefallbegründung plausibel ist. Antworte ausschließlich mit true, false oder undefined.",
  "description": "Prüft die Plausibilität der Härtefallbegründung",
  "inputs": {
    "context": [
      {
        "id": "ctx_guidelines",
        "role": "reference"
      },
      {
        "id": "ctx_gutachten",
        "role": "subject"
      }
    ],
    "dataPoints": ["dp_hardship_reason", "dp_annual_income"],
    "texts": ["text_bgb_823"]
  },
  "config": {
    "deterministic": true,
    "effort": "high",
    "temperature": 0.1
  }
}
```

### Fields

| **Field**     | **Type** | **Description**                                                                                                                                                            |
| ------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`       | String   | MUST contain a symbolic reference to the AI model to use ([`CAP-30`](../08-validation/index.md#rule-cap-30))                                                                                                   |
| `prompt`      | String   | MAY specify the prompt text inline in the RUML file. If present, this prompt is used — otherwise the tool-configured prompt template of the model is used ([`CAP-30`](../08-validation/index.md#rule-cap-30)). |
| `description` | String   | MAY describe the purpose of the AI query ([`CAP-30`](../08-validation/index.md#rule-cap-30))                                                                                                                   |
| `inputs`      | Object   | MAY define the input data for the LLM ([`CAP-30`](../08-validation/index.md#rule-cap-30))                                                                                                                      |
| `config`      | Object   | MAY contain configuration hints for execution ([`CAP-30`](../08-validation/index.md#rule-cap-30))                                                                                                              |

### inputs Object

| **Field**    | **Type**                | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `context`    | Array[String \| Object] | MAY specify IDs from the `ruml:context` Capability. Every id MUST be a key of the `data` of `ruml:context` ([`CTX-10`](../08-validation/index.md#rule-ctx-10)). As String: shorthand form (implicitly `role: "reference"`). As Object: `id` (MUST) and `role` (MAY, `"reference"` or `"subject"`, default: `"reference"`) ([`CAP-31`](../08-validation/index.md#rule-cap-31)). `"subject"` marks the document as the subject of examination for this query. **Note:** Context objects referenced with `role: "subject"` SHOULD have `subject: true` set in the context object itself (see [Chapter 4.11](4-11-ruml-context.md)). |
| `dataPoints` | Array[String]           | MAY specify DataPoint IDs whose values are passed to the LLM ([`CAP-31`](../08-validation/index.md#rule-cap-31)). Every id MUST be a key of the `data` of `ruml:datapoints` ([`DP-18`](../08-validation/index.md#rule-dp-18))                                                                                                                                                                                                                                                                                                                                                                                                   |
| `texts`      | Array[String]           | MAY specify IDs from the `ruml:text-reference` Capability (see [Chapter 4.12](4-12-ruml-text-reference.md)) ([`CAP-31`](../08-validation/index.md#rule-cap-31)). Every id MUST be a key of the `data` of `ruml:text-reference` ([`TXT-19`](../08-validation/index.md#rule-txt-19))                                                                                                                                                                                                                                                                                                                                               |

### config Object

| **Field**       | **Type** | **Description**                                                                                                                                                  |
| --------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `deterministic` | Boolean  | MAY indicate whether the same model and inputs should yield a consistent result ([`CAP-32`](../08-validation/index.md#rule-cap-32))                                                                  |
| `effort`        | String   | MAY indicate how much effort the model should spend on the query (`"low"`, `"medium"`, `"high"`), e.g. as reasoning effort. Default: `"medium"` ([`CAP-32`](../08-validation/index.md#rule-cap-32)). |
| `temperature`   | Number   | MAY specify the sampling temperature for the LLM (0.0-1.0) ([`CAP-32`](../08-validation/index.md#rule-cap-32)).                                                                                      |

### AI Model

The `model` field references the AI model (LLM) or class of models to use for the evaluation. The
allowed values and their meanings are tool-dependent and not part of this standard. The concrete
model associated with a value, the API endpoint, and the prompt template are stored in the tool
settings, **NOT** in the RUML file — unless the `prompt` field provides the prompt text directly
inline. In that case, the inline `prompt` takes precedence over the tool-configured template.

### Evaluation Rules

- A node MAY define both `ruml:query` and `ruml:ai-query` ([`CAP-33`](../08-validation/index.md#rule-cap-33))
- When multiple `decision` Capabilities are present on the node, `decisionMode` determines the
  combination logic (see [Chapter 4.3](4-3-capabilities-node-field.md))
- The LLM MUST return a result of `true`, `false`, or `undefined`
- For `undefined` (undecidable), `ruml:actions` with `onUndefined` SHOULD be combined

### Example — Complete Node

```jsonc
"3": {
  "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
  "label": "Begründung plausibel",
  "capabilities": [
    {
      "id": "ruml:ai-query",
      "payload": {
        "model": "strong",
        "prompt": "Prüfe anhand der bereitgestellten Unterlagen, ob eine Härtefallbegründung plausibel ist. Antworte ausschließlich mit true, false oder undefined.",
        "description": "Prüft die Plausibilität der Härtefallbegründung anhand der Richtlinien und Beispielfälle",
        "inputs": {
          "context": [
            "ctx_guidelines",
            "ctx_bsg_ruling",
            "ctx_example_approved_medical",
            "ctx_example_rejected_luxury"
          ],
          "dataPoints": ["dp_hardship_reason", "dp_annual_income"]
        },
        "config": {
          "deterministic": true,
          "effort": "high",
          "temperature": 0.1
        }
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "onUndefined": {
          "operation": "requestDecision",
          "ref": "manual_review_workflow",
          "config": {
            "recipient": "role:social-worker",
            "deadline": "P5D",
            "responseOptions": ["approve", "reject", "requestMoreInfo"]
          }
        }
      }
    }
  ]
}
```

### Root-Level Declaration

To use `ruml:ai-query` in a RUML file, the Capability MUST be declared in the root `capabilities`
array ([`CAP-15`](../08-validation/index.md#rule-cap-15)). The optional `config` field MAY contain a global `systemPrompt` that is used
for all AI query executions in this file:

```jsonc
"capabilities": [
  {
    "id": "ruml:ai-query",
    "payload": {
      "config": {
        "systemPrompt": "Du bist ein rechtlicher Assistent. Analysiere die bereitgestellten Sachverhalte anhand der geltenden deutschen Rechtslage und antworte ausschließlich mit true, false oder undefined."
      }
    }
  }
]
```

| Field          | Type   | Description                                                                                                                                                                                                                                                    |
| -------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `systemPrompt` | String | MAY define a global system prompt that applies to all `ruml:ai-query` executions in this file. When a node additionally has a `prompt` field, the `systemPrompt` is passed as the system role and the node-specific `prompt` as the user role ([`CAP-32`](../08-validation/index.md#rule-cap-32)). |
