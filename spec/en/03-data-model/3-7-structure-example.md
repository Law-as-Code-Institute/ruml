<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 3.7 Structure Example

## 3.7 Complete Structure Example

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "created": "2024-01-01T12:00:00+01:00",
    "modified": "2024-01-15T14:30:00+01:00",
    "status": "draft",
    "documentType": "procedure",
    "title": "Credit Approval"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "operator": "AND",
        "label": "Approve credit?",
        "children": ["2", "7"]
      },
      "2": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "operator": "OR",
        "label": "Income verification",
        "children": ["3", "4"]
      },
      "3": {
        "id": "9ddd08c6-a6d3-4f0f-9bb9-1adbe33b6e10",
        "label": "High income"
      },
      "4": {
        "id": "e07fe192-121b-43eb-90f0-eca4573ba8fa",
        "operator": "AND",
        "label": "Medium income + collateral",
        "children": ["5", "6"]
      },
      "5": {
        "id": "fcf02185-ffee-48a4-bf93-d2fb1b17944d",
        "label": "Medium income"
      },
      "6": {
        "id": "4a9f0fc7-c802-489e-8ae2-3596ba584fd9",
        "label": "Collateral available"
      },
      "7": {
        "id": "043fdfce-d617-4a76-af40-e02de43c07b8",
        "operator": "NOT_AND",
        "label": "No negative indicators",
        "children": ["8", "9"]
      },
      "8": {
        "id": "38f26fa1-17a5-4e38-9054-3147e3158a41",
        "label": "Insolvency present"
      },
      "9": {
        "id": "7baae662-0b5c-44bb-9a2b-802074fe5d0f",
        "label": "Negative SCHUFA entry"
      }
    }
  }
}
```

---

## 3.7.1 Supplementary Example: RUML File as Law

This example shows a RUML file that represents a legal text (`documentType: "law"`). Each node marks
the norm it represents with an anchor of type `represents` in the node-level `ruml:text-reference`
capability; the underlying text entries live in the `data` object of the root-level
`ruml:text-reference` capability (see
[Chapter 4.12](../04-capabilities/4-12-ruml-text-reference.md)).

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:text-reference",
      "payload": {
        "data": {
          "text_estg_32a": {
            "title": "§ 32a EStG – Einkommensteuertarif",
            "uri": "/akn/de/act/2024-01-01/estg#sec_32a",
            "timestamp": "2024-01-15T00:00:00Z",
            "status": "inForce",
            "type": "embedded",
            "text": "§ 32a Einkommensteuer\n(1) Die tarifliche Einkommensteuer bemisst sich nach dem zu versteuernden Einkommen. Sie beträgt ab dem Veranlagungszeitraum 2024 vorbehaltlich der §§ 32b, 32d, 34, 34a, 34b und 34c jeweils in Euro für zu versteuernde Einkommen bis 11.604 Euro (Grundfreibetrag): 0 ...",
            "validFrom": "2024-01-01T00:00:00Z",
            "language": "de"
          },
          "text_estg_1": {
            "title": "§ 1 EStG – Steuerpflicht",
            "uri": "/akn/de/act/2024-01-01/estg#sec_1",
            "timestamp": "2024-01-15T00:00:00Z",
            "status": "inForce",
            "type": "embedded",
            "text": "§ 1 Steuerpflicht\n(1) Natürliche Personen, die im Inland einen Wohnsitz oder ihren gewöhnlichen Aufenthalt haben, sind unbeschränkt einkommensteuerpflichtig.",
            "validFrom": "2024-01-01T00:00:00Z",
            "language": "de"
          }
        }
      }
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "2024-01-01",
    "created": "2024-01-15T10:00:00+01:00",
    "modified": "2024-01-15T10:00:00+01:00",
    "status": "draft",
    "documentType": "law",
    "title": "Income Tax – Basic Allowance"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "operator": "AND",
        "label": "Income tax applies",
        "children": ["2", "3"],
        "capabilities": [
          {
            "id": "ruml:text-reference",
            "payload": {
              "refs": [
                {
                  "id": "text_estg_32a",
                  "type": "represents"
                }
              ]
            }
          }
        ]
      },
      "2": {
        "id": "8fc54c7d-7f60-410e-9493-4f1eecfb1af8",
        "label": "Income exceeds basic allowance",
        "capabilities": [
          {
            "id": "ruml:text-reference",
            "payload": {
              "refs": [
                {
                  "id": "text_estg_32a",
                  "type": "represents"
                }
              ]
            }
          }
        ]
      },
      "3": {
        "id": "56b5b9db-b791-4fe5-abb0-a05cb0847db6",
        "label": "Unlimited tax liability",
        "capabilities": [
          {
            "id": "ruml:text-reference",
            "payload": {
              "refs": [
                {
                  "id": "text_estg_1",
                  "type": "represents"
                }
              ]
            }
          }
        ]
      }
    }
  }
}
```

**Notes on the supplementary example:**

- The root-level `ruml:text-reference` capability holds the norm texts in its `data` object, keyed
  by text ID ([Chapter 4.12](../04-capabilities/4-12-ruml-text-reference.md))
- Each node marks the norm it represents with an anchor of type `represents`, naming a text entry of
  the same file by its `id`
- The texts here are plain `text` entries, so an anchor addresses a whole entry. To anchor
  individual subsections or sentences, the law carries its text as RUML Text and anchors add the
  element's `GUID` as `element` (see [3.7.2](#372-supplementary-example-law-carried-as-ruml-text))
