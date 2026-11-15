<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.1 Allgemeine Eigenschaften

### Dateiendung

- **Primär**: `.ruml`
- **Auswertungsergebnisse**: `.ruml-result` (siehe [Abschnitt 2.2](2-2-file-structure.md))
- **Capability-Erweiterungen**: `.ruml-ext` (siehe
  [Kapitel 4.5](../04-capabilities/4-5-ruml-ext.md))
- **Container**: `.rumlc` (ZIP, siehe [Kapitel 7](../07-container/index.md)) — für Komprimierung,
  Signatur und Verschlüsselung

### MIME-Type

- **Aktuell**: `application/x-ruml`
- **Zukünftig** (nach IANA-Registrierung): `application/vnd.rulemapping.ruml+json`

### Zeichenkodierung

- **MUSS**: UTF-8 ([`FMT-01`](../08-validation/index.md#rule-fmt-01))
- Andere Kodierungen sind NICHT erlaubt

### JSON-Konformität

- RUML-Dateien MÜSSEN valides JSON gemäß [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) sein
  ([`FMT-02`](../08-validation/index.md#rule-fmt-02))
- Pretty-printing mit Einrückung wird EMPFOHLEN für menschliche Lesbarkeit
- Kompakte Darstellung (minified) ist erlaubt
- Kanonische Darstellung MUSS RFC 8785 für Hash-Berechnung auf Container-Ebene folgen (siehe
  [Kapitel 7](../07-container/index.md))

### Dateigrößen

- Keine inhärenten Größenbeschränkungen
- Implementierungen SOLLTEN mit Dateien bis 100 MB umgehen können
- Für größere Dateien wird Komprimierung EMPFOHLEN

## Konformitätstests

- [2.1 General Properties](../../../tests/02-file-format-basics/2-1-general-properties.test.yaml)
