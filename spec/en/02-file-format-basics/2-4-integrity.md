<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.4 Integrity Assurance

### Overview

Integrity assurance is provided via the **RUML Container Format** (see
[Chapter 7](../07-container/index.md)). Hash computation, signatures, and encryption are container
layers and are NOT part of the JSON content file itself.

A standalone `.ruml` JSON file without a container has **no embedded integrity protection**. This is
intentional: in development and draft mode (e.g., status `"draft"`), the file should be freely
editable without requiring a hash recalculation on every change.

### Canonical JSON Representation

For consistent hash computation at container level, the RUML file MUST be canonicalized according to
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785). Details on the canonicalization procedure and
hash computation see [Chapter 7](../07-container/index.md).

### Authenticity and Legal Binding

Legal immutability and authenticity are ensured through **signatures** at container level — not
through hashes alone. A hash secures technical integrity (detection of transmission errors or
accidental changes), but provides no protection against intentional manipulation.

See [Chapter 7](../07-container/index.md) for the complete specification of hashing, signatures, and
encryption.
