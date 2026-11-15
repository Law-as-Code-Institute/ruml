<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.6 Parser-Pflichten

Die Pflichten von Parsern und Werkzeugen, die RUML- oder RUML-EXT-Dateien verarbeiten, sind in den
Kapiteln definiert, die sie betreffen, und mit Verweisen auf diese Kapitel in
[Kapitel 8](../08-validation/index.md) katalogisiert; die Parser-Pflichten des Capability-Systems
stehen in [Kapitel 8.7](../08-validation/index.md#87-regeln-zu-capabilities). Dieser Abschnitt
ergänzt die Reihenfolge, in der ein Parser eine Datei liest. Diese Reihenfolge ist von außen nicht
beobachtbar und hat deshalb keine Regel-ID.

Die Reihenfolge der Capability-Einträge eines Knotens ist in
[Kapitel 4.3](4-3-capabilities-node-field.md#reihenfolge-der-felder) definiert; an der Root ist sie
nicht signifikant.

### Frühzeitiges Lesen des `capabilities`-Arrays

Ein Parser MUSS das `capabilities`-Array lesen und auswerten, **bevor** er die `rulemap` oder andere
strukturelle Felder der Datei verarbeitet. Dies sichert das Fail-Fast-Verhalten für
`required: true`-Capabilities.

:::note[Empfohlene Parse-Reihenfolge]
1. `$format` und `$specVersion` lesen und validieren
2. `capabilities`-Array lesen und für jede Capability prüfen, ob sie bekannt ist
3. Bei unbekannter `required: true`-Capability: Abbruch
4. Restliche Felder verarbeiten
:::

### Hinweis zu Werkzeug-Implementierungen

:::warning[Validierungswerkzeuge]
Ein Validierungswerkzeug MUSS jede Regel der Ebenen Schema und semantisch in
[Kapitel 8](../08-validation/index.md) prüfen ([`CAP-28`](../08-validation/index.md#rule-cap-28)). Ein Werkzeug, das nur die
Kernstruktur prüft und das `capabilities`-System ignoriert, ist kein vollständiger RUML-Validator.
:::
