<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 05. RUML-Result-Format

Auswertungsergebnisse MÜSSEN in einer eigenständigen RUML-Result-Datei (`.ruml-result`) gespeichert
werden. Beim Laden einer RUML-Result-Datei werden Actions **NICHT** erneut ausgelöst — das
gespeicherte Ergebnis dient ausschließlich der Dokumentation.

Dieses Kapitel beschreibt das Format der RUML-Result-Datei (`.ruml-result`), in der
Auswertungsergebnisse einer Rulemap gespeichert werden. Ihre Struktur definiert das JSON Schema
[`ruml-result.schema.json`](../../../schemas/ruml-result.schema.json)
([Draft 2020-12](https://json-schema.org/draft/2020-12)).

- [5.0 Knotenstatus](5-0-status-types.md) — Die möglichen Knotenstatus (`true`, `false`,
  `undefined`, `ignored`)
- [5.1 Ergebnismodell und Speicherung](5-1-result-model.md) — RUML-Result-Datei,
  Integritätssicherung und Beispiele
