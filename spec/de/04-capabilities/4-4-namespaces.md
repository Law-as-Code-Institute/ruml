<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.4 Namensräume für Capability-IDs

### Zweck

Capability-IDs MÜSSEN global eindeutig sein, um Kollisionen zwischen Capabilities verschiedener
Anbieter zu verhindern. Ein Namensraum-Mechanismus auf Basis von Präfixen stellt diese Eindeutigkeit
sicher.

Jede Capability-ID besteht aus einem **Präfix** und einem **lokalen Namen**, getrennt durch ein
definiertes Trennzeichen.

### Präfix-Tabelle

| Präfix              | Trennzeichen | Eigentümer                 | Normativität       | Beschreibung                                                        |
| ------------------- | ------------ | -------------------------- | ------------------ | ------------------------------------------------------------------- |
| `ruml:`             | `:`          | RUML-Spezifikationsgremium | Normativ           | Offizielle Capabilities der RUML-Spezifikation — reserviert         |
| `ruml:draft/`       | `:` + `/`    | RUML-Spezifikationsgremium | Experimentell      | Experimentelle Capabilities; DÜRFEN sich ohne Vorankündigung ändern |
| `<reverse-domain>/` | `.` + `/`    | Drittanbieter              | Anbieterspezifisch | Beliebige Drittanbieter nach Reverse-Domain-Konvention              |

