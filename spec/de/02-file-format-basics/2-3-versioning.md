<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.3 Versionierung

### Format-Version vs. Inhalts-Version

RUML unterscheidet zwei unabhängige Versionsebenen:

| **Ebene**            | **Feld**           | **Beschreibung**                      | **Beispiel**        |
| -------------------- | ------------------ | ------------------------------------- | ------------------- |
| **Format-Version**   | `$specVersion`     | Version der RUML-Spezifikation        | "1.0", "1.1", "2.0" |
| **Dokument-Version** | `metadata.version` | Version des Inhalts dieser RUML-Datei | "2024.1.0", "1.0.0" |

### Semantic Versioning für Format-Version

Die Format-Version folgt Semantic Versioning:

- **MAJOR**: Inkompatible Änderungen (1.0 → 2.0)
- **MINOR**: [Rückwärtskompatible](#das-feld-specversion) Erweiterungen (1.0 → 1.1)
- **PATCH**: Fehlerkorrekturen in der Spezifikation (1.0.0 → 1.0.1)

:::note[Rückwärtskompatibilität]
Innerhalb einer MAJOR-Version halten neue Versionen der Spezifikation die Schemas und das
Auswertungsverhalten rückwärtskompatibel: RUML-Dateien, RUML-Ext-Dateien und RUML-Ergebnisdateien,
die nach einer Version gültig sind, bleiben nach späteren MINOR- und PATCH-Versionen gültig, und
eine RUML-Datei wird zusammen mit ihren RUML-Ext-Dateien zum selben Ergebnis ausgewertet. Nur eine
neue MAJOR-Version kann das brechen.
:::

### Das Feld `$specVersion`

Das Feld `$specVersion` besteht nur aus MAJOR und MINOR; eine Änderung der PATCH-Version ändert es
nicht. Es gibt die Version der Spezifikation an, der die Datei entspricht. Die Schemas listen die
Versionen, die eine Datei angeben darf, im `enum` von `$specVersion` ([`FMT-04`](../08-validation/index.md#rule-fmt-04)).

Die Version eines Parsers oder Evaluators ist die höchste Version der Spezifikation, die er
implementiert.

Anforderungen an Parser:

- Ein Parser MUSS eine Datei akzeptieren, deren `$specVersion` seine MAJOR-Version und eine
  MINOR-Version bis zu seiner eigenen hat ([`FMT-09`](../08-validation/index.md#rule-fmt-09)).
- Ein Parser MUSS eine Datei, deren `$specVersion` eine höhere MINOR-Version oder eine andere
  MAJOR-Version hat, mit einer klaren Fehlermeldung ablehnen ([`FMT-09`](../08-validation/index.md#rule-fmt-09)).

Anforderungen an Evaluatoren:

- Die Eingabeversion einer Auswertung ist die höchste `$specVersion` unter der RUML-Datei und ihren
  RUML-Ext-Dateien.
- Hat die Eingabeversion eine frühere MINOR-Version als ihre eigene, MÜSSEN Evaluatoren dasselbe
  Ergebnis liefern wie ein Evaluator, der die Eingabeversion implementiert.
- Das Ergebnis MUSS die Eingabeversion als `$specVersion` haben, nicht die Version des Evaluators.
