<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.11 ruml:context

## 4.11 Capability `ruml:context`

### Overview

| Property               | Value                                             |
| ---------------------- | ------------------------------------------------- |
| **Capability ID**      | `ruml:context`                                    |
| **Scope**              | Root-Level (`data`) + Node-Level                  |
| **Default `required`** | `false`                                           |
| **Node-Level**         | `payload.refs` of the node's `ruml:context` entry |
| **Role**               | `data`                                            |

This Capability provides context materials that are relevant for the evaluation and application of
the Rulemap. Two fundamentally different roles are distinguished:

**Reference material** (`subject: false`, default) — Background knowledge associated with the
Rulemap: court decisions, commentaries, administrative directives, guidelines, example cases.
Reference material is part of the Rulemap or its sidecar files and remains the same across all
evaluation processes.

**Subject of examination** (`subject: true`) — A document that is itself the object being assessed
in at least one evaluation: an expert opinion to be evaluated, an application or notice under
review, evidence such as photos or documents. Unlike reference material, subject documents are
typically supplied per evaluation rather than being fixed in the Rulemap.

The role assignment occurs in two places:

- On the **context object** itself: `subject: true` signals that this document serves as the subject
  of examination in at least one place
- In the **`inputs.context` reference** of a `ruml:ai-query`: `role: "subject"` or
  `role: "reference"` determines in which role the document is used for this specific query (see
  [Chapter 4.9](4-9-ruml-ai-query.md))

### Use Cases

**As reference material:**

- Court decisions and precedents for interpreting regulations
- Legal commentaries and specialist literature
- Administrative directives and guidelines
- Example and model cases for AI queries
- Historical development of a regulation
- Linked Rulemaps for detailed checks

**As subject of examination:**

- Expert opinions that are to be evaluated substantively
- Applications and notices for review
- Photos, screenshots, or documents as evidence
- Reports and statements as a basis for decisions

### Provision via Capability

