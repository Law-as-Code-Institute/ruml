<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.1 Anwendungsbereich

RUML (Rulemapping Logic Format) ist ein offenes, JSON-basiertes Dateiformat zur maschinenlesbaren
Darstellung von Entscheidungslogik über normative Texte.

### Gegenstand dieser Spezifikation

Diese Spezifikation definiert:

- Die Struktur einer RUML-Datei (Kapitel 2–3) — JSON-Aufbau, Identifikator-Systeme, Metadaten-Felder
  und das hierarchische Node-Modell mit seinen Operatoren.
- Den Capability-Erweiterungsmechanismus (Kapitel 4) — Deklaration, Transport und Validierung
  optionaler oder proprietärer Funktionalität.
- Das RUML Result Format (Kapitel 5) — das separate Dateiformat für Auswertungsergebnisse.
- Den Mechanismus modularer Nodes (Kapitel 6) — Node-Wiederverwendung an mehreren Positionen
  einschließlich rekursiver Strukturen.
- Das RUML Container Format (Kapitel 7) — Verpackung für Integritätssicherung, digitale Signaturen
  und Verschlüsselung.
- Die Validierungsanforderungen für konforme Parser (Kapitel 8).

### Nicht Gegenstand dieser Spezifikation

Diese Spezifikation definiert nicht:

- Laufzeit-Auswertungsalgorithmen jenseits dessen, was das Datenmodell verlangt.
- Tool-Verhalten jenseits der festgelegten Konformanzregeln.
- Deployment-, Distributions- oder Speicher-Infrastruktur.
- Governance-Modelle, Zertifizierungsverfahren oder organisatorische Prozesse rund um RUML-Dateien.
- Die Motivation, Anwendbarkeit oder den Nutzen von RUML in bestimmten Domänen oder Organisationen.

### Two-Layer Model

| Schicht                             | Inhalt                                                                                                                      | Zweck                                                                         |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **RUML Core** (Kapitel 2–3)         | Entscheidungsbaum, Operatoren, Labels, Metadaten                                                                            | Strukturelle Abbildung von Regelwerken                                        |
| **RUML + Capabilities** (Kapitel 4) | Offizielle `ruml:`-Capabilities (siehe [Kapitel 4.4](../04-capabilities/4-4-namespaces.md)) und Drittanbieter-Erweiterungen | Entscheidungsfindung, Ausführung, Materialien und Drittanbieter-Erweiterungen |

Der RUML Core ist **strukturell autark**: Eine RUML-Datei ohne Capabilities enthält alle
Informationen zur Darstellung der Regelstruktur und ihrer normativen Textverankerung. Die Anwendung
einer Rulemap auf einen konkreten Sachverhalt — also das Bereitstellen von Eingangsdaten, die
Auswertung von Leaf-Node-Bedingungen und das Auslösen von Actions — wird durch Capabilities
(Kapitel 4) und die Laufzeitumgebung ermöglicht.
