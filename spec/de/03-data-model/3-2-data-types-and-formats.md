<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.2 Datentypen und Formate

### 3.2.1 LexID

Siehe [Kapitel 2.5](../02-file-format-basics/2-5-identifier-system.md#lexid) für die vollständige
Definition.

### 3.2.2 UUID

Siehe
[Kapitel 2.5](../02-file-format-basics/2-5-identifier-system.md#uuid-universally-unique-identifier)
für die vollständige Definition.

### 3.2.3 Weitere Datentypen

| **Typ**    | **Format**  | **Beispiel**                    | **Validierung**                                                                                                                                                   |
| ---------- | ----------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `String`   | UTF-8       | `"Bundesministerium"`           | MUSS UTF-8 kodiert sein ([`FMT-01`](../08-validation/index.md#rule-fmt-01)).                                                                                                                          |
| `Number`   | JSON Number | `42`, `3.14`, `1000.50`         | MUSS eine JSON-konforme Zahl sein (IEEE 754 double) ([`FMT-13`](../08-validation/index.md#rule-fmt-13)). DARF ganzzahlige oder dezimale Werte darstellen.                                             |
| `Boolean`  | Boolean     | `true`, `false`                 | MUSS ein JSON Boolean (`true` oder `false`) sein ([`FMT-13`](../08-validation/index.md#rule-fmt-13)).                                                                                                 |
| `DateTime` | RFC 3339    | `"2024-01-01T12:00:00+01:00"`   | MUSS ein `date-time` nach [RFC 3339, Abschnitt 5.6](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) sein, das JSON-Schema-Format `date-time` ([`FMT-13`](../08-validation/index.md#rule-fmt-13)). |
| `Enum`     | String      | `"draft"`, `"inForce"`, `"AND"` | MUSS ein in der Spezifikation definierter Wert sein ([`FMT-13`](../08-validation/index.md#rule-fmt-13)). Erlaubte Werte werden im jeweiligen Feld dokumentiert.                                       |
| `Object`   | JSON Object | `{"key": "value"}`              | MUSS ein JSON-Objekt sein ([`FMT-13`](../08-validation/index.md#rule-fmt-13)).                                                                                                                        |
| `Array`    | JSON Array  | `[1, 2, 3]`                     | MUSS ein valides JSON Array sein ([`FMT-13`](../08-validation/index.md#rule-fmt-13)).                                                                                                                 |

### 3.2.4 Hash-Format

Hashing und Integritätssicherung der RUML-Datei sind eine Aufgabe des RUML-Containers (siehe
[Kapitel 7](../07-container/index.md)). Die RUML-JSON-Datei enthält keinen Hash ihrer selbst. Die
Hashes, die sie enthalten kann, gehören zu anderen Inhalten: `derivedFrom.originalHash`
([3.3](3-3-metadata-object.md)), der `hash` eines Context-Eintrags
([4.11](../04-capabilities/4-11-ruml-context.md)) und der `digest` eines Text-Eintrags
([4.12](../04-capabilities/4-12-ruml-text-reference.md)).

**Hash-Format (Referenz für Container-Ebene):**

Hashes in RUML verwenden das erweiterte Format:

```
"{algorithm}:{value}"
```

**Beispiel:**

```
"sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
```

**Unterstützte Algorithmen:**

| **Algorithmus** | **Verwendung**                                              | **Format**              |
| --------------- | ----------------------------------------------------------- | ----------------------- |
| `sha3-256`      | MUSS für alle neuen Container verwendet werden              | 64 hexadezimale Zeichen |
| `sha256`        | DARF für Rückwärtskompatibilität verwendet werden           | 64 hexadezimale Zeichen |
| `blake3`        | DARF für performance-kritische Anwendungen verwendet werden | 64 hexadezimale Zeichen |

**Kanonische JSON-Repräsentation:**

Für konsistente Hash-Berechnung auf Container-Ebene MUSS die RUML-Datei kanonisiert werden. Die
Kanonisierung MUSS RFC 8785 (JSON Canonicalization Scheme) implementieren. Details zum
Berechnungsverfahren siehe [Kapitel 7](../07-container/index.md).

**Authentizität und rechtliche Verbindlichkeit:**

Hashes allein gewährleisten **keine Authentizität** und **keine rechtliche Verbindlichkeit**. Diese
Garantien werden durch Signaturen auf Container-Ebene erreicht (siehe
[Kapitel 7](../07-container/index.md)).

### 3.2.5 Integritätssicherung

Integritätssicherung — einschließlich Hashing, Signaturen und Zeitstempel — wird vollständig auf
Container-Ebene behandelt (siehe [Kapitel 7](../07-container/index.md)). Inline-Felder wie
`metadata.hash` oder `metadata.integrity` sind **nicht mehr Teil des RUML-Datenmodells**.

### 3.2.6 RUML-Dateistruktur (Top-Level)

Die Top-Level-Struktur einer RUML-Datei ist in
[Kapitel 2.2](../02-file-format-basics/2-2-file-structure.md) definiert.

**Designprinzip: Key = Identifikator bei Map-Strukturen**

RUML verwendet durchgängig das Prinzip, dass bei Map-Strukturen (JSON-Objekten) der **Key selbst als
Identifikator** dient. Ein Eintrag **DARF** seinen eigenen Key daher **NICHT** als Feld wiederholen:
Ein Knoten hat kein `lexId`-Feld, und Text-, Datapoint- und Context-Objekte haben keine eigene id
([`FMT-14`](../08-validation/index.md#rule-fmt-14), [`NODE-03`](../08-validation/index.md#rule-node-03)).

Andere Identifikatoren am Eintrag bleiben davon unberührt. Ein Knoten wird über seine LexID
adressiert, trägt aber weiterhin ein ERFORDERLICHES Feld `id` mit seiner UUID (siehe
[Kapitel 2.5](../02-file-format-basics/2-5-identifier-system.md)) — ein eigenständiger
Identifikator, keine Kopie des Keys ([`NODE-01`](../08-validation/index.md#rule-node-01)).

Dieses Prinzip gilt für alle Map-Strukturen in RUML:

`nodes` – Key ist die LexID (z.B. `"1"`, `"42"`)

`capabilities[{id: "ruml:text-reference"}].data` – Key ist die Text-ID (z.B. `"text_bgb_823"`,
`"text_sgb_12_21"`)

`capabilities[].data` – Key ist die Artefakt-ID (z.B. `"ctx_bgh_2024"`, `"dp_monthly_income"`) für
die Daten von `ruml:datapoints`, `ruml:context` usw.

**Vorteile:** Keine Redundanz, garantierte Eindeutigkeit durch JSON-Key-Semantik, einfachere
Validierung.

## Konformitätstests

- [3.2 Data Types and Formats](../../../tests/03-data-model/3-2-data-types-and-formats.test.yaml)