Context objects are provided via the `ruml:context` Capability — either inline in the `capabilities`
array or via a RUML-EXT sidecar file:

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:context",
      "payload": {
        "data": {
          "ctx_bgh_2024": {
            "title": "BGH zur Auslegung des Wohnsitzbegriffs",
            "category": "courtDecision"
            // ...
          },
          "ctx_example_approved": {
            "title": "Beispiel: Genehmigter Härtefall",
            "category": "example"
            // ...
          }
        }
      }
    }
  ],
  "metadata": {/* ... */},
  "rulemap": {/* ... */}
}
```

### Basic Structure

```jsonc
"ctx_bgh_2024": {
  "title": "BGH zur Auslegung des Wohnsitzbegriffs",
  "category": "courtDecision",
  "type": "url",
  "timestamp": "2024-01-15T10:00:00Z",
  // ...
  "metadata": {/* ... */},
  "content": {/* ... */},
  "source": {/* ... */}
}
```

### Required Fields

| **Field**                                                                                                                                                                                                                | **Type** | **Description**                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------ |
| `title`                                                                                                                                                                                                                  | String   | MUST have a title ([`CTX-01`](../08-validation/index.md#rule-ctx-01)).                                                                           |
| `category`                                                                                                                                                                                                               | Enum     | MUST be one of the defined categories (see below) ([`CTX-01`](../08-validation/index.md#rule-ctx-01), [`CTX-02`](../08-validation/index.md#rule-ctx-02)).                            |
| `timestamp`                                                                                                                                                                                                              | DateTime | MUST specify the modification time of the context as an RFC 3339 `date-time` ([`CTX-01`](../08-validation/index.md#rule-ctx-01), [`CTX-03`](../08-validation/index.md#rule-ctx-03)). |
| **Note:** The object key (e.g., `"ctx_bgh_2024"`) serves as the identifier (see [Chapter 3.2.6](../03-data-model/3-2-data-types-and-formats.md)). Context IDs MUST match the pattern `[a-z_][a-z0-9_]*` ([`CTX-04`](../08-validation/index.md#rule-ctx-04)). |

Context objects are defined at root level in the `data` field of the capability entry — this is the
pool of available context. They are not bound to nodes at the point of definition.

#### Binding Context to Nodes

A node references the context objects it uses via the `refs` array in the `payload` of its
node-level `ruml:context` entry, analogous to `payload.refs` of the `ruml:text-reference` entry (see
[Chapter 4.3](4-3-capabilities-node-field.md)). The same context id MUST NOT appear more than once
in a node's `refs` ([`CTX-05`](../08-validation/index.md#rule-ctx-05)).

```jsonc
"2": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "label": "Einkommensgrenze unterschritten",
  "capabilities": [
    {
      "id": "ruml:context",
      "payload": {
        "refs": ["ctx_bgh_2024", "ctx_guidelines"]
      }
    }
  ]
}
```

### Optional Fields

| **Field**       | **Type** | **Description**                                                                                                                                                                                                                                                                             |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`          | Enum     | MAY specify the embedding type: `embedded`, `container`, `url`, `external`. Default: `embedded`. Set explicitly for `container`, `url`, or `external` entries ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                              |
| `subject`       | Boolean  | MAY indicate that this document serves as the subject of examination in at least one place (see role distinction above). Default: `false` ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                  |
| `metadata`      | Object   | MAY contain additional category-specific metadata ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                                                                                                          |
| `content`       | Object   | MAY contain the payload and/or a summary. Open object — its internal structure is flexible (see [Content Object](#content-object)) ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                         |
| `source`        | Object   | MAY contain source references ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                                                                                                                              |
| `url`           | String   | MUST contain the URL of the document when `type: "url"` ([`CTX-07`](../08-validation/index.md#rule-ctx-07)).                                                                                                                                                                                                                    |
| `containerPath` | String   | MUST specify the path in the container when `type: "container"` ([`CTX-07`](../08-validation/index.md#rule-ctx-07)).                                                                                                                                                                                                            |
| `ref`           | String   | MUST contain a symbolic reference when `type: "external"` ([`CTX-07`](../08-validation/index.md#rule-ctx-07)).                                                                                                                                                                                                                  |
| `hash`          | String   | MAY contain an integrity hash of the referenced file/document, on entries of any `type` (typically `container` or `url`) ([`CTX-06`](../08-validation/index.md#rule-ctx-06)). MUST have the form `<algorithm>:<hex>`: the algorithm `sha3-256`, `sha256` or `blake3`, then 64 lowercase hexadecimal characters ([`CTX-08`](../08-validation/index.md#rule-ctx-08)). |
| `accessDate`    | Date     | MAY specify the date the source was last accessed, as an ISO 8601 date (`YYYY-MM-DD`). Permitted on entries of any `type`, typically `url` ([`CTX-03`](../08-validation/index.md#rule-ctx-03), [`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                  |

### 4.11.1 Context Categories

Context objects are categorized by their content type via the `category` field.

`metadata` is an open object — RUML prescribes no specific keys per category. Any values that are
present SHOULD conform to the RUML data types (see
[Chapter 3.2](../03-data-model/3-2-data-types-and-formats.md)); beyond that, how metadata is
validated is implementation-defined. The examples below illustrate keys that are commonly used, but
none are required.

### Predefined Categories

| **Category**             | **Description**                                                                                                      |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `courtDecision`          | Court decision / precedent                                                                                           |
| `commentary`             | Legal commentary                                                                                                     |
| `administrativeGuidance` | Administrative directive / guideline                                                                                 |
| `explanatoryMemorandum`  | Legislative explanatory memorandum (Gesetzesbegründung) — primary interpretive material from the legislative process |
| `example`                | Example / model case                                                                                                 |
| `literature`             | Specialist literature / article                                                                                      |
| `faq`                    | Frequently asked questions                                                                                           |
| `history`                | Historical development                                                                                               |
| `rulemap`                | Linked RUML file                                                                                                     |
| `custom`                 | User-defined                                                                                                         |

### Examples by Category

**courtDecision:**

```jsonc
"ctx_bgh_2024": {
  "title": "BGH zur Auslegung des Wohnsitzbegriffs",
  "category": "courtDecision",
  "type": "url",
  "timestamp": "2024-01-15T10:00:00Z",
  "url": "https://www.bundesgerichtshof.de/2024/123",
  "metadata": {
    "court": "BGH",
    "reference": "I ZR 123/23",
    "date": "2024-01-01"
  },
  "content": {
    "summary": "Präzisierung des Wohnsitzbegriffs bei Auslandsbezug"
  },
  "source": {
    "citation": "BGH, Urt. v. 1.1.2024 - I ZR 123/23",
    "url": "https://www.bundesgerichtshof.de/2024/123",
    "publication": "NJW 2024, 456"
  }
}
```

**commentary:**

```jsonc
"ctx_palandt_823": {
  "title": "Palandt zu § 823 BGB",
  "category": "commentary",
  "type": "external",
  "timestamp": "2024-01-01T00:00:00Z",
  "metadata": {
    "author": "Sprau",
    "publication": "Palandt BGB Kommentar",
    "edition": "83. Auflage 2024"
  },
  "ref": "legal_database_palandt",
  "source": {
    "citation": "Palandt/Sprau, § 823 Rn. 15-20",
    "license": "Copyright"
  }
}
```

**administrativeGuidance:**

```jsonc
"ctx_bmf_income_tax": {
  "title": "BMF-Schreiben zur Einkommensteuer",
  "category": "administrativeGuidance",
  "type": "url",
  "timestamp": "2024-01-01T00:00:00Z",
  "metadata": {
    "authority": "Bundesministerium der Finanzen",
    "reference": "IV C 2 - S 2400/19/10001",
    "validFrom": "2024-01-01"
  },
  "url": "https://www.bundesfinanzministerium.de/bmf-schreiben/2024-01-01-einkommensteuer",
  "source": {
    "citation": "BMF-Schreiben v. 1.1.2024, IV C 2 - S 2400/19/10001",
    "license": "Public Domain"
  }
}
```

**example:**

```jsonc
"ctx_example_approved": {
  "title": "Beispiel: Genehmigter Härtefall",
  "category": "example",
  "type": "embedded",
  "timestamp": "2024-01-01T00:00:00Z",
  "content": {
    "text": "Fall: Alleinerziehende Mutter, zwei Kinder, Jahreseinkommen 18.000 EUR. Begründung: Unvorhergesehene Krankheitskosten. Entscheidung: Genehmigt.",
    "summary": "Genehmigung aufgrund unvorhergesehener Krankheitskosten"
  }
}
```

**rulemap:**

```jsonc
"ctx_rulemap_residence": {
  "title": "Detailprüfung Wohnsitzbegriff",
  "category": "rulemap",
  "type": "external",
  "timestamp": "2024-01-01T00:00:00Z",
  "metadata": {
    "rulemapId": "043fdfce-d617-4a76-af40-e02de43c07b8",
    "rulemapHash": "sha3-256:ed73f1144536b4be0eaa8d8dcc82bbfacbca02ca3bea57b4dc8b5c67484b5c0f",
    "relationship": "extends",
    "description": "Vertiefende Prüfung für Sonderfälle"
  },
  "ref": "rulemap_repository"
}
```

### Relationship Types for Linked Rulemaps

| **Relationship** | **Description**                 |
| ---------------- | ------------------------------- |
| `extends`        | Extends this Rulemap            |
| `replaces`       | Replaces an older version       |
| `references`     | References a related regulation |
| `depends`        | Requires this Rulemap           |
| `conflicts`      | Conflicts with this Rulemap     |

### 4.11.2 Content Types

The `type` field defines how the context content is embedded. RUML supports four embedding types.
`type` is optional and defaults to `embedded` (see [Optional Fields](#optional-fields)).

| **Type**    | **Description**                      | **Usage**                        |
| ----------- | ------------------------------------ | -------------------------------- |
| `embedded`  | Embedded directly in the RUML file   | Short texts, examples, summaries |
| `container` | Embedded in the RUML container (ZIP) | PDF documents, extensive texts   |
| `url`       | External URL                         | Public documents, legal texts    |
| `external`  | Symbolic reference                   | Databases, APIs, local files     |

### Type: embedded

The content is stored directly in the `content` object of the RUML file.

```jsonc
"ctx_example_rejected": {
  "title": "Beispiel: Abgelehnter Härtefall",
  "category": "example",
  "type": "embedded",
  "timestamp": "2024-01-01T00:00:00Z",
  "content": {
    "text": "Fall: Einzelperson, Jahreseinkommen 45.000 EUR. Begründung: Urlaubsreise geplant. Entscheidung: Abgelehnt, da keine Härte erkennbar.",
    "summary": "Ablehnung mangels Härtefall-Kriterien"
  }
}
```

**Content object** {#content-object}

`content` is an **open object** — its internal structure is flexible and not constrained by RUML.
The examples in this chapter use `text` (the embedded payload) and `summary`; `media`
(Base64-encoded) is also common. Any other structure is permitted.

**Recommendation:** Use `type: "embedded"` for texts under 10,000 characters and small media under 1
MB.

### Type: container

The content is stored as a separate file in the RUML container (see
[Chapter 7](../07-container/index.md) for the complete container specification).

```jsonc
"ctx_bgh_judgment_pdf": {
  "title": "BGH-Urteil I ZR 123/23",
  "category": "courtDecision",
  "type": "container",
  "timestamp": "2024-01-15T10:00:00Z",
  "containerPath": ".context/BGH-I-ZR-123-23.pdf",
  "hash": "sha3-256:49ebbe3e80b9c4ad2cb32540c4b052017d346b2306e75bf669d1dfc281cdaf6d",
  "content": {
    "summary": "Präzisierung des Wohnsitzbegriffs bei Auslandsbezug"
  },
  "metadata": {
    "court": "BGH",
    "reference": "I ZR 123/23",
    "date": "2024-01-01"
  }
}
```

**Fields for container:**

| **Field**       | **Type** | **Description**                                                                                     |
| --------------- | -------- | --------------------------------------------------------------------------------------------------- |
| `containerPath` | String   | MUST specify the path in the container. MUST start with `.context/` ([`CTX-07`](../08-validation/index.md#rule-ctx-07), [`CTX-09`](../08-validation/index.md#rule-ctx-09)). |
| `hash`          | String   | MAY contain the file hash for integrity verification.                                               |

### Type: url

The content is referenced via an external URL.

```jsonc
"ctx_estg_32a": {
  "title": "§ 32a EStG - Einkommensteuertarif",
  "category": "administrativeGuidance",
  "type": "url",
  "timestamp": "2024-01-01T00:00:00Z",
  "url": "https://www.gesetze-im-internet.de/estg/__32a.html",
  "hash": "sha3-256:877998158956cc7b189ce0906e3b6c30cf2cc27e6d8d3dc3170460389d610b5b",
  "content": {
    "summary": "Grundtarif der Einkommensteuer"
  },
  "source": {
    "citation": "§ 32a EStG",
    "license": "Public Domain"
  }
}
```

**Required fields for url:**

| **Field** | **Type** | **Description**                                          |
| --------- | -------- | -------------------------------------------------------- |
| `url`     | String   | MUST contain a valid URL ([`CTX-03`](../08-validation/index.md#rule-ctx-03), [`CTX-07`](../08-validation/index.md#rule-ctx-07)). |

**Optional fields for url:**

| **Field**    | **Type** | **Description**                                           |
| ------------ | -------- | --------------------------------------------------------- |
| `hash`       | String   | MAY contain the document hash for integrity verification. |
| `accessDate` | Date     | MAY specify the date of last access.                      |

**Note:** For `type: "url"`, the tool SHOULD load and cache the content at runtime. The optional
`hash` enables checking whether the content has changed.

### Type: external

The content is obtained via a symbolic reference that is resolved by the tool at runtime.

```jsonc
"ctx_internal_guidelines": {
  "title": "Interne Bearbeitungsrichtlinien",
  "category": "administrativeGuidance",
  "type": "external",
  "timestamp": "2024-01-01T00:00:00Z",
  "ref": "internal_knowledge_base",
  "content": {
    "summary": "Richtlinien für die Sachbearbeitung"
  }
}
```

**Required fields for external:**

| **Field** | **Type** | **Description**                                    |
| --------- | -------- | -------------------------------------------------- |
| `ref`     | String   | MUST contain a symbolic reference ([`CTX-07`](../08-validation/index.md#rule-ctx-07)). |

**Tool Workflow:**

1. When loading the RUML file, the tool collects all context objects with `type: "external"`
2. The tool displays an overview: "The following context sources need to be configured:"
3. For each `ref`, the tool enables assignment to a concrete data source
4. The connection details are stored in the tool configuration, NOT in the RUML file

**Use cases for external:**

- Internal knowledge bases
- Proprietary document servers
- Dynamic content from APIs
- Local file systems

### 4.11.3 Source References and Licenses

The optional `source` object documents the origin of the context content and its usage rights.

### Source Object Structure

```jsonc
"ctx_commentary_823": {
  "title": "Kommentar zu § 823 BGB",
  "category": "commentary",
  "type": "external",
  "timestamp": "2024-01-01T00:00:00Z",
  "ref": "legal_database",
  "source": {
    "citation": "Palandt/Sprau, § 823 Rn. 15-20",
    "author": "Sprau, Hartwig",
    "publication": "Palandt BGB Kommentar, 83. Auflage",
    "url": "https://beck-online.de/palandt-bgb/823",
    "isbn": "978-3-406-12345-6",
    "doi": "10.1234/example.doi",
    "accessDate": "2024-06-01",
    "license": "Copyright",
    "note": "Nur Zitate nach § 51 UrhG erlaubt"
  }
}
```

### Source Fields

`source` is an **open object** with a flexible structure. The example above shows the common keys
(`citation`, `author`, `publication`, `url`, `isbn`, `doi`, `accessDate`, `license`, `note`); any
other keys are permitted. Of these, only `license` carries defined semantics — see
[Licenses](#licenses) below.

### Licenses

The `license` field documents the usage rights of the embedded material. This is critical for the
legally compliant use of copyrighted material.

`license` is a **free-form string**, not a closed enumeration — proprietary or custom license
identifiers are permitted. The values below are a recommended vocabulary that tools SHOULD
recognize. A value of `null` is explicitly valid and signals an unknown or unclear legal status,
which tools MUST treat conservatively (see [Recommendations for Tools](#recommendations-for-tools)).

**Common licenses and their meaning:**

| **License**       | **Meaning**               | **Permitted Use in RUML**                          |
| ----------------- | ------------------------- | -------------------------------------------------- |
| `"Public Domain"` | Public domain             | Full embedding permitted                           |
| `"CC0"`           | Waiver of all rights      | Full embedding permitted                           |
| `"CC-BY-4.0"`     | Attribution required      | Embedding with source reference                    |
| `"CC-BY-SA-4.0"`  | Attribution + share-alike | Embedding, RUML must have the same license         |
| `"CC-BY-NC-4.0"`  | Non-commercial            | Only for non-commercial RUML                       |
| `"Copyright"`     | All rights reserved       | Only citations within the scope of citation rights |
| `"Proprietary"`   | Proprietary/Protected     | Only with explicit permission                      |

### Examples of Source References

**Court decision (usually public domain):**

```jsonc
"source": {
  "citation": "BGH, Urt. v. 1.1.2024 - I ZR 123/23",
  "url": "https://www.bundesgerichtshof.de/2024/123",
  "publication": "NJW 2024, 456",
  "license": "Public Domain",
  "note": "Amtliche Werke nach § 5 UrhG gemeinfrei"
}
```

**Commentary literature (protected):**

```jsonc
"source": {
  "citation": "Palandt/Sprau, § 823 Rn. 15",
  "author": "Sprau, Hartwig",
  "publication": "Beck Verlag 2024",
  "isbn": "978-3-406-12345-6",
  "license": "Copyright",
  "note": "Nur Zitate nach § 51 UrhG erlaubt"
}
```

**Open access article:**

```jsonc
"source": {
  "citation": "Müller, Digitale Verwaltung, JurPC 2024",
  "author": "Müller, Klaus",
  "doi": "10.1234/jurpc.2024.123",
  "url": "https://www.jurpc.de/2024/123",
  "license": "CC-BY-4.0",
  "note": "Volltext-Einbindung mit Namensnennung erlaubt"
}
```

**Administrative directive:**

```jsonc
"source": {
  "citation": "BMF-Schreiben v. 1.1.2024, IV C 2 - S 2400/19/10001",
  "url": "https://www.bundesfinanzministerium.de/bmf-schreiben/2024-01-01-einkommensteuer",
  "license": "Public Domain",
  "note": "Amtliches Werk"
}
```

**Unclear legal status:**

```jsonc
"source": {
  "citation": "Historisches Dokument von 1950",
  "license": null,
  "note": "Urheberrechtsstatus unklar - Vorsicht bei Verwendung"
}
```

### Source References

The `source` object is optional. Provide it wherever attribution or licensing matters — in
particular for third-party material such as commentary or literature, where a `license` makes the
usage rights explicit.

### Recommendations for Tools

Based on the license, tools SHOULD:

| **License**                      | **Tool Behavior**                       |
| -------------------------------- | --------------------------------------- |
| Open License (CC, Public Domain) | Display full text, allow editing        |
| Copyright/Proprietary            | Only summary/citations, display warning |
| License missing/unclear          | Display warning, treat conservatively   |

**Important note:** Specifying an open license in the RUML file does NOT replace verification of the
actual legal situation. Creators of RUML files are themselves responsible for the legally compliant
use of third-party material.

### 4.11.4 Complete Example

The following example shows a RUML file with various context types that are referenced in an AI
query:

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:context",
      "payload": {
        "data": {
          "ctx_guidelines": {
            "title": "Richtlinien zur Härtefallprüfung",
            "category": "administrativeGuidance",
            "type": "url",
            "timestamp": "2024-01-01T00:00:00Z",
            "url": "https://www.example.gov/haertefall-richtlinien.pdf",
            "hash": "sha3-256:bd7a69bf084c64d738739cff1a68a9949802e82c83314fd1b93c3ce58a028afb",
            "metadata": {
              "authority": "Bundesministerium für Soziales",
              "reference": "BMSoz-2024-001",
              "validFrom": "2024-01-01"
            },
            "content": {
              "summary": "Offizielle Richtlinien für die Beurteilung von Härtefällen"
            },
            "source": {
              "citation": "BMSoz-Richtlinie v. 1.1.2024",
              "license": "Public Domain"
            }
          },
          "ctx_bsg_ruling": {
            "title": "BSG zur Auslegung des Härtefallbegriffs",
            "category": "courtDecision",
            "type": "container",
            "timestamp": "2023-06-15T10:00:00Z",
            "containerPath": ".context/BSG-B-14-AS-123-22.pdf",
            "hash": "sha3-256:d70cff10ab78f18281549cf0c0daf5a13370b8142797be951e75c5f74c5f0eef",
            "metadata": {
              "court": "BSG",
              "reference": "B 14 AS 123/22",
              "date": "2023-06-15"
            },
            "content": {
              "summary": "Grundsatzurteil zur Auslegung des Härtefallbegriffs im Sozialrecht"
            },
            "source": {
              "citation": "BSG, Urt. v. 15.6.2023 - B 14 AS 123/22",
              "publication": "BSGE 135, 123",
              "license": "Public Domain"
            }
          },
          "ctx_example_approved_medical": {
            "title": "Beispiel: Genehmigt - Medizinische Notlage",
            "category": "example",
            "type": "embedded",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
              "text": "Fall: Alleinerziehende Mutter, zwei Kinder (4 und 7 Jahre), Jahreseinkommen 18.000 EUR. Begründung: Unvorhergesehene Krankheitskosten nach Unfall des älteren Kindes, Zuzahlungen für Rehabilitation. Entscheidung: Genehmigt. Begründung: Unvorhersehbarkeit der Kosten, nachgewiesene finanzielle Belastung, soziale Verantwortung für Kinder.",
              "summary": "Genehmigung aufgrund unvorhergesehener medizinischer Kosten"
            }
          },
          "ctx_example_approved_job_loss": {
            "title": "Beispiel: Genehmigt - Arbeitsplatzverlust",
            "category": "example",
            "type": "embedded",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
              "text": "Fall: Einzelperson, 52 Jahre, vorheriges Jahreseinkommen 42.000 EUR, aktuell arbeitslos. Begründung: Betriebsbedingte Kündigung nach 20 Jahren, schwierige Arbeitsmarktlage in der Region. Entscheidung: Genehmigt. Begründung: Unverschuldeter Arbeitsplatzverlust, fortgeschrittenes Alter erschwert Neuanstellung.",
              "summary": "Genehmigung aufgrund unverschuldeten Arbeitsplatzverlusts"
            }
          },
          "ctx_example_rejected_luxury": {
            "title": "Beispiel: Abgelehnt - Freiwillige Ausgaben",
            "category": "example",
            "type": "embedded",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
              "text": "Fall: Einzelperson, Jahreseinkommen 45.000 EUR. Begründung: Finanzielle Engpässe nach Kauf eines Neuwagens und geplanter Urlaubsreise. Entscheidung: Abgelehnt. Begründung: Selbstverschuldete Situation durch freiwillige Luxusausgaben, keine unvorhersehbare Notlage.",
              "summary": "Ablehnung aufgrund selbstverschuldeter Situation"
            }
          },
          "ctx_example_rejected_income": {
            "title": "Beispiel: Abgelehnt - Einkommen zu hoch",
            "category": "example",
            "type": "embedded",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
              "text": "Fall: Ehepaar, gemeinsames Jahreseinkommen 85.000 EUR. Begründung: Hohe Kreditraten für Eigenheim. Entscheidung: Abgelehnt. Begründung: Einkommen deutlich über Härtefallgrenze, Kreditverpflichtungen waren vorhersehbar und freiwillig eingegangen.",
              "summary": "Ablehnung aufgrund zu hohen Einkommens"
            }
          }
        }
      }
    },
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_hardship_reason": {
            "name": "Härtefallbegründung",
            "type": "string",
            "binding": {
              "type": "input",
              "hint": "Bitte beschreiben Sie Ihre besondere Situation"
            },
            "validation": {
              "required": true,
              "minLength": 50,
              "maxLength": 2000
            }
          },
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
          }
        }
      }
    },
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:ai-query"
    },
    {
      "id": "ruml:actions"
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "created": "2024-01-01T12:00:00+01:00",
    "modified": "2024-01-15T14:30:00+01:00",
    "status": "draft"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
        "operator": "AND",
        "label": "Härtefall anerkennen?",
        "children": ["2", "3"],
        "capabilities": [
          {
            "id": "ruml:actions",
            "payload": {
              "description": "Erstellt den Bescheid basierend auf dem Gesamtergebnis",
              "onTrue": {
                "operation": "createDocument",
                "ref": "document_service",
                "config": {
                  "template": "hardship-approval",
                  "format": "pdf"
                }
              },
              "onFalse": {
                "operation": "createDocument",
                "ref": "document_service",
                "config": {
                  "template": "hardship-rejection",
                  "format": "pdf"
                }
              }
            }
          }
        ]
      },
      "2": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Einkommensgrenze unterschritten",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_annual_income < 25000"
            }
          }
        ]
      },
      "3": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "label": "Begründung plausibel",
        "capabilities": [
          {
            "id": "ruml:ai-query",
            "payload": {
              "model": "strong",
              "description": "Prüft die Plausibilität der Härtefallbegründung anhand der Richtlinien und Beispielfälle",
              "inputs": {
                "context": [
                  "ctx_guidelines",
                  "ctx_bsg_ruling",
                  "ctx_example_approved_medical",
                  "ctx_example_approved_job_loss",
                  "ctx_example_rejected_luxury",
                  "ctx_example_rejected_income"
                ],
                "dataPoints": ["dp_hardship_reason", "dp_annual_income"]
              },
              "config": {
                "deterministic": true,
                "effort": "high"
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
                  "responseOptions": ["approve", "reject", "requestMoreInfo"],
                  "context": ["ctx_guidelines", "ctx_bsg_ruling"]
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

**Notes on the example:**

- **Capability declaration:** `ruml:context`, `ruml:ai-query`, and `ruml:actions` are declared in
  the root `capabilities` array; context data resides in the `data` field of `ruml:context`
- **Various context types:** The example shows `url` (guidelines), `container` (court decision as
  PDF), and `embedded` (example cases)
- **Various categories:** `administrativeGuidance`, `courtDecision`, and `example`
- **Node binding:** The example cases and guidelines are referenced from the AI query node via
  `inputs.context`
- **AI query with context:** The AI query is defined via `capabilities.ruml:ai-query` on the node
  and references context objects in the `inputs.context` array
- **Actions as node Capability:** Both the root node and the AI query node use
  `capabilities.ruml:actions`
- **Source references:** All context objects with external sources have a `source` object with
  license information
- **Object key as ID:** The context objects have no separate `id` field — the object key (e.g.,
  `"ctx_guidelines"`) serves as the identifier

### Delivery via Sidecar (RUML-EXT)

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
      "id": "ruml:context",
      "payload": {
        "data": {
          "ctx_guidance": {
            "title": "Kreditvergaberichtlinien",
            "category": "administrativeGuidance",
            "type": "url",
            "url": "https://intern.bank.de/richtlinien.pdf",
            "timestamp": "2024-01-01T00:00:00Z"
          }
        }
      }
    }
  ],
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "ruml:context": {
        "refs": ["ctx_guidance"]
      }
    }
  }
}
```

### Validation

All validation rules apply — the required fields (`title`, `category`, `timestamp`) plus the
`type`-dependent ones (`url`, `containerPath`, `ref`), each node `refs` entry MUST resolve to an
entry in the `data` pool ([`CTX-10`](../08-validation/index.md#rule-ctx-10)), license tracking.

## Conformance tests

- [4.11 ruml:context](../../../tests/04-capabilities/4-11-ruml-context.test.yaml)
