<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 06. Modulare Knoten

Ein modularer Knoten wird einmal definiert und an mehreren Stellen im Baum referenziert, sodass ein
Teilbaum, von dem mehrere Regeln abhängen, nur an einer Stelle gepflegt wird. Dieses Kapitel
definiert, wie solche Knoten deklariert werden, wie sie ausgewertet werden, wenn sie über mehrere
Pfade erreicht werden, und welche Grenzen eine Rulemap endlich halten.

- [6.1 Konzept](6-1-concept.md) — Was ein modularer Knoten ist und wann er sich anbietet
- [6.2 Implementierung](6-2-implementation.md) — `modular: true` deklarieren und referenzieren
- [6.3 Auswertung und Kopierverhalten](6-3-evaluation.md) — Warum Ergebnisse über den Pfad und nicht
  über die LexID indiziert werden
- [6.4 Rekursion](6-4-recursion.md) — Selbstreferenz, die dafür nötigen Operatoren und Terminierung
- [6.5 Verschachtelung](6-5-nesting.md) — Modulare Knoten in modularen Knoten
