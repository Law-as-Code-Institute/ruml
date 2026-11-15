<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.1 Konzept

Modulare Knoten sind wiederverwendbare Strukturen innerhalb einer Rulemap – entweder einzelne
Endknoten oder Knoten mit Kindern (Teilbäume). Ein modularer Knoten existiert genau einmal im
`nodes`-Objekt und wird an mehreren Stellen der Rulemap wiederverwendet. Wann ein Knoten modular
ist, legt [6.2](6-2-implementation.md#definition-modularer-knoten) fest.

**Anwendungsfälle:**

- **Wiederverwendbare Prüfungen:** Ein Prüf-Teilbaum wird an mehreren Stellen der Rulemap eingesetzt
  — zentral definiert, konsistent und wartungseffizient
- **Standardisierte Teilprozesse:** Häufig benötigte Entscheidungslogiken müssen nur einmal
  definiert werden
- **Rekursive Strukturen:** Zyklen wie Angebot → Ablehnung → neues Angebot können beliebig oft
  durchlaufen werden
