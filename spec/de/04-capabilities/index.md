<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 04. Capabilities

Dieses Kapitel definiert den Erweiterungsmechanismus von RUML: das **Capabilities-System**.

Capabilities ermöglichen es, RUML-Dateien mit optionalen oder proprietären Funktionalitäten
anzureichern, ohne die Kernspezifikation zu verändern. Parser können unbekannte Capabilities sicher
ablehnen (wenn erforderlich) oder ignorieren (wenn optional) — stille Datenverluste oder unbemerkte
Korruption werden ausgeschlossen.

---

### Abschnitte dieses Kapitels

| Abschnitt                                                        | Inhalt                                                                       |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [4.1 Konzept](4-1-concept.md)                                    | Motivation, Design-Philosophie, Liefermodi                                   |
| [4.2 Capability-Deklaration](4-2-capabilities-field.md)          | Root-Level-Deklaration, Eintragsformat, Parser-Pflichten                     |
| [4.3 Capability-Daten am Knoten](4-3-capabilities-node-field.md) | Node-Level-Erweiterungsdaten, referenzielle Integrität                       |
| ~~4.4 RUML-Container-Format~~                                    | Verschoben nach [Kapitel 7](../07-container/index.md)                        |
| [4.4 Namensräume](4-4-namespaces.md)                             | Capability-ID-Konventionen, Präfix-Tabelle, Syntaxregeln                     |
| [4.5 RUML-EXT-Format](4-5-ruml-ext.md)                           | Sidecar-Datei `.ruml-ext`, `$base`-Referenz, Hash-Verifizierung              |
| [4.6 Parser-Pflichten](4-6-parser-obligations.md)                | Lesereihenfolge und Anforderungen an Validierungswerkzeuge                   |
| [4.7 `ruml:datapoints`](4-7-data-points.md)                      | Typisierte Datenpunkt-Definitionen als Capability                            |
| [4.8 `ruml:query`](4-8-ruml-query.md)                            | Datenbasierte Query-Expressions als Capability                               |
| [4.9 `ruml:ai-query`](4-9-ruml-ai-query.md)                      | KI-gestützte Entscheidungen als Capability                                   |
| [4.10 `ruml:actions`](4-10-ruml-actions.md)                      | Actions als Capability                                                       |
| [4.11 `ruml:context`](4-11-ruml-context.md)                      | Context-Materialien als Capability                                           |
| [4.12 `ruml:text-reference`](4-12-ruml-text-reference.md)        | Normative Textreferenzen als Capability                                      |
| [4.13 `ruml:protocol`](4-13-ruml-protocol.md)                    | Auswertungsprotokoll (Audit-Trail) als Capability                            |
| [4.14 `ruml:expression`](4-14-ruml-expression.md)                | Verknüpfungsausdruck für den Operator `DELEGATED`                            |
| [4.15 `ruml:tree-reference`](4-15-ruml-tree-reference.md)        | Verweise auf Knoten und Teilbäume anderer RUML-Dateien als Capability        |
| [4.16 `ruml:tree-include`](4-16-ruml-tree-include.md)            | Auswertung eines Knotens einer anderen RUML-Datei an Stelle eines Leaf-Nodes |
