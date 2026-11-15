<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.5 Verhältnis zu anderen Standards

Dieser Abschnitt benennt die Standards, die RUML verwendet oder auf die es sich bezieht. Er trifft
keine vergleichenden Aussagen über Abdeckung oder Eignung.

### Direkt von RUML verwendete Standards

| Standard                                                                          | Verwendung in RUML                                                               |
| --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) — JSON Data Interchange Format | Jede RUML-Datei ist ein gültiges JSON-Dokument.                                  |
| [JSON Schema draft 2020-12](https://json-schema.org/draft/2020-12) — JSON Schema  | Format der mit dieser Spezifikation gelieferten Schemas.                         |
| [JSONata](https://docs.jsonata.org/) 2.2.0                                        | Ausdruckssprache von `ruml:query`, `ruml:expression` und berechneten DataPoints. |
| [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) — JSON Canonicalization Scheme | Kanonische Hash-Berechnung auf Container-Ebene.                                  |
| [RFC 7515](https://www.rfc-editor.org/rfc/rfc7515) — JSON Web Signature           | Container-Signaturformat `jws-detached`.                                         |
| [RFC 7516](https://www.rfc-editor.org/rfc/rfc7516) — JSON Web Encryption          | Container-Verschlüsselungsformat `jwe`.                                          |
| [RFC 5652](https://www.rfc-editor.org/rfc/rfc5652) — Cryptographic Message Syntax | Container-Formate `cms-detached` und `cms-enveloped`.                            |
| [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) — Keyword Requirement Levels     | Bedeutung von MUSS, SOLLTE, DARF und verwandten Schlüsselwörtern.                |
| ISO 3166-1, ISO 3166-2                                                            | Länder- und Subdivisions-Codes im Feld `metadata.jurisdiction`.                  |
| ISO 639-1                                                                         | Sprachcodes in `metadata.language`.                                              |
| ISO 8601                                                                          | Datums- und DateTime-Werte im gesamten Format.                                   |
| ISO 4217                                                                          | Währungscodes empfohlen für das `unit`-Feld von `currency`-DataPoints.           |
| RFC 5322                                                                          | E-Mail-Format für den DataPoint-Typ `email`.                                     |
| E.164                                                                             | Telefon-Format für den DataPoint-Typ `phone`.                                    |
| RFC 3986                                                                          | URI-Format für den DataPoint-Typ `url`.                                          |

### Angrenzende Standards

Andere Standards adressieren überlappende oder angrenzende Belange im Bereich der rechtlichen
Datenmodellierung. Diese Spezifikation definiert keine formalen Abbildungen auf solche Standards.
Ihre Verwendung zusammen mit RUML wird nicht adressiert.
