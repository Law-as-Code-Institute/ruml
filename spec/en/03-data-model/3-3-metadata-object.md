<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.3 Metadata Object

The metadata object contains all information about the RUML file itself.

### 3.3.1 Required Fields

| **Field**  | **Type**   | **Description**                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`       | `UUID`     | MUST be a unique identification of the RUML file ([`META-01`](../08-validation/index.md#rule-meta-01))                                                                                                                                                                                                                                                                                                                                    |
| `version`  | `String`   | MUST specify the content version ([`META-01`](../08-validation/index.md#rule-meta-01)). Free-form, like a container image tag; SHOULD match `[A-Za-z0-9_][A-Za-z0-9._-]{0,127}` so it can serve as the version tag of a RUML URI (`…/<name>:<version>`). Rulemaps SHOULD use Semantic Versioning; files with `documentType: "law"` SHOULD use the date of the law version (`YYYY-MM-DD`, with `.n` for a further version on the same day) |
| `created`  | `DateTime` | MUST specify the creation timestamp ([`META-01`](../08-validation/index.md#rule-meta-01))                                                                                                                                                                                                                                                                                                                                                 |
| `modified` | `DateTime` | MUST specify the timestamp of the last modification ([`META-01`](../08-validation/index.md#rule-meta-01)). MUST be >= `created` ([`META-03`](../08-validation/index.md#rule-meta-03))                                                                                                                                                                                                                                                                                          |
| `status`   | `Enum`     | MUST specify the status of the regulation ([`META-01`](../08-validation/index.md#rule-meta-01)). MUST be one of the defined status values ([`META-02`](../08-validation/index.md#rule-meta-02))                                                                                                                                                                                                                                                                                |

### 3.3.2 Optional Fields

| **Field**      | **Type**        | **Description**                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`        | `String`        | MAY contain a human-readable title of the rulemap.                                                                                                                                                                                                                                                                                                                                                              |
| `description`  | `String`        | MAY contain a short description of the rulemap.                                                                                                                                                                                                                                                                                                                                                                 |
| `documentType` | `Enum`          | MAY classify the document type. MUST if present be one of the defined values ([`META-05`](../08-validation/index.md#rule-meta-05)). See [Section 3.3.6](3-3-metadata-object.md) for the complete value list.                                                                                                                                                                                                                                         |
| `authors`      | `Array[Object]` | MAY contain a list of authors. MUST if present contain at least one entry ([`META-06`](../08-validation/index.md#rule-meta-06)). Each object MUST contain a `name` field (`String`) ([`META-06`](../08-validation/index.md#rule-meta-06)). The fields `email` (String, RFC 5321) and `organization` (`String`) are optional. Note: `authors[].organization` refers to the institutional affiliation of the author — not the publishing organization of the document (see `organization`). |
| `organization` | `String`        | MAY specify the **publishing** organization (who is institutionally responsible for the document). Note: Difference from `authors[].organization`: This field describes responsibility for the document, not an individual's affiliation.                                                                                                                                                                       |
| `jurisdiction` | `String`        | MAY specify the jurisdiction. MUST begin with an ISO 3166-1 alpha-2 country code ([`META-07`](../08-validation/index.md#rule-meta-07)). MAY contain hyphen-separated subdivisions ([`META-07`](../08-validation/index.md#rule-meta-07)). Format: `"CC"` or `"CC-XX"` or `"CC-XX-YY-..."`. Examples: `"DE"`, `"DE-BY"`, `"DE-BY-M"`, `"DE-BY-09162"`.                                                                                                                                      |
| `legalDomain`  | `String`        | MAY specify the legal domain.                                                                                                                                                                                                                                                                                                                                                                                   |
| `tags`         | `Array[String]` | MAY contain categorization/tagging.                                                                                                                                                                                                                                                                                                                                                                             |
| `derivedFrom`  | `Object`        | MAY contain information about the origin. MUST be used for working copies.                                                                                                                                                                                                                                                                                                                                      |
| `language`     | `String`        | MAY specify the language. MUST conform to the ISO 639-1 format (e.g., `"de"`, `"en"`) ([`META-08`](../08-validation/index.md#rule-meta-08)).                                                                                                                                                                                                                                                                                                         |
| `validFrom`    | `DateTime`      | MAY specify the validity start date.                                                                                                                                                                                                                                                                                                                                                                            |
| `validUntil`   | `DateTime`      | MAY specify the validity end date. If both `validFrom` and `validUntil` are set, `validUntil` MUST be > `validFrom` ([`META-09`](../08-validation/index.md#rule-meta-09)).                                                                                                                                                                                                                                                                           |
| `replaces`     | `UUID`          | MAY reference a replaced version. MAY be used together with `replacedBy` ([`META-04`](../08-validation/index.md#rule-meta-04)).                                                                                                                                                                                                                                                                                                                      |
| `replacedBy`   | `UUID`          | MAY reference a successor version. MAY be used together with `replaces` ([`META-04`](../08-validation/index.md#rule-meta-04)).                                                                                                                                                                                                                                                                                                                       |
| `comment`      | `String`        | MAY contain a free-text comment on the document, e.g. the reason for the status `suspended`.                                                                                                                                                                                                                                                                                                                    |

### 3.3.3 Status Values

The status of a RUML file MUST be one of the following values ([`META-02`](../08-validation/index.md#rule-meta-02)):

| **Status**    | **Description** | **Requirements**                                                                               |
| ------------- | --------------- | ---------------------------------------------------------------------------------------------- |
| `"draft"`     | Draft           | NO additional requirements                                                                     |
| `"review"`    | Under review    | SHOULD have `authors` set                                                                      |
| `"approved"`  | Approved        | SHOULD have `organization` set                                                                 |
| `"inForce"`   | In force        | MUST have `validFrom` set ([`META-10`](../08-validation/index.md#rule-meta-10)). SHOULD have `jurisdiction` set                     |
| `"suspended"` | Suspended       | SHOULD have `validUntil` or `comment` set                                                      |
| `"expired"`   | Expired         | MUST have `validUntil` set ([`META-11`](../08-validation/index.md#rule-meta-11)). `validUntil` MUST be in the past ([`META-11`](../08-validation/index.md#rule-meta-11)) |
| `"replaced"`  | Replaced        | MUST have `replacedBy` set ([`META-12`](../08-validation/index.md#rule-meta-12))                                                    |

**Additional rules:**

- The status MUST be checked with every content change
- When transitioning status from `"draft"` to `"inForce"`, all required fields MUST be validated
- A status of `"replaced"` MUST NOT be set back to another status

**Note: Document status vs. node status**

The status values defined here (`draft`, `review`, `approved`, `inForce`, `suspended`, `expired`,
`replaced`) describe the **document status** of the RUML file. They are stored in the
`metadata.status` field and describe the validity state of the entire regulation.

These are to be distinguished from the **node status** (`pending`, `true`, `false`, `undefined`,
`ignored`), which is computed at runtime during evaluation. The node status is NOT stored in the
RUML structure, but exclusively in a separate RUML Result file (`.ruml-result`). Details see
[Chapter 5](../05-result-format/index.md).

### 3.3.4 Metadata Object Example

```jsonc
"metadata": {
  "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
  "version": "2024.1.0",
  "created": "2024-01-15T10:00:00+01:00",
  "modified": "2024-02-01T14:30:00+01:00",
  "status": "inForce",
  "documentType": "law",
  "authors": [
    {
      "name": "Max Mustermann",
      "email": "max.mustermann@bmf.bund.de",
      "organization": "Bundesministerium der Finanzen"
    }
  ],
  "jurisdiction": "DE",
  "legalDomain": "Steuerrecht",
  "language": "de",
  "validFrom": "2024-01-01T00:00:00+01:00",
  "tags": ["Einkommensteuer", "§32a", "Grundtarif"]
}
```

**Notes:**

- This example shows a metadata object with status `"inForce"` and `documentType: "law"`
- The required field `validFrom` is set
- The optional fields `jurisdiction`, `legalDomain`, etc. are populated as examples

- Integrity assurance (hashing, signatures) is provided at container level (see
  [Chapter 7](../07-container/index.md))

### 3.3.5 Working Copies of Documents with Status `"inForce"`

**Basic principle:** Documents with status `"inForce"` SHOULD NOT be modified. Immutability is
ensured through signatures at container level (see [Chapter 7](../07-container/index.md)). Working
copies MUST be possible.

**Rules for working copies:**

1. **When creating a working copy, the following MUST be done:**

- A new UUID must be assigned
- The status must be changed to `"draft"`
- The origin must be documented in the `derivedFrom` object

1. **The** `derivedFrom` **object:**

| **Field**        | **Type**   | **Description**                                                                                                                                      |
| ---------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `originalId`     | `UUID`     | MUST contain the ID of the original document ([`META-13`](../08-validation/index.md#rule-meta-13))                                                                                        |
| `originalHash`   | `String`   | MAY contain the hash of the original document ([`META-04`](../08-validation/index.md#rule-meta-04)). The hash is computed at container level (see [Chapter 7](../07-container/index.md)). |
| `originalStatus` | `Enum`     | MUST contain the status of the original at the time of copying ([`META-13`](../08-validation/index.md#rule-meta-13))                                                                      |
| `derivationType` | `Enum`     | MUST specify the type: `"workingCopy"`, `"amendment"`, `"revision"` ([`META-13`](../08-validation/index.md#rule-meta-13))                                                                 |
| `derivedAt`      | `DateTime` | MUST contain the timestamp of the copy creation ([`META-13`](../08-validation/index.md#rule-meta-13))                                                                                     |
| `derivedBy`      | `String`   | SHOULD specify the creating entity/person                                                                                                            |

1. **Validation for working copies:**

- The system MAY verify the integrity of the original via the container hash (see
  [Chapter 7](../07-container/index.md))
- The system MUST ensure that the copy is NOT marked as `"inForce"` ([`META-14`](../08-validation/index.md#rule-meta-14))
- The system SHOULD make the derivation chain traceable

**Working copy example:**

```jsonc
"metadata": {
  "id": "d8129e0c-cf2e-4ef9-b7b6-fa8b206d5517",
  "version": "1.0.1-draft",
  "created": "2024-01-15T10:00:00+01:00",
  "modified": "2024-01-15T10:00:00+01:00",
  "status": "draft",
  "derivedFrom": {
    "originalId": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "originalHash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2",
    "originalStatus": "inForce",
    "derivationType": "workingCopy",
    "derivedAt": "2024-01-15T10:00:00+01:00",
    "derivedBy": "Bundesministerium der Justiz"
  }
}
```

**Note:** This structure enables legislators to work with copies of legally binding documents. The
integrity and immutability of the originals is ensured through signatures at container level (see
[Chapter 7](../07-container/index.md)).

### 3.3.6 documentType Values

The optional field `documentType` classifies the document type of the RUML file. If present, it MUST
be one of the following values ([`META-05`](../08-validation/index.md#rule-meta-05)):

| **Value**              | **Description**                                                                                                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `"law"`                | Formal law (e.g., EStG, BGB, SGB)                                                                                                                                                          |
| `"regulation"`         | Regulation, statute, or binding rule — public law (e.g., implementing regulation) or private sector (e.g., internal corporate policy with binding character)                               |
| `"guideline"`          | Guide, recommendation, or non-binding directive — e.g., administrative regulation, compliance guideline, best practice document                                                            |
| `"decision"`           | Decision logic for rule-based notices or judgments — public law (e.g., administrative decision, court ruling) or private sector (e.g., credit decision, compliance review, insurance case) |
| `"procedure"`          | Process or procedure description — e.g., administrative procedure, approval process, internal company workflow                                                                             |
| `"form"`               | Structured data collection or application process — e.g., application form, onboarding process, data collection                                                                            |
| `"documentGeneration"` | Rulemap for rule-based document generation — e.g., notices, contracts, reports, certificates. Evaluation produces one or more documents as output.                                         |
| `"other"`              | Other document types that do not match any of the more specific values                                                                                                                     |

**Notes:**

- The `documentType` field is independent of the `legalDomain` field: `legalDomain` describes the
  subject area (e.g., `"Steuerrecht"`, `"Kreditwesen"`, `"HR-Compliance"`), while `documentType`
  describes the form of the document (e.g., `"decision"`, `"documentGeneration"`)
- The value `"other"` SHOULD NOT be used when one of the more specific values applies
- The value list MAY be extended in future versions of the specification
- `documentType` is the **only** classification of a RUML file. The `rulemap` object deliberately
  contains no `type` field — document classification is exclusively located in the `metadata`
  object.

## Conformance tests

- [3.3 Metadata Object](../../../tests/03-data-model/3-3-metadata-object.test.yaml)
