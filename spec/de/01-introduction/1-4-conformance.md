<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.4 Konformität

Diese Spezifikation definiert Konformität für vier Rollen: RUML-Dateien, RUML-Parser, RUML-Producer
und RUML-Evaluatoren.

### Konforme RUML-Datei

Eine RUML-Datei ist konform, wenn sie:

- die strukturellen Anforderungen aus Kapitel 2 und 3 erfüllt,
- die Anforderungen an die referenzielle Integrität für alle deklarierten Capabilities
  ([Kapitel 4](../04-capabilities/index.md)) erfüllt,
- die in dieser Spezifikation definierten Invarianten einhält.

Eine Datei, die zusammen mit einem Sidecar (`.ruml-ext`) oder einem Auswertungsergebnis
(`.ruml-result`) ausgeliefert wird, MUSS zusätzlich den jeweiligen Formatdefinitionen aus
[Kapitel 4.5](../04-capabilities/4-5-ruml-ext.md) und [Kapitel 5](../05-result-format/index.md)
entsprechen.

### Konformer Parser

Ein Parser ist konform, wenn er:

- jede konforme RUML-Datei fehlerfrei liest, deren `$specVersion` er akzeptiert
  ([Kapitel 2.3](../02-file-format-basics/2-3-versioning.md)) und deren erforderliche Capabilities
  er umsetzt,
- die strukturelle Validierung gemäß [Kapitel 2.6](../02-file-format-basics/2-6-file-validation.md)
  und [Kapitel 3.8](../03-data-model/3-8-integrity-validation.md) durchführt,
- das `capabilities`-Array zuerst liest, wie
  [Kapitel 4.6](../04-capabilities/4-6-parser-obligations.md) es verlangt, und die Parser-Pflichten
  umsetzt, die in [Kapitel 8.7](../08-validation/index.md#87-regeln-zu-capabilities) katalogisiert
  sind,
- das RUML Container Format gemäß [Kapitel 7.6](../07-container/7-6-processing.md) verarbeitet, wenn
  ein Container vorliegt,
- jede Datei zurückweist, die eine Capability mit `required: true` enthält, die er nicht unterstützt
  ([`CAP-01`](../08-validation/index.md#rule-cap-01)).

Ein Parser DARF zusätzlich capability-spezifische Verarbeitung für jede ihm bekannte Capability
implementieren. Die capability-spezifischen Verarbeitungsregeln stehen in der jeweiligen
Capability-Spezifikation.

### Konformer Producer

Ein Producer ist konform, wenn er:

- ausschließlich Dateien erzeugt, die im obigen Sinne konform sind,
- `$specVersion` auf eine Version setzt, die er tatsächlich umsetzt,
- nie einen `undefined`-Operator in einem anderen Status als `draft` ausgibt,
- jede verwendete Capability im Root-`capabilities`-Array deklariert.

### Konformer Evaluator

Ein Evaluator ermittelt das Ergebnis einer Rulemap. Ein Evaluator ist konform, wenn er:

- ein konformer Parser ist,
- die Operatoren so auswertet, wie [Kapitel 3.6](../03-data-model/3-6-operators.md) es festlegt, und
  modulare Knoten so, wie [Kapitel 6](../06-modular-nodes/index.md) es festlegt,
- jede decision-Capability, die er umsetzt, so auswertet, wie die Spezifikation dieser Capability es
  festlegt,
- ein Ergebnis schreibt, das [Kapitel 5](../05-result-format/index.md) entspricht und die Version
  trägt, die [Kapitel 2.3](../02-file-format-basics/2-3-versioning.md) verlangt.

### Validierungswerkzeug

Ein Validierungswerkzeug ist ein konformer Parser, der zusätzlich jede Regel des Katalogs in
[Kapitel 8](../08-validation/index.md) prüft, deren Ebene `schema` oder `semantic` ist
([`CAP-28`](../08-validation/index.md#rule-cap-28)).

### Konformitätsstufen

Diese Spezifikation definiert keine mehrstufige Konformität. Eine Datei, ein Parser, ein Producer
oder ein Evaluator ist entweder konform oder nicht.
