<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.4 Integritätssicherung

### Überblick

Integritätssicherung wird über das **RUML-Container-Format** bereitgestellt (siehe
[Kapitel 7](../07-container/index.md)). Hash-Berechnung, Signaturen und Verschlüsselung sind
Container-Schichten und KEIN Bestandteil der JSON-Inhaltsdatei selbst.

Eine einzelne `.ruml`-JSON-Datei ohne Container besitzt **keinen eingebetteten Integritätsschutz**.
Dies ist beabsichtigt: Im Entwicklungs- und Entwurfsmodus (z.B. Status `"draft"`) soll die Datei
frei bearbeitbar sein, ohne dass bei jeder Änderung ein Hash neu berechnet werden muss.

### Kanonische JSON-Repräsentation

Für konsistente Hash-Berechnung auf Container-Ebene MUSS die RUML-Datei nach
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) kanonisiert werden. Details zum
Kanonisierungsverfahren und zur Hash-Berechnung siehe [Kapitel 7](../07-container/index.md).

### Authentizität und rechtliche Verbindlichkeit

Rechtliche Unveränderlichkeit und Authentizität werden durch **Signaturen** auf Container-Ebene
gewährleistet — nicht durch Hashes allein. Ein Hash sichert die technische Integrität (Erkennung von
Übertragungsfehlern oder versehentlichen Änderungen), bietet aber keinen Schutz gegen absichtliche
Manipulation.

Siehe [Kapitel 7](../07-container/index.md) für die vollständige Spezifikation von Hashing,
Signaturen und Verschlüsselung.
