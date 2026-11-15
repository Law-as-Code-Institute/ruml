<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 07. RUML-Container

Dieses Kapitel definiert das **RUML-Container-Format** — das Verpackungsformat für RUML-Dateien, das
Integritätssicherung, digitale Signaturen und Verschlüsselung ermöglicht.

| Abschnitt                                         | Inhalt                                        |
| ------------------------------------------------- | --------------------------------------------- |
| [7.1 Überblick](7-1-overview.md)                  | Dual-Mode-Konzept, Anwendungsfälle            |
| [7.2 Container-Struktur](7-2-structure.md)        | ZIP-Layout, Dateitypen, Manifest              |
| [7.3 Hash-Schicht](7-3-hashing.md)                | Integritätsprüfung, kanonische Repräsentation |
| [7.4 Signatur-Schicht](7-4-signatures.md)         | Detached Signatures, Format-Registry          |
| [7.5 Verschlüsselungs-Schicht](7-5-encryption.md) | Dateiverschlüsselung, Format-Registry         |
| [7.6 Verarbeitungsreihenfolge](7-6-processing.md) | Hash → Signatur → Verschlüsselung             |
| [7.7 Versionierung](7-7-versioning.md)            | Mehrere Versionen im Container                |
