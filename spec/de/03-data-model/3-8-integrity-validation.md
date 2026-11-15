<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.8 Integritätsvalidierung

Hashing, Signaturen und Integritätssicherung sind Container-Ebene-Aufgaben und werden in
[Kapitel 7](../07-container/index.md) spezifiziert. Die RUML-JSON-Datei enthält keinen Hash und
keine Signatur ihrer selbst; zu den Hashes anderer Inhalte, die sie enthalten kann, siehe
[3.2.4](3-2-data-types-and-formats.md#324-hash-format).

**Strukturelle Validierung beim Laden:**

Implementierungen MÜSSEN beim Laden einer RUML-Datei die **strukturelle Validität** prüfen:

1. **JSON-Validität:** Die Datei MUSS valides JSON sein ([`FMT-02`](../08-validation/index.md#rule-fmt-02))
2. **Pflichtfelder:** Alle in [Kapitel 3.3](3-3-metadata-object.md) definierten Pflichtfelder MÜSSEN
   vorhanden sein ([`META-01`](../08-validation/index.md#rule-meta-01))
3. **Typkonformität:** Feldwerte MÜSSEN den in [Kapitel 3.2](3-2-data-types-and-formats.md)
   definierten Datentypen entsprechen ([`FMT-13`](../08-validation/index.md#rule-fmt-13))
4. **Knotenreferenzen:** Alle `children`-Referenzen MÜSSEN auf existierende LexIDs im `nodes`-Objekt
   verweisen ([`NODE-10`](../08-validation/index.md#rule-node-10))
5. **UUID-Eindeutigkeit:** Die `id` jedes Knotens und `metadata.id` MÜSSEN innerhalb der Datei
   eindeutig sein ([`NODE-08`](../08-validation/index.md#rule-node-08)). Eine UUID, die auf einen anderen Knoten oder eine andere Datei
   verweist, etwa `replacedBy` oder eine Tree-Referenz, wiederholt deren id

**Validierung bei Änderungen:**

Bei jeder Änderung einer RUML-Datei MUSS:

1. Das `modified`-Feld aktualisiert werden
2. Die strukturelle Validität erneut geprüft werden

Hash-Verifikation und Signaturprüfung erfolgen auf Container-Ebene. Details siehe
[Kapitel 7](../07-container/index.md).
