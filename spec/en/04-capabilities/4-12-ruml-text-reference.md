<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.12 ruml:text-reference

## 4.12 Capability `ruml:text-reference`

### Overview

| Property               | Value                                                    |
| ---------------------- | -------------------------------------------------------- |
| **Capability ID**      | `ruml:text-reference`                                    |
| **Scope**              | Root-Level (`data`) + Node-Level                         |
| **Default `required`** | `false`                                                  |
| **Node-Level**         | `payload.refs` of the node's `ruml:text-reference` entry |
| **Role**               | `data`                                                   |

This Capability links nodes with normative texts — laws, regulations, technical standards,
administrative directives, and other regulatory frameworks.

A RUML file carries its texts in the root `data` object — as plain text or as structured
[RUML Text](#ruml-text). Node-level [anchors](#node-level-anchors) are **local**: they point only
into the texts of the same RUML file. A rulemap that relies on a law kept in another RUML file does
not anchor into that file's text; it references the law's nodes
([`ruml:tree-reference`](4-15-ruml-tree-reference.md)), which have their own anchors.

**The node's norm (`represents`):** among its anchors, a node MAY mark the single text it
_represents_ — the norm the rule implements (see [Node-Level](#node-level-anchors)).

**Distinction from `ruml:context`:** `ruml:context` ([Chapter 4.11](4-11-ruml-context.md)) contains
supporting, informative materials (court decisions, commentaries, examples) as well as the subject
matter under examination. `ruml:text-reference` contains normative foundational texts on which
decision rules are based.

### Use Cases

- Linking nodes with underlying norms and regulatory frameworks
- Documentation of legal bases for audit trails
- Carrying a complete law as structured text in the RUML file that represents it
- Linking every node of that law's rulemap to the element of the text it represents
- Multilingual texts for international applications

---

### Root Level: Text Entries

Texts are provided via the `ruml:text-reference` Capability — either inline in the `capabilities`
array of the RUML file or via a RUML-EXT sidecar file ([Chapter 4.5](4-5-ruml-ext.md)):

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:text-reference",
      "payload": {
        "data": {
          "text_main": {
            "title": "Sozialgesetzbuch (SGB) Zwölftes Buch (XII) – Sozialhilfe",
            "uri": "eli/bund/bgbl-1/2003/s3023/2026-07-30/1/deu",
            "timestamp": "2026-10-09T00:00:00Z",
            "digest": "sha3-256:87464fc40b2e11c817467dffbc6c57c16d1611e132d4ae8d431f3f755357198f",
            "source": {
              "uri": "https://testphase.rechtsinformationen.bund.de/v1/legislation/eli/bund/bgbl-1/2003/s3023/2026-07-30/1/deu/regelungstext-verkuendung-1.xml"
            },
            "content": {
              "type": "akomaNtoso",
              "attrs": {
                "xmlns": "http://Inhaltsdaten.LegalDocML.de/1.8.2/"
              },
              "content": [/* ... */]
            }
          },
          "text_bgb_823": {
            "title": "§ 823 BGB – Schadensersatzpflicht",
            "uri": "/akn/de/act/1896-08-18/bgb#sec_823__subsec_1",
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "inForce",
            "text": "Wer vorsätzlich oder fahrlässig das Leben, den Körper, die Gesundheit, die Freiheit, das Eigentum oder ein sonstiges Recht eines anderen widerrechtlich verletzt, ist dem anderen zum Ersatz des daraus entstehenden Schadens verpflichtet.",
            "validFrom": "2002-01-01T00:00:00Z",
            "language": "de"
          },
          "text_3f2c9a1e4b7d4e0f9a6c1b2d3e4f5a6b": {
            "title": "Benutzungssatzung der Stadtbibliothek",
            "timestamp": "2026-10-10T09:00:00Z",
            "digest": "sha3-256:b146f781bafdee78f9e68475fca93da37cf68d3559cd1c5f6e82ab3cef9c2638",
            "content": {
              "type": "akomaNtoso",
              "attrs": {
                "xmlns": "http://Inhaltsdaten.LegalDocML.de/1.8.2/"
              },
              "content": [/* ... */]
            }
          }
        }
      }
    }
  ],
  "metadata": {/* ... */},
  "rulemap": {/* ... */}
}
```

**Key Convention:** The keys in the `data` object (e.g., `text_main`) serve as unique identifiers.
Keys **MUST** match the pattern `[a-z_][a-z0-9_]*` ([`TXT-02`](../08-validation/index.md#rule-txt-02)). A separate `id` field is not
required. Anchors embed the key, so a key **MUST NOT** change once anchors may point at it
([`TXT-03`](../08-validation/index.md#rule-txt-03)); tools that generate keys **SHOULD** use `text_` followed by the 32 hexadecimal
digits of a UUID without hyphens (`text_3f2c9a1e4b7d4e0f9a6c1b2d3e4f5a6b`) and **SHOULD NOT** derive
keys from titles. Each official language version of a text is its own entry (e.g., `text_de`,
`text_fr`).

#### Required Fields

| **Field**   | **Type** | **Description**                                                                                                                                                                    |
| ----------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`     | String   | **MUST** give the human-readable title of the text, e.g. for lists and catalogs ([`TXT-04`](../08-validation/index.md#rule-txt-04)).                                                                                   |
| `timestamp` | DateTime | **MUST** specify the time of recording as an RFC 3339 `date-time` ([`TXT-04`](../08-validation/index.md#rule-txt-04), [`TXT-05`](../08-validation/index.md#rule-txt-05)).                                                                                  |
| `status`    | Enum     | **MUST** specify the status (see [Status Values](#status-values)) unless the entry has `content`; with `content`, the status follows from the text's own metadata ([`TXT-04`](../08-validation/index.md#rule-txt-04)). |

#### Optional Fields

| **Field**       | **Type** | **Description**                                                                                                                                                                                                                                |
| --------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `uri`           | String   | **MUST** identify the text when it is published by an authority or another external source (see [URI Convention](#uri-convention)); omitted for texts written in this RUML file.                                                               |
| `type`          | Enum     | **MAY** specify the embedding type: `embedded`, `container`, `url`, `external`. Default: `embedded`. `external` is deprecated ([`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                 |
| `text`          | String   | **MAY** contain the text as plain text. An entry **MUST NOT** carry both `text` and `content` ([`TXT-06`](../08-validation/index.md#rule-txt-06), [`TXT-07`](../08-validation/index.md#rule-txt-07)).                                                                                                                  |
| `content`       | Object   | **MAY** contain the text as [RUML Text](#ruml-text). Requires `digest` ([`TXT-06`](../08-validation/index.md#rule-txt-06), [`TXT-08`](../08-validation/index.md#rule-txt-08)).                                                                                                                                         |
| `digest`        | String   | **MUST** be present with `content`: `sha3-256:` followed by the hex SHA3-256 of the [canonical form](#digest) of `content` ([`TXT-08`](../08-validation/index.md#rule-txt-08), [`TXT-09`](../08-validation/index.md#rule-txt-09)).                                                                                     |
| `source`        | Object   | **SHOULD** be present with `content`: provenance of the text — `uri` of the source document it was imported from, optional `digest` of the archived source, optional `terms` (URI of the source's reuse terms, where the source attaches any). |
| `url`           | String   | **MUST** contain the URL when `type: "url"`. **MUST** be a valid URI format ([`TXT-05`](../08-validation/index.md#rule-txt-05), [`TXT-10`](../08-validation/index.md#rule-txt-10)).                                                                                                                                    |
| `containerPath` | String   | **MUST** specify the path in the container when `type: "container"`. **MUST** start with `.texts/` ([`TXT-10`](../08-validation/index.md#rule-txt-10), [`TXT-11`](../08-validation/index.md#rule-txt-11)).                                                                                                             |
| `ref`           | String   | **MUST** contain a symbolic reference when `type: "external"` ([`TXT-10`](../08-validation/index.md#rule-txt-10)).                                                                                                                                                                 |
| `version`       | String   | **MAY** specify the version (e.g., `"Fassung vom 1.1.2024"`) ([`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                                                                  |
| `validFrom`     | DateTime | **MAY** specify the validity start date. **MUST** be an RFC 3339 `date-time` ([`TXT-05`](../08-validation/index.md#rule-txt-05), [`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                                   |
| `validUntil`    | DateTime | **MAY** specify the validity end date. **MUST** be > `validFrom` if present ([`TXT-06`](../08-validation/index.md#rule-txt-06), [`TXT-12`](../08-validation/index.md#rule-txt-12)).                                                                                                                                    |
| `language`      | String   | **MAY** specify the language. **MUST** conform to ISO 639-1 format (e.g., `"de"`, `"en"`) ([`TXT-05`](../08-validation/index.md#rule-txt-05), [`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                      |
| `isReferenced`  | Boolean  | **MAY** indicate whether this entry is referenced by nodes. Default: `true` ([`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                                                   |

When an entry has `content`, the fields `status`, `validFrom`, `validUntil`, `language` and
`version` **SHOULD** be omitted; if present, they **MUST** agree with the text's own metadata
([`TXT-13`](../08-validation/index.md#rule-txt-13)).

#### URI Convention

The `uri` of a text entry identifies a text that exists outside the RUML file — preferably by its
official identifier. A text written in the RUML file itself has no `uri`; it is identified by the
file and its entry key. The `uri` is not used to address elements inside the text; that is the job
of [anchors](#node-level-anchors).

| Format                                | Example                                                                                    | Notes                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| European Legislation Identifier (ELI) | `eli/bund/bgbl-1/2003/s3023/2026-07-30/1/deu`, `http://data.europa.eu/eli/reg/2016/679/oj` | Preferred where the authority issues ELIs             |
| Akoma Ntoso (AKN)                     | `/akn/de/act/1900-08-18/bgb`                                                               | International standard for legal documents            |
| STOP (NL)                             | `/akn/nl/act/2024/gst-2024-123`                                                            | Dutch legal documents                                 |
| Gesetze-im-Internet                   | `https://www.gesetze-im-internet.de/bgb/__823.html`                                        | Acceptable for German law without official identifier |

The RUML spec does **not** mandate a specific URI scheme. Authors **SHOULD** use the official
identifier where one exists.

#### Embedding Types (`type`)

| **Type**    | **Description**                                   | **Usage**                                                                           |
| ----------- | ------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `embedded`  | Directly in the RUML file, as `text` or `content` | Text of any length — from individual sections up to the complete text of a law      |
| `container` | In the RUML container (ZIP)                       | Original/binary formats (e.g., PDF)                                                 |
| `url`       | External URL                                      | Public portals (e.g., [gesetze-im-internet.de](https://www.gesetze-im-internet.de)) |
| `external`  | Symbolic reference (deprecated)                   | Superseded by RUML files that carry the text themselves                             |

**Note on complete statutes:** a rulemap that represents a law (`documentType: "law"`) carries the
full statutory text as an `embedded` entry, preferably as `content` in RUML Text — there is NO
length limit. Other rulemaps reference that law's nodes instead of copying the text.

**Note on `url`:** The tool **SHOULD** fetch and cache the content as needed. The URL **SHOULD**
point to a stable, versioned source.

**Note on `external`:** The tool **MUST** resolve the symbolic reference (`ref`) to a concrete data
source. Configuration is done in the tool settings, **NOT** in the RUML file. New files **SHOULD**
reference the RUML file that carries the text instead.

The complete container specification (ZIP structure, manifest, directory conventions) is defined in
[Chapter 7](../07-container/index.md).

#### Status Values

| **Status** | **Description** | **Usage**                                                    |
| ---------- | --------------- | ------------------------------------------------------------ |
| `draft`    | Draft           | Not yet enacted                                              |
| `proposed` | Proposed        | Introduced drafts, under deliberation                        |
| `enacted`  | Enacted         | Adopted but not yet in force                                 |
| `inForce`  | In force        | Currently valid norm                                         |
| `amended`  | Amended         | Replaced by a newer version but still valid for legacy cases |
| `repealed` | Repealed        | No longer in force                                           |

**Validation rule:** For `status: "inForce"` and `type: "embedded"` (the default), the entry
**MUST** have a non-empty `text` or a `content` ([`TXT-07`](../08-validation/index.md#rule-txt-07)). Entries with any other status
**MAY** omit both.

---

### RUML Text

RUML Text is the structured form of a legal text: an
[Akoma Ntoso](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/) XML document written as
JSON, without loss. It is part of the RUML format, not a file format of its own: it exists only in a
text entry's `content`, and its rules are those of the file's `$specVersion`. XML remains the format
for exchange and validation: Akoma Ntoso documents, including those of national dialects such as
LegalDocML.de, convert into RUML Text and back mechanically ([Conversion](#conversion)).

#### Structure

```jsonc
"content": {
  "type": "akomaNtoso",
  "attrs": {
    "xmlns": "http://Inhaltsdaten.LegalDocML.de/1.8.2/"
  },
  "content": [
    {
      "type": "act",
      "attrs": {
        "name": "regelungstext"
      },
      "content": [
        {
          "type": "body",
          "content": [
            {
              "type": "article",
              "attrs": {
                "eId": "art-z1",
                "GUID": "0b1e9e8a-2c55-4f5f-9a3e-6d1c7b2a4e01"
              },
              "content": [
                {
                  "type": "num",
                  "content": ["§ 1"]
                },
                {
                  "type": "heading",
                  "content": ["Aufgabe der Sozialhilfe"]
                },
                {
                  "type": "paragraph",
                  "attrs": {
                    "eId": "art-z1_abs-z",
                    "GUID": "5d8f3c21-7a64-4c0b-8e2f-1a9b6c3d7e02"
                  },
                  "content": [
                    {
                      "type": "num"
                    },
                    {
                      "type": "content",
                      "content": [
                        {
                          "type": "p",
                          "content": [
                            "Aufgabe der Sozialhilfe ist es, den Leistungsberechtigten die Führung eines Lebens zu ermöglichen, das der Würde des Menschen entspricht.",
                            {
                              "type": "marker",
                              "attrs": {
                                "eId": "art-z1_abs-z_inhalt-n1_text-n1_marker-n1",
                                "GUID": "9a7c2e14-3b58-4d6f-a1e0-4c2b8d5f6a03",
                                "refersTo": "satzende"
                              }
                            },
                            " Die Leistung soll sie so weit wie möglich befähigen, unabhängig von ihr zu leben; darauf haben auch die Leistungsberechtigten nach ihren Kräften hinzuarbeiten.",
                            {
                              "type": "marker",
                              "attrs": {
                                "eId": "art-z1_abs-z_inhalt-n1_text-n1_marker-n2",
                                "GUID": "e27b9d03-1c4a-4f86-b5d2-7a0c9e3f1b24",
                                "refersTo": "satzende"
                              }
                            },
                            " Zur Erreichung dieser Ziele haben die Leistungsberechtigten und die Träger der Sozialhilfe im Rahmen ihrer Rechte und Pflichten zusammenzuwirken.",
                            {
                              "type": "marker",
                              "attrs": {
                                "eId": "art-z1_abs-z_inhalt-n1_text-n1_marker-n3",
                                "GUID": "55a21fb5-d00e-41c1-91a2-38eda90f21e0",
                                "refersTo": "satzende"
                              }
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

- **Elements:** every element of the XML document is a node `{type, attrs?, content?}`. `type` is
  the element name and `attrs` holds its attributes with string values, both named as in the XML.
  `content` holds the children in document order; character data is a plain JSON string.
- **Exact tree:** wrapper elements such as `content`, `intro` or `num` are nodes like any other. All
  character data is kept, including whitespace between elements. Adjacent strings **MUST** be merged
  into one ([`TXT-14`](../08-validation/index.md#rule-txt-14)).
- **Root:** the root object is the Akoma Ntoso root element. It **MUST** have `type`, `attrs` and
  `content` ([`TXT-15`](../08-validation/index.md#rule-txt-15)).
- **Namespaces:** namespace declarations are attributes and stay where the XML has them. The root
  **MUST** declare the namespace of its [dialect](#dialects) as the default namespace (`xmlns`), so
  the dialect's elements carry no prefix; no other element redeclares `xmlns` ([`TXT-15`](../08-validation/index.md#rule-txt-15),
  [`TXT-16`](../08-validation/index.md#rule-txt-16)). Names from other namespaces, such as the `ris:` metadata of LegalDocML.de, keep
  their prefix; the prefix **MUST** be declared by an `xmlns:<prefix>` attribute on the element or
  an ancestor ([`TXT-16`](../08-validation/index.md#rule-txt-16)). Elements and attributes of any namespace **MUST** be kept, also when
  a tool does not understand them ([`TXT-17`](../08-validation/index.md#rule-txt-17)).
- **Document types:** the root may hold any Akoma Ntoso document type — `act`, `bill`, `amendment`,
  `judgment`, `documentCollection` and others.

#### Conversion

**From XML.** Each element becomes a node with its name as `type`, its attributes (namespace
declarations included) as `attrs` and its children as `content`. Character data, CDATA sections and
resolved entity and character references become strings. Not represented are the XML declaration,
the document type declaration, comments, processing instructions and the attribute
`xsi:schemaLocation`: they carry no part of the legal text. An element **MUST NOT** have the
attribute `xsi:schemaLocation` ([`TXT-16`](../08-validation/index.md#rule-txt-16)). Where the source binds the dialect's namespace to a
prefix (LegalDocML.de documents use `akn:`), the importer removes the prefix from the names of the
elements in that namespace and declares the namespace with `xmlns` on the root; it keeps the
`xmlns:<prefix>` declaration only while attributes still use the prefix.

**To XML.** Each node becomes an element named `type` with the attributes in `attrs` and its
`content` in order. Strings become character data, with `&`, `<` and `>` escaped, and in attribute
values also `"`, tab, line feed and carriage return. An exporter **MAY** write an XML declaration
and the schema references its dialect uses (for LegalDocML.de, `xsi:schemaLocation` on the root and
an `xml-model` processing instruction for the Schematron).

**Round trip.** An XML document converted to RUML Text and back equals the original under
[Canonical XML 2.0](https://www.w3.org/TR/xml-c14n2/), except for the parts not represented and a
prefix the importer removed.

#### Dialects

The root's default namespace names the Akoma Ntoso dialect of the text and its version. Converted to
XML, a text **MUST** be valid against the schemas of its dialect ([`TXT-18`](../08-validation/index.md#rule-txt-18)). A text **MAY** be
a fragment that omits parts its dialect requires, such as the `meta` block of a text generated by a
tool; every element it does contain **MUST** then be valid where it stands in a complete document of
the dialect ([`TXT-18`](../08-validation/index.md#rule-txt-18)). RUML restates none of the dialect's rules: numbering, `eId` formation
and citation are defined by the dialect and checked by its schemas.

| Dialect                                  | Namespace (`xmlns`)                                | Schemas                                                                                                                                                                                                                                                                                                                                   |
| ---------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Akoma Ntoso 3.0 (OASIS)                  | `http://docs.oasis-open.org/legaldocml/ns/akn/3.0` | [XSD](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd)                                                                                                                                                                                                                                       |
| LegalDocML.de 1.8.2 (German federal law) | `http://Inhaltsdaten.LegalDocML.de/1.8.2/`         | [XSD](https://raw.githubusercontent.com/digitalservicebund/ris-norms/18c7c79ddc0e17f6cab36ba16171927b80a43272/LegalDocML.de/1.8.2/schema/legalDocML.de-baukasten.xsd), [Schematron](https://raw.githubusercontent.com/digitalservicebund/ris-norms/18c7c79ddc0e17f6cab36ba16171927b80a43272/LegalDocML.de/1.8.2/schema/legalDocML.de.sch) |

#### Element Identity: `GUID`

Every element that carries an `eId` **MUST** also carry a `GUID` ([`TXT-16`](../08-validation/index.md#rule-txt-16)). The `GUID` is the
element's lasting identity, and [anchors](#node-level-anchors) point at it; the `eId` is its
readable designation in the current version, formed from the numbering by the rules of the text's
[dialect](#dialects) (for LegalDocML.de: Schematron rules SCH-00430 to SCH-00450), and changes when
the text is renumbered.

- **Value:** **MUST** be a lowercase UUID (RFC 9562, [`TXT-16`](../08-validation/index.md#rule-txt-16)), assigned when the element is
  created. A text imported from a source that carries `GUID` values (LegalDocML.de requires one on
  every element) keeps them.
- **Uniqueness:** within one text entry, a `GUID` **MUST** be unique ([`TXT-16`](../08-validation/index.md#rule-txt-16)). A copied
  element is a new element and gets a new `GUID`.
- **Stability:** a `GUID` **MUST NOT** change — not in published versions and not in drafts, because
  anchors in this file, and references from other RUML files to the nodes anchored here, may already
  rely on it ([`TXT-03`](../08-validation/index.md#rule-txt-03)). Renumbering changes `eId` values only.
- **Across versions:** a new version of a text keeps the `GUID` of every element that continues and
  gives new elements new ones. Where a source issues new `GUID` values for each version, the
  importer **MUST** carry forward the `GUID` of each element it matches to the previous version
  ([`TXT-03`](../08-validation/index.md#rule-txt-03)).
- **Languages:** each language version is its own text entry with its own `GUID` values; RUML
  defines no identity across language versions.

**Example:** "§ 3" is created with `eId` `art-z3` and `GUID` `7c1e9a52-…`. A new § 2 is inserted
before it; the element becomes "§ 4" with `eId` `art-z4` — its `GUID` stays `7c1e9a52-…`, so every
anchor to it still finds it, and citations show the current "§ 4".

#### Sentences

Where the source marks the end of a sentence with a `marker` element whose `refersTo` is `satzende`
(as LegalDocML.de does), the marker's `GUID` identifies the sentence ending at that marker; an
anchor to it addresses that sentence. Tools **MUST NOT** add sentence markers that the source does
not contain ([`TXT-17`](../08-validation/index.md#rule-txt-17)). Texts without sentence markers can be anchored down to their smallest
marked element (e.g., a subsection or item).

#### Digest

The `digest` of a text entry is `sha3-256:` followed by the lowercase hex SHA3-256 hash of the UTF-8
bytes of the RFC 8785 (JSON Canonicalization Scheme) form of `content`. A parser **SHOULD** verify
it before relying on the text.

#### Provenance

`source` records where the text was imported from; `source.terms` points to the source's reuse terms
where the source attaches any (for example an attribution requirement).

RUML defines no plain-text form of RUML Text. Tools that need plain text derive it from the tree
themselves.

---

### Node-Level: Anchors

Nodes point at the texts of their own RUML file with **anchors** in the `refs` list of their
node-level `ruml:text-reference` entry. An anchor names a text entry by its key and, optionally, one
element of its RUML Text by the element's [`GUID`](#element-identity-guid).

```jsonc
{
  "id": "ruml:text-reference",
  "payload": {
    "refs": [
      {
        "id": "text_main",
        "element": "9a7c2e14-3b58-4d6f-a1e0-4c2b8d5f6a03",
        "type": "represents"
      },
      {
        "id": "text_main",
        "element": "e27b9d03-1c4a-4f86-b5d2-7a0c9e3f1b24",
        "type": "refers-to"
      },
      {
        "id": "text_bgb_823",
        "type": "refers-to"
      }
    ]
  }
}
```

| **Field** | **Type**      | **Required** | **Description**                                                                                                                                                                                                  |
| --------- | ------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `refs`    | Array[Object] | **MUST**     | The node's anchors; at least one ([`TXT-01`](../08-validation/index.md#rule-txt-01)).                                                                                                                                                                |
| `id`      | String        | **MUST**     | Key of a text entry in this file's own `data` object ([`TXT-01`](../08-validation/index.md#rule-txt-01)).                                                                                                                                            |
| `element` | String        | **MAY**      | `GUID` of an element of the entry's RUML Text — an article, a paragraph, a list item, a sentence marker. Without `element` the anchor addresses the whole text ([`TXT-01`](../08-validation/index.md#rule-txt-01)).                                  |
| `type`    | Enum          | **MUST**     | `represents`: the norm the node implements — the text the rule turns into a decision. `refers-to`: a text the node relies on without implementing it, such as a definition or a cross-reference ([`TXT-01`](../08-validation/index.md#rule-txt-01)). |

**Validation rules:**

- `refs` **MUST** contain at least one anchor ([`TXT-01`](../08-validation/index.md#rule-txt-01)).
- A node **MUST NOT** have more than one anchor of type `represents` ([`TXT-01`](../08-validation/index.md#rule-txt-01)).
- Each `id` **MUST** exist as a key in the `data` object of this file's `ruml:text-reference`
  Capability ([`TXT-19`](../08-validation/index.md#rule-txt-19)).
- An `element` **MUST** be the `GUID` of an element in that entry's `content`; an entry without
  `content` can only be anchored as a whole ([`TXT-20`](../08-validation/index.md#rule-txt-20)).
- Anchors **MUST** be unique — the same `id`, `element` and `type` **MUST NOT** appear twice
  ([`TXT-01`](../08-validation/index.md#rule-txt-01)).

Anchors never leave their RUML file, so they carry no file or version: when the file moves to a new
version of its text, the anchors stay as they are because `GUID` values are stable. Character ranges
and text-quote selectors are not supported; the finest addressable unit is an element with a `GUID`.

**Behavior for modular nodes:** a modular node (`modular: true`) always represents the same norm —
its anchors apply to **all instantiations**, regardless of where the node appears in the rule tree.

## Conformance tests

- [4.12 ruml:text-reference](../../../tests/04-capabilities/4-12-ruml-text-reference.test.yaml)
