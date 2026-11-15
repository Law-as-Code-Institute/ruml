<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 2.6 Dateivalidierung

## 2.6 Datei-Validierung

Die Struktur einer RUML-Datei definiert das JSON Schema
[`ruml.schema.json`](../../../schemas/ruml.schema.json)
([Draft 2020-12](https://json-schema.org/draft/2020-12)).

### Beim Laden einer RUML-Datei MUSS:

1. **Format-Prüfung**:

- `$format` MUSS "RUML" sein ([`FMT-03`](../08-validation/index.md#rule-fmt-03))
- `$specVersion` MUSS unterstützte Version sein ([`FMT-04`](../08-validation/index.md#rule-fmt-04), [`FMT-09`](../08-validation/index.md#rule-fmt-09))

2. **Struktur-Prüfung**:

- Alle Pflichtfelder MÜSSEN vorhanden sein
- Datentypen MÜSSEN den Spezifikationen aus Kapitel 3.2 entsprechen ([`FMT-13`](../08-validation/index.md#rule-fmt-13))

3. **Hash-Verifikation** (nur bei Verwendung des Container-Formats):

- Hash-Prüfung erfolgt auf Container-Ebene (siehe [Kapitel 7](../07-container/index.md))
- Bei vorhandenem Hash MUSS dieser verifiziert werden; bei Abweichung MUSS die Verarbeitung
  verweigert werden

**Identifikator-Prüfung**:

- LexIDs **MÜSSEN** eindeutig sein; ein wiederverwendeter modularer Knoten hat genau einen
  `nodes`-Eintrag ([`FMT-12`](../08-validation/index.md#rule-fmt-12))
- UUIDs **MÜSSEN** dem Pattern entsprechen ([`FMT-10`](../08-validation/index.md#rule-fmt-10))
- Das `nodes`-Objekt **MUSS** einen Eintrag mit Key `"1"` (Root-Node) enthalten ([`FMT-08`](../08-validation/index.md#rule-fmt-08))

### Validierung von RUML-EXT-Dateien

Beim Laden einer RUML-EXT-Datei (`.ruml-ext`, `$format: "RUML-EXT"`) MUSS ein Validator zusätzlich
prüfen:

1. **Referenzielle Integrität von `$base`**: Die `$base.id` MUSS mit der `metadata.id` der
   referenzierten Basis-RUML-Datei übereinstimmen, und `$base.hash` MUSS dem aktuellen Hash der
   Basis-Datei entsprechen ([`CAP-24`](../08-validation/index.md#rule-cap-24)).
2. **UUID-Existenz**: Jede UUID im `nodes`-Objekt der EXT-Datei MUSS in der Basis-RUML-Datei
   existieren. UUIDs ohne korrespondierende Knoten in der Basis-Datei MÜSSEN als Fehler behandelt
   werden ([`CAP-26`](../08-validation/index.md#rule-cap-26)).

Siehe [Kapitel 4.5](../04-capabilities/4-5-ruml-ext.md) für die vollständige RUML-EXT-Spezifikation.
