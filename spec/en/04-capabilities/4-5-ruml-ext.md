<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.5 RUML-EXT Format

### Overview

The RUML-EXT format defines a **sidecar file** that stores capability extension data separately from
the original RUML file. It supplements the inline method described in [Chapter 4.1](4-1-concept.md)
with the sidecar mode.

- **File extension:** `.ruml-ext`
- **Format identification:** `$format: "RUML-EXT"`
- **Purpose:** Transport of `capabilities` data without modification of the original RUML file
- **Schema:** [`ruml-ext.schema.json`](../../../schemas/ruml-ext.schema.json)
  ([draft 2020-12](https://json-schema.org/draft/2020-12))

### Root Object Structure

A RUML-EXT file MUST contain the following required fields:

```jsonc
{
  "$format": "RUML-EXT",
  "$specVersion": "1.0",
  "$base": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "capabilities": [/* ... */],
  "nodes": {/* ... */}
}
```

| Field          | Type   | Required | Description                                                                                                                                                  |
| -------------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `$format`      | String | MUST     | MUST have the value `"RUML-EXT"`                                                                                                                             |
| `$specVersion` | String | MUST     | Same versioning rules as RUML (see [Chapter 2.3](../02-file-format-basics/2-3-versioning.md))                                                                |
| `$base`        | Object | MUST     | Reference to the base RUML file (see below)                                                                                                                  |
| `capabilities` | Array  | MUST     | The capabilities whose data is contained in this EXT file — a list of entries as in [Chapter 4.2](4-2-capabilities-field.md), whose order is not significant |
| `nodes`        | Object | MUST     | Extension data indexed by UUIDs                                                                                                                              |

A parser MUST verify that `$format` has the value `"RUML-EXT"` before it processes the EXT file any
further ([`CAP-22`](../08-validation/index.md#rule-cap-22)).

The root object of a RUML-EXT file MUST NOT contain the fields `metadata` and `rulemap` — they are
reserved exclusively for the base RUML file ([`CAP-23`](../08-validation/index.md#rule-cap-23)). A parser MUST treat the presence of
either field as a validation error. `evaluation` is not an EXT root field either — it belongs to
RUML result files (`.ruml-result`) — but it is not part of the [`CAP-23`](../08-validation/index.md#rule-cap-23) check.

Root-level artifact data is NOT transported as separate root fields of the EXT file, but via the
`payload.data` field of the respective entry in the `capabilities` array (see
[Chapter 4.2](4-2-capabilities-field.md)).

### The `$base` Field

```jsonc
"$base": {
  "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
  "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
}
```

| Field  | Type   | Required | Description                                                                                                                                                    |
| ------ | ------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`   | UUID   | MUST     | The `metadata.id` of the base RUML file. MUST conform to the UUID v4 format (pattern `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`). |
| `hash` | String | MUST     | The hash of the base RUML file at the time this EXT file was created.                                                                                          |

The hash MUST be computed over the canonical form of the base RUML file according to the container
hashing rules ([Chapter 2.4](../02-file-format-basics/2-4-integrity.md),
[Chapter 7.3](../07-container/7-3-hashing.md)). It identifies the **exact version** of the base file
that the EXT file refers to.

### Hash Verification

Before a parser merges extension data from a RUML-EXT file with a RUML file, it MUST perform the
following steps ([`CAP-24`](../08-validation/index.md#rule-cap-24)):

1. **ID matching:** The `$base.id` of the EXT file MUST match the `metadata.id` of the RUML file.
2. **Hash verification:** The current hash of the RUML file MUST match the `$base.hash` of the EXT
   file.
3. **If the hash does not match:** The parser MUST abort the merge and emit an error.

A parser MUST NOT skip this hash comparison — not even in development environments or with an
explicit user override, unless the specification defines an exception ([`CAP-25`](../08-validation/index.md#rule-cap-25)).

:::warning[Outdated EXT File]
If the base RUML file has been modified since the EXT file was created, the hash will no longer
match. The parser MUST reject the merge in this case. Silently merging outdated extension data would
lead to inconsistent states.
:::

### The `nodes` Object in RUML-EXT

The extension data in the `nodes` object is indexed by **UUIDs** (not LexIDs). This is necessary
because LexIDs are not uniquely position-addressable for modular nodes, whereas UUIDs are globally
unique.

```jsonc
"nodes": {
  "0eb360a6-626a-406d-89a1-9f434ced141b": {
    "com.example/review-notes": {
      "status": "approved",
      "reviewer": "rechtsabteilung"
    }
    // ...
  },
  "8fc54c7d-7f60-410e-9493-4f1eecfb1af8": {
    "com.example/review-notes": {
      "status": "pending"
    }
  }
  // ...
}
```

- **Key:** A valid UUID that exists in the `nodes` object of the base RUML file (the node's `id`
  field value).
- **Value:** An object whose keys are capability IDs from the `capabilities` array of the EXT file.

#### Unknown UUID References

If a UUID in the `nodes` object of the EXT file does not correspond to any node in the base RUML
file, the parser MUST treat this as an error ([`CAP-26`](../08-validation/index.md#rule-cap-26)). This prevents silent data phantoms
(extension data for non-existent nodes).

### Complete Example

**Base RUML file** (`pruefung-volljährigkeit.ruml`):

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_age": {
            "name": "Alter",
            "type": "integer",
            "binding": {
              "type": "input"
            }
          },
          "dp_competent": {
            "name": "Geschäftsfähig",
            "type": "boolean",
            "binding": {
              "type": "input"
            }
          }
        }
      }
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.2.0",
    "created": "2024-01-15T09:00:00Z",
    "modified": "2024-03-20T14:30:00Z",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "operator": "AND",
        "label": "Geschäftsfähigkeit",
        "children": ["2", "3"]
      },
      "2": {
        "id": "8fc54c7d-7f60-410e-9493-4f1eecfb1af8",
        "label": "Volljährigkeit",
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
        "id": "56b5b9db-b791-4fe5-abb0-a05cb0847db6",
        "label": "Keine Entmündigung",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_competent = true"
            }
          }
        ]
      }
    }
  }
}
```

**RUML-EXT Sidecar** (`pruefung-volljährigkeit.ruml-ext`):

```jsonc
{
  "$format": "RUML-EXT",
  "$specVersion": "1.0",
  "$base": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "capabilities": [
    {
      "id": "com.example/review-notes",
      "role": "data"
    },
    {
      "id": "com.example/priority",
      "role": "data"
    }
  ],
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "com.example/review-notes": {
        "status": "approved",
        "reviewer": "rechtsabteilung"
      },
      "com.example/priority": {
        "level": "high"
      }
    },
    "8fc54c7d-7f60-410e-9493-4f1eecfb1af8": {
      "com.example/review-notes": {
        "status": "pending"
      }
    },
    "56b5b9db-b791-4fe5-abb0-a05cb0847db6": {
      "com.example/review-notes": {
        "status": "approved",
        "reviewer": "rechtsabteilung"
      },
      "com.example/priority": {
        "level": "low"
      }
    }
  }
}
```

### Relationship to the Inline Method

It is not permitted to define the same capability for the same node both inline (in the
`capabilities` field) and in an EXT file simultaneously. During a merge, the parser MUST check
whether a conflict exists and treat it as an error ([`CAP-27`](../08-validation/index.md#rule-cap-27)). Silent overwriting or merging
MUST NOT occur.

### Multiple EXT Files for One RUML File

There MAY be multiple EXT files referencing the same base RUML file — e.g., one EXT file per
capability provider. Each EXT file MUST be verified independently. Conflicts between EXT files (same
capability on the same node in two different EXT files) MUST be treated as errors ([`CAP-27`](../08-validation/index.md#rule-cap-27)).