Ein Parser MUSS prüfen, ob jede Capability-ID einem dieser Präfixe entspricht. Eine ID ohne
erkennbares Präfix-Muster MUSS er als Fehler behandeln ([`CAP-21`](../08-validation/index.md#rule-cap-21)).

:::warning[Namensraum-Reservierung]
Der Präfix `ruml:` ist **reserviert**. Drittanbieter DÜRFEN diesen Präfix NICHT für eigene
Capabilities verwenden. Ein Parser MUSS eine Datei ablehnen, die eine `ruml:`-ID enthält, die weder
in dieser Spezifikationsversion definiert noch eine `ruml:draft/`-ID ist, unabhängig vom Wert von
`required`.
:::

### Offizielle Capabilities (`ruml:`)

Capabilities unter dem Präfix `ruml:` (ohne `draft/`) sind Teil der RUML-Spezifikation. Sie MÜSSEN
in einem offiziellen Capability-Register dokumentiert sein und folgen den Versionsregeln der
Spezifikation (siehe [Kapitel 2.3](../02-file-format-basics/2-3-versioning.md)).

#### Offizielles Capability-Register

Die folgenden `ruml:`-Capabilities sind in der aktuellen Spezifikation definiert:

| Capability-ID         | Scope                     | Beschreibung                                                                | Spezifikation                               |
| --------------------- | ------------------------- | --------------------------------------------------------------------------- | ------------------------------------------- |
| `ruml:datapoints`     | Root (`data`)             | DataPoints-Schema (Datendefinitionen) und Binding-Hints                     | [Kapitel 4.7](4-7-data-points.md)           |
| `ruml:query`          | Node                      | Datenbasierte Query-Expression (Leaf-Nodes)                                 | [Kapitel 4.8](4-8-ruml-query.md)            |
| `ruml:ai-query`       | Node                      | KI-gestützte Entscheidungen (LLM-basiert)                                   | [Kapitel 4.9](4-9-ruml-ai-query.md)         |
| `ruml:actions`        | Node                      | Actions-Objekte auf beliebigen Knoten (Reaktionen auf Status)               | [Kapitel 4.10](4-10-ruml-actions.md)        |
| `ruml:context`        | Root (`data`) + Node      | Context-Map (Kontextmaterialien) und Node-Referenzen                        | [Kapitel 4.11](4-11-ruml-context.md)        |
| `ruml:text-reference` | Root (`data`) + Node      | Texts-Map (Rechtstexte/Normen) und Node-Referenzen                          | [Kapitel 4.12](4-12-ruml-text-reference.md) |
| `ruml:protocol`       | Root (Deklaration)        | Auswertungsprotokoll (Audit-Trail) in der Result-Datei                      | [Kapitel 4.13](4-13-ruml-protocol.md)       |
| `ruml:expression`     | Root (Deklaration) + Node | Verknüpfungsausdruck für den Operator `DELEGATED` (Parent-Nodes)            | [Kapitel 4.14](4-14-ruml-expression.md)     |
| `ruml:tree-reference` | Root (Deklaration) + Node | Verweise auf Knoten anderer RUML-Dateien und deren Teilbäume                | [Kapitel 4.15](4-15-ruml-tree-reference.md) |
| `ruml:tree-include`   | Root (Deklaration) + Node | Wertet einen Knoten einer anderen RUML-Datei an Stelle eines Leaf-Nodes aus | [Kapitel 4.16](4-16-ruml-tree-include.md)   |

### Experimentelle Capabilities (`ruml:draft/`)

Capabilities unter dem Präfix `ruml:draft/` befinden sich im Entwurfsstadium:

- DÜRFEN sich in Name, Struktur oder Semantik ohne Vorankündigung ändern.
- SOLLTEN in produktiven Dateien NICHT mit `required: true` verwendet werden.
- DÜRFEN in zukünftigen Versionen in offizielle `ruml:`-Capabilities überführt oder verworfen
  werden.

:::note[Upgrade-Pfad]
Wenn eine `ruml:draft/`-Capability stabil wird, erhält sie eine neue ID ohne `draft/`. Dateien, die
die Draft-Capability verwenden, müssen manuell migriert werden.
:::

### Drittanbieter-Capabilities (Reverse-Domain)

Alle Capabilities außerhalb des `ruml:`-Namensraums folgen der Reverse-Domain-Konvention:

```
com.example/review-notes
io.acme.legaltools/citation-style
org.myproject/custom-operator
```

Das Format ist: `<reverse-domain>/<lokaler-name>`

- Der Reverse-Domain-Teil MUSS eine gültige Domain-Hierarchie widerspiegeln, deren Eigentümerschaft
  beim Anbieter liegt.
- Der lokale Name MUSS mindestens ein Zeichen lang sein.
- Der Eintrag auf Root-Level MUSS die Rolle deklarieren, die die Rulemap von der Capability erwartet
  (siehe [Kapitel 4.1](4-1-concept.md); [`CAP-03`](../08-validation/index.md#rule-cap-03)). Ein Parser, der die Capability
  implementiert, weist die Datei zurück, wenn die deklarierte Rolle von seiner Implementierung
  abweicht ([`CAP-04`](../08-validation/index.md#rule-cap-04)).

### Syntaxregeln

| Regel                 | Beschreibung                                                                                        |
| --------------------- | --------------------------------------------------------------------------------------------------- |
| Zeichensatz           | Erlaubt: `[a-z0-9_-]`, dazu die Trennzeichen aus der Präfix-Tabelle und `/` (als Hierarchietrenner) |
| Mindestlänge          | Mindestens 1 Zeichen                                                                                |
| Maximallänge          | DARF 128 Zeichen NICHT überschreiten                                                                |
| Groß-/Kleinschreibung | Nur Kleinbuchstaben; Großbuchstaben sind NICHT erlaubt                                              |
| Leerzeichen           | NICHT erlaubt                                                                                       |

### Erlaubte und verbotene Beispiele

```
// GÜLTIG
"ruml:query"
"ruml:draft/ai-annotations"
"com.example/review-notes"
"com.example/priority"
"io.acme/v2/legal-refs"
"de.justiz.nrw/aktenzeichen"

// UNGÜLTIG — Leerzeichen
"com.example/my capability"

// UNGÜLTIG — Großbuchstaben
"com.example/Review-Notes"

// UNGÜLTIG — reservierter Präfix für Drittanbieter
"ruml:my-vendor-extension"

// UNGÜLTIG — keine Domain, kein Trennzeichen
"layout"
"myextension"

// UNGÜLTIG — leerer lokaler Name
"com.example/"
```
