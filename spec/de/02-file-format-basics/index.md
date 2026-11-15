<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 02. Dateiformat Grundlagen

Dieses Kapitel definiert, was eine Datei zu einer RUML-Datei macht: ihre Kodierung, die Felder jedes
Root-Objekts sowie die Regeln zu Versionierung, Integrität und Identifikatoren. Das Datenmodell
hinter diesen Feldern folgt in [Kapitel 3](../03-data-model/index.md).

- [2.1 Allgemeine Eigenschaften](2-1-general-properties.md) — Kodierung, JSON-Wohlgeformtheit,
  Dateiendungen
- [2.2 Dateistruktur Übersicht](2-2-file-structure.md) — Das Root-Objekt: `$format`, `$specVersion`,
  `metadata`, `rulemap`
- [2.3 Versionierung](2-3-versioning.md) — Spezifikationsversion und Dokumentversion und ihr
  Unterschied
- [2.4 Integritätssicherung](2-4-integrity.md) — Hash-Algorithmen und kanonische Repräsentation
- [2.5 Identifikator-System](2-5-identifier-system.md) — LexIDs als Map-Keys, UUIDs als globale
  Identifikatoren
- [2.6 Dateivalidierung](2-6-file-validation.md) — Welche Prüfungen ein Validator vornimmt und in
  welcher Reihenfolge
