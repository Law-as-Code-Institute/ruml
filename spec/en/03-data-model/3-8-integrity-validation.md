<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.8 Integrity Validation

Hashing, signatures, and integrity assurance are container-level responsibilities and are specified
in [Chapter 7](../07-container/index.md). The RUML JSON file contains no hash or signature of
itself; for the hashes of other content it may contain, see
[3.2.4](3-2-data-types-and-formats.md#324-hash-format).

**Structural validation on load:**

Implementations MUST check the **structural validity** when loading a RUML file:

1. **JSON validity:** The file MUST be valid JSON ([`FMT-02`](../08-validation/index.md#rule-fmt-02))
2. **Required fields:** All required fields defined in [Chapter 3.3](3-3-metadata-object.md) MUST be
   present ([`META-01`](../08-validation/index.md#rule-meta-01))
3. **Type conformity:** Field values MUST conform to the data types defined in
   [Chapter 3.2](3-2-data-types-and-formats.md) ([`FMT-13`](../08-validation/index.md#rule-fmt-13))
4. **Node references:** All `children` references MUST point to existing LexIDs in the `nodes`
   object ([`NODE-10`](../08-validation/index.md#rule-node-10))
5. **UUID uniqueness:** The `id` of every node and `metadata.id` MUST be unique within the file
   ([`NODE-08`](../08-validation/index.md#rule-node-08)). A UUID that refers to another node or file, such as `replacedBy` or a tree
   reference, repeats that id

**Validation on changes:**

On every change to a RUML file, the following MUST be done:

1. The `modified` field must be updated
2. Structural validity must be re-verified

Hash verification and signature checking are performed at container level. Details see
[Chapter 7](../07-container/index.md).
