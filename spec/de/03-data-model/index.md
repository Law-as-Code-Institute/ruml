<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 03. Datenmodell

Dieses Kapitel ist der strukturelle Kern der Spezifikation. Es definiert die flache Knoten-Map, die
eine Rulemap trägt, die Felder jedes Knotens und die Operatoren, die Kindergebnisse verknüpfen.
Alles, was Capabilities später ergänzen, setzt an den hier definierten Objekten an.

- [3.1 Architekturprinzipien](3-1-architecture-principles.md) — Flache Map, Key als Identifikator,
  keine abgeleiteten Zustände in der Datei
- [3.2 Datentypen und Formate](3-2-data-types-and-formats.md) — Zeitstempel, Hashes, UUIDs und die
  Map-Strukturen
- [3.3 Metadata-Objekt](3-3-metadata-object.md) — Dokumentidentität, Status, Gültigkeit und
  Urheberschaft
- [3.4 Rulemap-Objekt](3-4-rulemap-object.md) — Die `nodes`-Map und ihr Wurzeleintrag
- [3.5 Node-Objekt](3-5-node-object.md) — Pflicht- und optionale Knotenfelder, Unterscheidung
  Parent/Leaf
- [3.6 Operatoren](3-6-operators.md) — `AND`, `OR`, `XOR` und ihre negierten Formen
- [3.7 Strukturbeispiel](3-7-structure-example.md) — Eine vollständige, kommentierte Rulemap
- [3.8 Integritätsvalidierung](3-8-integrity-validation.md) — Strukturprüfungen über die Knoten-Map
  hinweg
