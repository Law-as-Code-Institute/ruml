<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.3 Metadata-Objekt

Das Metadata-Objekt enthält alle Informationen über die RUML-Datei selbst.

### 3.3.1 Pflichtfelder

| **Feld**   | **Typ**    | **Beschreibung**                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`       | `UUID`     | MUSS eine eindeutige Identifikation der RUML-Datei sein ([`META-01`](../08-validation/index.md#rule-meta-01))                                                                                                                                                                                                                                                                                                                                                                             |
| `version`  | `String`   | MUSS die Version des Inhalts angeben ([`META-01`](../08-validation/index.md#rule-meta-01)). Frei wählbar, wie ein Container-Image-Tag; SOLLTE dem Muster `[A-Za-z0-9_][A-Za-z0-9._-]{0,127}` entsprechen, damit sie als Versions-Tag einer RUML-URI dienen kann (`…/<name>:<version>`). Rulemaps SOLLTEN Semantic Versioning verwenden; Dateien mit `documentType: "law"` SOLLTEN das Datum der Gesetzesfassung verwenden (`JJJJ-MM-TT`, mit `.n` für eine weitere Fassung am selben Tag) |
| `created`  | `DateTime` | MUSS den Erstellungszeitpunkt angeben ([`META-01`](../08-validation/index.md#rule-meta-01))                                                                                                                                                                                                                                                                                                                                                                                               |
| `modified` | `DateTime` | MUSS den Zeitpunkt der letzten Änderung angeben ([`META-01`](../08-validation/index.md#rule-meta-01)) MUSS >= `created` sein ([`META-03`](../08-validation/index.md#rule-meta-03))                                                                                                                                                                                                                                                                                                                                             |
| `status`   | `Enum`     | MUSS den Status der Regelung angeben ([`META-01`](../08-validation/index.md#rule-meta-01)) MUSS einer der definierten Status-Werte sein ([`META-02`](../08-validation/index.md#rule-meta-02))                                                                                                                                                                                                                                                                                                                                  |

### 3.3.2 Optionale Felder

| **Feld**       | **Typ**         | **Beschreibung**                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`        | `String`        | DARF einen menschenlesbaren Titel der Rulemap enthalten.                                                                                                                                                                                                                                                                                                                                                                                           |
| `description`  | `String`        | DARF eine kurze Beschreibung der Rulemap enthalten.                                                                                                                                                                                                                                                                                                                                                                                                |
| `documentType` | `Enum`          | DARF den Typ des Dokuments klassifizieren. MUSS wenn vorhanden einer der definierten Werte sein ([`META-05`](../08-validation/index.md#rule-meta-05)). Siehe [Abschnitt 3.3.6](3-3-metadata-object.md) für die vollständige Werteliste.                                                                                                                                                                                                                                                 |
| `authors`      | `Array[Object]` | DARF eine Liste von Autoren enthalten. MUSS wenn vorhanden mindestens einen Eintrag enthalten ([`META-06`](../08-validation/index.md#rule-meta-06)). Jedes Objekt MUSS ein `name`-Feld (`String`) enthalten ([`META-06`](../08-validation/index.md#rule-meta-06)). Die Felder `email` (String, RFC 5321) und `organization` (`String`) sind optional. Hinweis: `authors[].organization` bezeichnet die institutionelle Zugehörigkeit des Autors — nicht die herausgebende Organisation des Dokuments (siehe `organization`). |
| `organization` | `String`        | DARF die **herausgebende** Organisation angeben (wer ist institutionell für das Dokument verantwortlich). Hinweis: Unterschied zu `authors[].organization`: Dieses Feld beschreibt die Verantwortung für das Dokument, nicht die Zugehörigkeit einer Einzelperson.                                                                                                                                                                                 |
| `jurisdiction` | `String`        | DARF den Rechtsraum angeben. MUSS mit ISO 3166-1 alpha-2 Ländercode beginnen ([`META-07`](../08-validation/index.md#rule-meta-07)). DARF mit Bindestrichen getrennte Untergliederungen enthalten ([`META-07`](../08-validation/index.md#rule-meta-07)). Format: `"CC"` oder `"CC-XX"` oder `"CC-XX-YY-..."`. Beispiele: `"DE"`, `"DE-BY"`, `"DE-BY-M"`, `"DE-BY-09162"`.                                                                                                                                                     |
| `legalDomain`  | `String`        | DARF das Rechtsgebiet angeben.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `tags`         | `Array[String]` | DARF Kategorisierung/Verschlagwortung enthalten.                                                                                                                                                                                                                                                                                                                                                                                                   |
| `derivedFrom`  | `Object`        | DARF Informationen über die Herkunft enthalten. MUSS bei Arbeitskopien verwendet werden.                                                                                                                                                                                                                                                                                                                                                           |
| `language`     | `String`        | DARF die Sprache angeben. MUSS dem ISO 639-1 Format entsprechen (z.B. `"de"`, `"en"`) ([`META-08`](../08-validation/index.md#rule-meta-08)).                                                                                                                                                                                                                                                                                                                                            |
| `validFrom`    | `DateTime`      | DARF den Gültigkeitsbeginn angeben.                                                                                                                                                                                                                                                                                                                                                                                                                |
| `validUntil`   | `DateTime`      | DARF das Gültigkeitsende angeben. Wenn sowohl `validFrom` als auch `validUntil` gesetzt sind, MUSS `validUntil` > `validFrom` sein ([`META-09`](../08-validation/index.md#rule-meta-09)).                                                                                                                                                                                                                                                                                               |
| `replaces`     | `UUID`          | DARF auf eine ersetzte Version verweisen. DARF zusammen mit `replacedBy` verwendet werden ([`META-04`](../08-validation/index.md#rule-meta-04)).                                                                                                                                                                                                                                                                                                                                        |
| `replacedBy`   | `UUID`          | DARF auf eine Nachfolgeversion verweisen. DARF zusammen mit `replaces` verwendet werden ([`META-04`](../08-validation/index.md#rule-meta-04)).                                                                                                                                                                                                                                                                                                                                          |
| `comment`      | `String`        | DARF einen Freitext-Kommentar zum Dokument enthalten, z. B. den Grund für den Status `suspended`.                                                                                                                                                                                                                                                                                                                                                  |

### 3.3.3 Status-Werte

Der Status einer RUML-Datei MUSS einer der folgenden Werte sein ([`META-02`](../08-validation/index.md#rule-meta-02)):

| **Status**    | **Beschreibung** | **Anforderungen**                                                                                               |
| ------------- | ---------------- | --------------------------------------------------------------------------------------------------------------- |
| `"draft"`     | Entwurf          | KEINE zusätzlichen Anforderungen                                                                                |
| `"review"`    | In Überprüfung   | SOLLTE `authors` gesetzt haben                                                                                  |
| `"approved"`  | Genehmigt        | SOLLTE `organization` gesetzt haben                                                                             |
| `"inForce"`   | In Kraft         | MUSS `validFrom` gesetzt haben ([`META-10`](../08-validation/index.md#rule-meta-10)) SOLLTE `jurisdiction` gesetzt haben                             |
| `"suspended"` | Ausgesetzt       | SOLLTE `validUntil` oder `comment` gesetzt haben                                                                |
| `"expired"`   | Abgelaufen       | MUSS `validUntil` gesetzt haben ([`META-11`](../08-validation/index.md#rule-meta-11)) `validUntil` MUSS in der Vergangenheit liegen ([`META-11`](../08-validation/index.md#rule-meta-11)) |
| `"replaced"`  | Ersetzt          | MUSS `replacedBy` gesetzt haben ([`META-12`](../08-validation/index.md#rule-meta-12))                                                                |

**Zusätzliche Regeln:**

- Der Status MUSS bei jeder inhaltlichen Änderung geprüft werden
- Bei Statuswechsel von `"draft"` zu `"inForce"` MÜSSEN alle Pflichtfelder validiert sein
- Ein Status `"replaced"` DARF NICHT zurück auf einen anderen Status gesetzt werden

**Hinweis: Dokument-Status vs. Knotenstatus**

Die hier definierten Status-Werte (`draft`, `review`, `approved`, `inForce`, `suspended`, `expired`,
`replaced`) beschreiben den **Dokument-Status** der RUML-Datei. Sie werden im `metadata.status`-Feld
gespeichert und beschreiben den Gültigkeitszustand des gesamten Regelwerks.

Diese sind zu unterscheiden vom **Knotenstatus** (`pending`, `true`, `false`, `undefined`,
`ignored`), der zur Laufzeit während der Auswertung berechnet wird. Der Knotenstatus wird NICHT in
der RUML-Struktur gespeichert, sondern ausschließlich in einer separaten RUML-Result-Datei
(`.ruml-result`). Details siehe [Kapitel 5](../05-result-format/index.md).

### 3.3.4 Beispiel Metadata-Objekt

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

**Hinweise:**

- Dieses Beispiel zeigt ein Metadata-Objekt mit Status `"inForce"` und `documentType: "law"`
- Das erforderliche Feld `validFrom` ist gesetzt
- Die optionalen Felder `jurisdiction`, `legalDomain` etc. sind beispielhaft befüllt

- Integritätssicherung (Hashing, Signaturen) erfolgt auf Container-Ebene (siehe
  [Kapitel 7](../07-container/index.md))

### 3.3.5 Arbeitskopien von Dokumenten mit Status `"inForce"`

**Grundprinzip:** Dokumente mit Status `"inForce"` SOLLTEN NICHT verändert werden. Die
Unveränderlichkeit wird durch Signaturen auf Container-Ebene gewährleistet (siehe
[Kapitel 7](../07-container/index.md)). Arbeitskopien MÜSSEN möglich sein.

**Regeln für Arbeitskopien:**

1. **Bei der Erstellung einer Arbeitskopie MUSS:**

- Eine neue UUID vergeben werden
- Der Status auf `"draft"` geändert werden
- Die Herkunft im `derivedFrom`-Objekt dokumentiert werden

1. **Das** `derivedFrom`**-Objekt:**

| **Feld**         | **Typ**    | **Beschreibung**                                                                                                                                           |
| ---------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `originalId`     | `UUID`     | MUSS die ID des Originaldokuments enthalten ([`META-13`](../08-validation/index.md#rule-meta-13))                                                                                               |
| `originalHash`   | `String`   | DARF den Hash des Originaldokuments enthalten ([`META-04`](../08-validation/index.md#rule-meta-04)). Der Hash wird auf Container-Ebene berechnet (siehe [Kapitel 7](../07-container/index.md)). |
| `originalStatus` | `Enum`     | MUSS den Status des Originals zum Zeitpunkt der Kopie enthalten ([`META-13`](../08-validation/index.md#rule-meta-13))                                                                           |
| `derivationType` | `Enum`     | MUSS den Typ angeben: `"workingCopy"`, `"amendment"`, `"revision"` ([`META-13`](../08-validation/index.md#rule-meta-13))                                                                        |
| `derivedAt`      | `DateTime` | MUSS den Zeitpunkt der Kopie-Erstellung enthalten ([`META-13`](../08-validation/index.md#rule-meta-13))                                                                                         |
| `derivedBy`      | `String`   | SOLLTE die erstellende Stelle/Person angeben                                                                                                               |

1. **Validierung bei Arbeitskopien:**

- Das System DARF die Integrität des Originals über den Container-Hash verifizieren (siehe
  [Kapitel 7](../07-container/index.md))
- Das System MUSS sicherstellen, dass die Kopie NICHT als `"inForce"` markiert ist ([`META-14`](../08-validation/index.md#rule-meta-14))
- Das System SOLLTE die Abstammungskette nachvollziehbar machen

**Beispiel einer Arbeitskopie:**

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

**Hinweis:** Diese Struktur ermöglicht es Legisten, mit Kopien rechtskräftiger Dokumente zu
arbeiten. Die Integrität und Unveränderlichkeit der Originale wird durch Signaturen auf
Container-Ebene gewährleistet (siehe [Kapitel 7](../07-container/index.md)).

### 3.3.6 documentType-Werte

Das optionale Feld `documentType` klassifiziert den Dokumenttyp der RUML-Datei. Es MUSS wenn
vorhanden einer der folgenden Werte sein ([`META-05`](../08-validation/index.md#rule-meta-05)):

| **Wert**               | **Beschreibung**                                                                                                                                                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"law"`                | Formelles Gesetz (z.B. EStG, BGB, SGB)                                                                                                                                                                                    |
| `"regulation"`         | Verordnung, Satzung oder verbindliche Regelung — öffentlich-rechtlich (z.B. Durchführungsverordnung) oder privatwirtschaftlich (z.B. interne Unternehmensrichtlinie mit Verbindlichkeitscharakter)                        |
| `"guideline"`          | Leitfaden, Handlungsempfehlung oder nicht-verbindliche Vorgabe — z.B. Verwaltungsvorschrift, Compliance-Leitlinie, Best-Practice-Dokument                                                                                 |
| `"decision"`           | Entscheidungslogik für regelbasierte Bescheide oder Urteile — öffentlich-rechtlich (z.B. Verwaltungsentscheid, Gerichtsurteil) oder privatwirtschaftlich (z.B. Kreditentscheidung, Compliance-Prüfung, Versicherungsfall) |
| `"procedure"`          | Prozess- oder Verfahrensbeschreibung — z.B. Verwaltungsverfahren, Genehmigungsprozess, unternehmensinterner Workflow                                                                                                      |
| `"form"`               | Strukturierter Erfassungs- oder Antragsprozess — z.B. Antragsformular, Onboarding-Prozess, Datenerhebung                                                                                                                  |
| `"documentGeneration"` | Rulemap zur regelbasierten Generierung von Dokumenten — z.B. Bescheide, Verträge, Berichte, Zertifikate. Die Auswertung erzeugt als Ergebnis ein oder mehrere Dokumente.                                                  |
| `"other"`              | Sonstige Dokumenttypen, die keinem der spezifischeren Werte entsprechen                                                                                                                                                   |

**Hinweise:**

- Das Feld `documentType` ist unabhängig vom Feld `legalDomain`: `legalDomain` beschreibt den
  fachlichen Anwendungsbereich (z.B. `"Steuerrecht"`, `"Kreditwesen"`, `"HR-Compliance"`),
  `documentType` beschreibt die Form des Dokuments (z.B. `"decision"`, `"documentGeneration"`)
- Der Wert `"other"` SOLLTE NICHT verwendet werden, wenn einer der spezifischeren Werte passt
- Die Werteliste DARF in zukünftigen Versionen der Spezifikation erweitert werden
- `documentType` ist die **einzige** Klassifikation einer RUML-Datei. Das `rulemap`-Objekt enthält
  bewusst kein `type`-Feld — die Dokument-Klassifikation ist ausschließlich im `metadata`-Objekt
  verortet.

## Konformitätstests

- [3.3 Metadata Object](../../../tests/03-data-model/3-3-metadata-object.test.yaml)
