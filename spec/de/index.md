<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# RUML – Rulemapping Logic Format

RUML ist ein offenes, JSON-basiertes Dateiformat für die maschinenausführbare Repräsentation
rechtlicher Entscheidungslogik. Diese Spezifikation beschreibt das Format: seinen Aufbau, seine
Erweiterungsmechanik und die Anforderungen, die eine Implementierung erfüllen muss, um konform zu
sein.

RUML steht für Rulemapping Logic. Das Format zeichnet keinen Normtext aus, sondern hält die
Entscheidungslogik als eigenes Artefakt und verweist auf den Wortlaut zurück.

## Status dieses Dokuments

**Version 1.0.0 / 15. November 2026**

Herausgegeben von der Law as Code Institut GmbH. Rechteinhaberin der Spezifikation ist die
Rulemapping Group GmbH.

## Lizenz

Die Spezifikation steht unter
[Creative Commons Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.de).
Sie darf kopiert, weitergegeben, übersetzt und bearbeitet werden, auch zu wirtschaftlichen Zwecken,
sofern die Rechteinhaberin genannt wird und Bearbeitungen unter derselben Lizenz weitergegeben
werden.

Namensnennung:

> RUML – Rulemapping Logic Format, Version 1.0.0, © Rulemapping Group GmbH,
> herausgegeben von der Law as Code Institut GmbH, lizenziert unter CC BY-SA 4.0.

Die Lizenz liegt auf dem Dokument, nicht auf dem Format. Wer eine Laufzeitumgebung baut,
RUML-Dateien erzeugt, verarbeitet oder austauscht, braucht dafür keine Lizenz und keine Zustimmung.
Die Pflicht zur Weitergabe unter gleichen Bedingungen gilt für Bearbeitungen dieses Textes. Sie
erstreckt sich weder auf Software, die das Format umsetzt, noch auf Rulemaps, die im Format
entstehen; Rulemaps bleiben bei ihren Urhebern.

Die JSON-Schemas, die Konformitätstests und die Beispiele stehen unter der
[Apache-Lizenz 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Maßgebliche Fassung

Die englische Fassung ist maßgeblich. Die deutsche Fassung ist eine Übersetzung. Weichen beide
voneinander ab, gilt der englische Wortlaut.

## Zitierweise

> Rulemapping Group GmbH: RUML – Rulemapping Logic Format. Version 1.0.0. Law as Code
> Institut GmbH, 15. November 2026.
>
> https://ruml.org/1.0.0/

Ein Verweis auf eine einzelne Regelung nennt das Kapitel: _RUML 1.0.0, Kapitel 4.6
(Parser-Pflichten)._

## Fassungen und Adressen

|                          |                                                      |
| ------------------------ | ---------------------------------------------------- |
| Diese Fassung            | `https://ruml.org/1.0.0/` |
| Jeweils aktuelle Fassung | `https://ruml.org/`                                  |
| Änderungshistorie        | [Änderungshistorie](change-history.md)               |

Eine veröffentlichte Fassung bleibt unter ihrer Versionsadresse unverändert erreichbar. Wer die
Spezifikation zitiert oder in einem Dokument referenziert, verwendet die Versionsadresse, nicht die
aktuelle.

Die Versionierung des Formats selbst – das Feld `$specVersion` in der Datei – ist davon zu
unterscheiden und in [Kapitel 2.3](02-file-format-basics/2-3-versioning.md) geregelt.

## Marke

RUML ist ein Kennzeichen der Rulemapping Group GmbH; die Eintragung als Unionsmarke ist beantragt.
Das Format darf frei benannt werden: Aussagen wie „unterstützt RUML“ oder „RUML-kompatibel“ sind
zulässig, wenn sie zutreffen. Dateien, Software und Dienste, die dieser Spezifikation nicht
entsprechen, dürfen nicht als RUML bezeichnet werden. Eine geänderte oder abgeleitete Fassung dieser
Spezifikation darf nicht RUML heißen.

## Aufbau der Spezifikation

| Kapitel                                         | Gegenstand                                                            |
| ----------------------------------------------- | --------------------------------------------------------------------- |
| [1 Einführung](01-introduction/index.md)        | Anwendungsbereich, Notation, Terminologie, Konformität                |
| [2 Dateiformat](02-file-format-basics/index.md) | JSON-Aufbau, Versionierung, Integrität, Identifier                    |
| [3 Datenmodell](03-data-model/index.md)         | Metadaten, Rulemap, Knoten, Operatoren                                |
| [4 Capabilities](04-capabilities/index.md)      | Erweiterungsmechanik, `ruml:`-Capabilities, Drittanbieter-Namespaces  |
| [5 Ergebnisformat](05-result-format/index.md)   | RUML-Result                                                           |
| [6 Modulare Knoten](06-modular-nodes/index.md)  | Wiederverwendung, Rekursion, Verschachtelung                          |
| [7 Container](07-container/index.md)            | Bündelung, Hash, Signatur, Verschlüsselung                            |
| [8 Validierung](08-validation/index.md)         | Regelkatalog für konforme Parser                                      |
| [Anhang](appendix/index.md)                     | A. Spec Test Suite: Konformitätssuite und Runner-Vertrag (informativ) |

**Wo anfangen.** Wer das Format zum ersten Mal liest, beginnt bei
[Kapitel 1.1](01-introduction/1-1-introduction.md) (Anwendungsbereich) und
[1.4](01-introduction/1-4-conformance.md) (Konformität). Wer eine Laufzeitumgebung baut, liest
Kapitel [2](02-file-format-basics/index.md), [3](03-data-model/index.md),
[4](04-capabilities/index.md), [5](05-result-format/index.md), [6](06-modular-nodes/index.md),
[7](07-container/index.md) und [8](08-validation/index.md) zusammenhängend und prüft die
Implementierung gegen die Konformitätssuite in [Anhang A](https://ruml.org/de/appendix/spec-tests). Wer wissen will,
wie sich RUML zu Akoma Ntoso, DMN oder LegalRuleML verhält, findet das in
[Kapitel 1.5](01-introduction/1-5-relationship-to-other-standards.md).

## Rückmeldungen

Fehler, Unklarheiten und Widersprüche in dieser Spezifikation können über
[law-as-code.org/contact](https://law-as-code.org/contact) oder als Issue auf
[GitHub](https://github.com/Law-as-Code-Institute/ruml/issues) gemeldet werden. Änderungsvorschläge
zum Spezifikationstext sind auf demselben Weg willkommen; Pull Requests werden derzeit nicht
angenommen.
