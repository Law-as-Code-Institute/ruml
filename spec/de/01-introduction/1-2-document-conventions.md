<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.2 Konventionen dieses Dokuments

### Anforderungsstufen (RFC 2119)

Diese Spezifikation verwendet die Schlüsselwörter aus
[RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) zur Kennzeichnung von Anforderungsstufen. Die
Übersetzung der englischen Begriffe erfolgt nach der folgenden Tabelle:

| Schlüsselwort       | Englisch                    | Bedeutung                                                  |
| ------------------- | --------------------------- | ---------------------------------------------------------- |
| **MUSS**            | **MUST**, **SHALL**         | Absolute Anforderung                                       |
| **ERFORDERLICH**    | **REQUIRED**                | Absolute Anforderung                                       |
| **DARF NICHT**      | **MUST NOT**, **SHALL NOT** | Absolutes Verbot                                           |
| **SOLLTE**          | **SHOULD**                  | Starke Empfehlung; Abweichung erfordert begründeten Anlass |
| **EMPFOHLEN**       | **RECOMMENDED**             | Starke Empfehlung; Abweichung erfordert begründeten Anlass |
| **SOLLTE NICHT**    | **SHOULD NOT**              | Starke Empfehlung dagegen; nur mit begründetem Anlass      |
| **NICHT EMPFOHLEN** | **NOT RECOMMENDED**         | Starke Empfehlung dagegen; nur mit begründetem Anlass      |
| **DARF**            | **MAY**                     | Wirklich optional                                          |
| **OPTIONAL**        | **OPTIONAL**                | Wirklich optional                                          |

Die Schlüsselwörter sind nur in Großbuchstaben normativ. Die Pluralformen **MÜSSEN**, **DÜRFEN** und
**SOLLTEN** und gebeugte Formen wie **ERFORDERLICHES** sind dieselben Schlüsselwörter; **NICHT**
darf durch die Satzstellung vom Verb getrennt stehen („DARF `role` NICHT deklarieren“) oder als
**KEIN**, **KEINE**, **KEINEN** usw. am Substantiv stehen („DARF KEIN `children`-Array haben“).

### Notation

| Konvention         | Form                                                                                     | Beispiel           |
| ------------------ | ---------------------------------------------------------------------------------------- | ------------------ |
| JSON-Beispiel      | Fenced Code Block mit `json`-Highlighting                                                | `"lexId": "1"`     |
| Platzhalter        | Spitze Klammern                                                                          | `<lexId>`          |
| Optionales Element | Markiert `[optional]`                                                                    | `field [optional]` |
| Wiederholung       | Auslassungspunkte                                                                        | `..., ...`         |
| Pattern            | Regulärer Ausdruck (ECMA-262)                                                            | `^[1-9][0-9]*$`    |
| Feldtyp            | Verweist auf Datentypen in [Kapitel 3.2](../03-data-model/3-2-data-types-and-formats.md) | `UUID`, `DateTime` |

### Benennungs-Konventionen

RUML unterscheidet schema-definierte Felder von nutzerdefinierten Identifikatoren über die
Schreibweise:

- **Schema-definierte Felder** verwenden Camel-Case — z. B. `lexId`, `id`, `children`,
  `containerPath`, `validFrom`, `documentType`, `decisionMode`, `expression`, `onTrue`.
- **Nutzerdefinierte Identifikatoren** verwenden Snake-Case — z. B. DataPoint-IDs
  (`dp_annual_income`), Context-IDs (`ctx_court_ruling`) und Text-IDs (`text_bgb_823`)
  ([`DP-02`](../08-validation/index.md#rule-dp-02)).
- **Implementierungsdefinierte Identifikatoren** wie zum Beispiel Referenzen auf Actions oder
  AI-Models SOLLTEN Snake-Case verwenden — z. B. `document_service`, `manual_review_workflow`.

Tools SOLLTEN dieser Konvention beim Erzeugen neuer Identifikatoren folgen. Capability-IDs folgen
ihrer eigenen Namespace-Konvention gemäß [Kapitel 4.4](../04-capabilities/4-4-namespaces.md).
