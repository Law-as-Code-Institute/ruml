<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 1.3 Terminologie

Dieser Abschnitt definiert die in dieser Spezifikation verwendeten Begriffe. Jeder Begriff ist hier
zusammengefasst; die normative Definition steht im jeweils zitierten Kapitel.

### Rollen

| Begriff                       | Definition                                                         | Definiert in              |
| ----------------------------- | ------------------------------------------------------------------ | ------------------------- |
| **Parser**                    | Software, die eine RUML-Datei liest.                               | [1.4](1-4-conformance.md) |
| **Producer**                  | Software, die eine RUML-Datei schreibt.                            | [1.4](1-4-conformance.md) |
| **Evaluator**                 | Software, die das Ergebnis einer Rulemap ermittelt.                | [1.4](1-4-conformance.md) |
| **Validierungswerkzeug**      | Ein Parser, der jede Regel der Ebenen Schema und semantisch prüft. | [1.4](1-4-conformance.md) |
| **Werkzeug, Implementierung** | Software in einer dieser Rollen.                                   | [1.4](1-4-conformance.md) |

### Identifikatoren

| Begriff   | Definition                                                                                   | Definiert in                                                                                |
| --------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **LexID** | Identifikator eines Nodes innerhalb einer RUML-Datei: positive Ganzzahl, als String kodiert. | [2.5](../02-file-format-basics/2-5-identifier-system.md#lexid-lexical-identifier)           |
| **UUID**  | Global eindeutiger Identifikator (UUID v4) einer RUML-Datei (`metadata.id`) und jedes Nodes. | [2.5](../02-file-format-basics/2-5-identifier-system.md#uuid-universally-unique-identifier) |

### Strukturelemente

| Begriff          | Definition                    | Definiert in                                                                 |
| ---------------- | ----------------------------- | ---------------------------------------------------------------------------- |
| **Node**         | Element der RUML-Hierarchie.  | [3.5](../03-data-model/3-5-node-object.md)                                   |
| **Root-Node**    | Oberster Node, mit LexID `1`. | [3.5.1](../03-data-model/3-5-node-object.md#351-knotentypen-nach-rolle)      |
| **Parent-Node**  | Node mit `children`.          | [3.5.1](../03-data-model/3-5-node-object.md#351-knotentypen-nach-rolle)      |
| **Leaf-Node**    | Node ohne `children`.         | [3.5.1](../03-data-model/3-5-node-object.md#351-knotentypen-nach-rolle)      |
| **Modular-Node** | Wiederverwendbarer Node.      | [6.2](../06-modular-nodes/6-2-implementation.md#definition-modularer-knoten) |

### Normative Textverankerung

| Begriff          | Definition                                                                                                                                                                                  | Definiert in                                                            |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Anker**        | Verweis eines Knotens auf einen Text derselben RUML-Datei oder eines seiner Elemente: die Norm, die der Knoten umsetzt (`represents`), oder ein Text, auf den er sich stützt (`refers-to`). | [4.12](../04-capabilities/4-12-ruml-text-reference.md#node-level-anker) |
| **documentType** | Art des Textes, den eine RUML-Datei abbildet, etwa `"law"` oder `"regulation"`.                                                                                                             | [3.3.6](../03-data-model/3-3-metadata-object.md#336-documenttype-werte) |

### Operatoren

| Begriff                              | Definition                                                                                 | Definiert in                                                          |
| ------------------------------------ | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **AND**                              | Konjunktion — alle Children MÜSSEN `true` sein.                                            | [3.6.1](../03-data-model/3-6-operators.md#361-and-und-not_and)        |
| **OR**                               | Disjunktion — mindestens ein Child MUSS `true` sein.                                       | [3.6.2](../03-data-model/3-6-operators.md#362-or-und-not_or)          |
| **XOR**                              | Disjunktion über Children, die so konstruiert sind, dass höchstens eines `true` sein kann. | [3.6.3](../03-data-model/3-6-operators.md#363-xor-und-not_xor)        |
| **NOT_AND**, **NOT_OR**, **NOT_XOR** | Negationen der jeweiligen Operatoren.                                                      |                                                                       |
| **DELEGATED**                        | Verknüpfung durch eine im Node hinterlegte Capability.                                     | [3.6.4](../03-data-model/3-6-operators.md#364-der-operator-delegated) |
| **undefined**                        | Platzhalter-Operator; nur in `draft` zulässig.                                             | [3.6.5](../03-data-model/3-6-operators.md#365-der-undefined-operator) |

### Capabilities

| Begriff                  | Definition                                                                                                                          | Definiert in                                               |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Capability**           | Deklarierte Erweiterung, die Funktionalität hinzufügt, ohne die Kernstruktur zu verändern.                                          | [4.1](../04-capabilities/4-1-concept.md)                   |
| **Capability-Rolle**     | Funktion, die eine Capability in einer Rulemap erfüllt, etwa `decision` oder `data`.                                                | [4.1](../04-capabilities/4-1-concept.md#capability-rollen) |
| **Capability-Namespace** | Id-Prefix, das die Zuständigkeit festlegt: `ruml:` (reserviert), `ruml:draft/` (experimentell) oder Reverse-Domain (Drittanbieter). | [4.4](../04-capabilities/4-4-namespaces.md#präfix-tabelle) |

### Status

| Begriff             | Definition                                                                                     | Definiert in                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Document-Status** | Gültigkeitszustand einer RUML-Datei, etwa `draft` oder `inForce`.                              | [3.3.3](../03-data-model/3-3-metadata-object.md#333-status-werte) |
| **Node-Status**     | Auswertungszustand eines Nodes, etwa `true` oder `false`; nicht in der RUML-Datei gespeichert. | [5.0](../05-result-format/5-0-status-types.md)                    |

### Dateiformate und Integrität

| Begriff               | Definition                                                               | Definiert in                                                                |
| --------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| **RUML-Datei**        | Primäre Inhaltsdatei (`.ruml`).                                          | [2.2](../02-file-format-basics/2-2-file-structure.md#format-identifikation) |
| **RUML-EXT**          | Sidecar-Datei (`.ruml-ext`), die Capability-Daten separat transportiert. | [4.5](../04-capabilities/4-5-ruml-ext.md)                                   |
| **RUML-Result-Datei** | Datei (`.ruml-result`) mit Auswertungsergebnissen.                       | [5](../05-result-format/index.md)                                           |
| **Container**         | ZIP-Paket für Integritätssicherung, Signaturen und Verschlüsselung.      | [7](../07-container/index.md)                                               |
| **Hash**              | Integritätsprüfwert im Format `{algorithm}:{value}`.                     | [7.3](../07-container/7-3-hashing.md)                                       |
