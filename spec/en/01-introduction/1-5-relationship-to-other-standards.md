<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.5 Relationship to Other Standards

This section names the standards that RUML uses or refers to. It makes no comparative claims about
coverage or suitability.

### Standards Used Directly by RUML

| Standard                                                                          | Use in RUML                                                                     |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) — JSON Data Interchange Format | Every RUML file is a valid JSON document.                                       |
| [JSON Schema draft 2020-12](https://json-schema.org/draft/2020-12) — JSON Schema  | The format of the schemas shipped with this specification.                      |
| [JSONata](https://docs.jsonata.org/) 2.2.0                                        | Expression language of `ruml:query`, `ruml:expression` and computed DataPoints. |
| [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) — JSON Canonicalization Scheme | Canonical hash computation at container level.                                  |
| [RFC 7515](https://www.rfc-editor.org/rfc/rfc7515) — JSON Web Signature           | Container signature format `jws-detached`.                                      |
| [RFC 7516](https://www.rfc-editor.org/rfc/rfc7516) — JSON Web Encryption          | Container encryption format `jwe`.                                              |
| [RFC 5652](https://www.rfc-editor.org/rfc/rfc5652) — Cryptographic Message Syntax | Container formats `cms-detached` and `cms-enveloped`.                           |
| [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) — Keyword Requirement Levels     | Meaning of MUST, SHOULD, MAY, and related keywords.                             |
| ISO 3166-1, ISO 3166-2                                                            | Country and subdivision codes in `metadata.jurisdiction`.                       |
| ISO 639-1                                                                         | Language codes in `metadata.language`.                                          |
| ISO 8601                                                                          | Date and datetime values throughout the format.                                 |
| ISO 4217                                                                          | Currency codes recommended for the `unit` field of `currency` DataPoints.       |
| RFC 5322                                                                          | Email format used by the `email` DataPoint type.                                |
| E.164                                                                             | Phone format used by the `phone` DataPoint type.                                |
| RFC 3986                                                                          | URI format used by the `url` DataPoint type.                                    |

### Adjacent Standards

Other standards address overlapping or adjacent concerns in the legal-data-modeling space. This
specification does not define formal mappings to such standards. Their use alongside RUML is not
addressed.