- A `represents` anchor is optional but SHOULD be present for nodes in a `documentType: "law"` file

---

## 3.7.2 Supplementary Example: Law Carried as RUML Text

A law is carried once, in the RUML file that represents it. This file carries § 1 SGB XII as RUML
Text, and its nodes anchor into that text — down to individual sentences. Anchors are local
([Chapter 4.12](../04-capabilities/4-12-ruml-text-reference.md#node-level-anchors)): other rulemaps
do not anchor into this text but reference this file's nodes.

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
            "type": "embedded",
            "digest": "sha3-256:541651b3dea3102b4e29d035fbeebd8d6473630975d4848e57bf2831bb0249b3",
            "source": {
              "uri": "https://testphase.rechtsinformationen.bund.de/v1/legislation/eli/bund/bgbl-1/2003/s3023/2026-07-30/1/deu/regelungstext-verkuendung-1.xml"
            },
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
                      "attrs": {
                        "eId": "hauptteil-n1",
                        "GUID": "1f4e2a90-6b3c-4d7e-8a51-0c9d2e7f3b11"
                      },
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
                              "attrs": {
                                "eId": "art-z1_bezeichnung-n1",
                                "GUID": "6e3a1d70-9c42-4b85-a7f1-3d2c8b0e5f12"
                              },
                              "content": ["§ 1"]
                            },
                            {
                              "type": "heading",
                              "attrs": {
                                "eId": "art-z1_überschrift-n1",
                                "GUID": "2a9c5e81-4d07-4f3b-b6e2-8f1a0c7d9e13"
                              },
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
                                  "type": "num",
                                  "attrs": {
                                    "eId": "art-z1_abs-z_bezeichnung-n1",
                                    "GUID": "8b2d4f63-1e90-4a7c-9d35-6f0e2b1c8a14"
                                  }
                                },
                                {
                                  "type": "content",
                                  "attrs": {
                                    "eId": "art-z1_abs-z_inhalt-n1",
                                    "GUID": "3c7e9b05-2f18-4d6a-8e4c-1b9d0f5a7c15"
                                  },
                                  "content": [
                                    {
                                      "type": "p",
                                      "attrs": {
                                        "eId": "art-z1_abs-z_inhalt-n1_text-n1",
                                        "GUID": "d4a1c826-5b3e-4f07-a9d2-7e6c3b0f1a16"
                                      },
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
                                            "GUID": "f15b8e37-6a29-4c41-8d7f-2e0a9c3b5d17",
                                            "refersTo": "satzende"
                                          }
                                        },
                                        " Zur Erreichung dieser Ziele haben die Leistungsberechtigten und die Träger der Sozialhilfe im Rahmen ihrer Rechte und Pflichten zusammenzuwirken.",
                                        {
                                          "type": "marker",
                                          "attrs": {
                                            "eId": "art-z1_abs-z_inhalt-n1_text-n1_marker-n3",
                                            "GUID": "7e2c0a49-8d16-4b5e-9f83-5a1d4c6e2b18",
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
          }
        }
      }
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "2026-07-30",
    "created": "2026-10-09T00:00:00Z",
    "modified": "2026-10-09T00:00:00Z",
    "status": "inForce",
    "validFrom": "2026-07-30T00:00:00Z",
    "documentType": "law",
    "title": "SGB XII § 1"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "operator": "AND",
        "label": "Aufgabe der Sozialhilfe",
        "children": ["2", "3"],
        "capabilities": [
          {
            "id": "ruml:text-reference",
            "payload": {
              "refs": [
                {
                  "id": "text_main",
                  "element": "5d8f3c21-7a64-4c0b-8e2f-1a9b6c3d7e02",
                  "type": "represents"
                }
              ]
            }
          }
        ]
      },
      "2": {
        "id": "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e",
        "label": "Beneficiary works towards independence as far as possible",
        "capabilities": [
          {
            "id": "ruml:text-reference",
            "payload": {
              "refs": [
                {
                  "id": "text_main",
                  "element": "f15b8e37-6a29-4c41-8d7f-2e0a9c3b5d17",
                  "type": "represents"
                }
              ]
            }
          }
        ]
      },
      "3": {
        "id": "c3d4e5f6-a7b8-4c9d-ae1f-2a3b4c5d6e7f",
        "label": "Beneficiary cooperates with the social assistance agency",
        "capabilities": [
          {
            "id": "ruml:text-reference",
            "payload": {
              "refs": [
                {
                  "id": "text_main",
                  "element": "7e2c0a49-8d16-4b5e-9f83-5a1d4c6e2b18",
                  "type": "represents"
                },
                {
                  "id": "text_main",
                  "element": "9a7c2e14-3b58-4d6f-a1e0-4c2b8d5f6a03",
                  "type": "refers-to"
                }
              ]
            }
          }
        ]
      }
    }
  }
}
```

**Notes on the RUML Text example:**

- The text of § 1 SGB XII exists once, in this file; every anchor names the entry key `text_main`
  and, as `element`, a `GUID` of its RUML Text
- `5d8f3c21-…` is the paragraph of § 1; `f15b8e37-…` and `7e2c0a49-…` are the sentence-end markers
  of Satz 2 and Satz 3, because LegalDocML.de marks sentence ends with `satzende` markers
- Node 3 represents Satz 3 and refers to Satz 1 (`9a7c2e14-…`), which states the aim the cooperation
  serves
- When the law gets a new version, the anchors stay as they are: the `GUID` values continue as long
  as the elements still exist, even if they are renumbered
