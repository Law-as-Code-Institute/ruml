<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 3.1 Architekturprinzipien

Das RUML-Datenmodell definiert die Struktur für maschinenlesbare Regelwerke und Entscheidungslogik.
Die Architektur basiert auf einer hierarchischen **Eltern-zu-Kind-Beziehung**, bei der jeder Knoten
ausschließlich Informationen über seine direkten Kinder speichert.

## 3.1 Grundlegende Architekturprinzipien

**Die RUML-Architektur MUSS diesen fundamentalen Prinzipien folgen:**

1. **Unidirektionale Beziehungen:** Knoten **DÜRFEN KEINE** anderen Knoten als ihre direkten Kinder
   kennen. Knoten **DÜRFEN KEINE** Informationen über ihre Parent-Knoten speichern ([`NODE-03`](../08-validation/index.md#rule-node-03)).
2. **Ein Operator pro Knoten:** Jeder Parent-Knoten **MUSS** genau EINEN Operator-Typ haben, der für
   ALLE seine direkten Kinder gilt.
3. **Geordnete Hierarchie:** Die Reihenfolge der Kinder im children-Array der Parent-Knoten **MUSS**
   signifikant sein und **MUSS** bei der Ausführungslogik berücksichtigt werden ([`NODE-04`](../08-validation/index.md#rule-node-04)).
4. **LexID als primärer Identifikator:** Knoten **MÜSSEN** innerhalb der RUML über numerische LexIDs
   identifiziert werden ([`FMT-11`](../08-validation/index.md#rule-fmt-11)).
5. **Flache Map-Struktur:** Alle Knoten **MÜSSEN** in einem zentralen `nodes`-Objekt definiert
   werden ([`NODE-02`](../08-validation/index.md#rule-node-02)). Eltern-Kind-Beziehungen **MÜSSEN** über LexID-Referenzen im
   `children`-Array hergestellt werden, NICHT durch eingebettete Objekte ([`FMT-11`](../08-validation/index.md#rule-fmt-11)). Dies
   ermöglicht die Mehrfach-Referenzierung derselben LexID für modulare Knoten (siehe
   [Kapitel 6](../06-modular-nodes/index.md)).
