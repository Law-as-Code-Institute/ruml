<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.3 Hash Layer

### Purpose

Hashing serves exclusively for **technical integrity verification** — it answers the question: _"Is
this file unmodified?"_

Hashing provides **no authenticity** and **no immutability guarantee**. Any person with write access
can modify the content and compute a new hash. For authenticity and non-repudiation, a digital
signature is required (see [7.4](7-4-signatures.md)).

### Hash in the Manifest

Each file in the container MAY have a hash. The hash is recorded in the manifest entry of the file;
there are no separate hash files:

```jsonc
"hash": {
  "algorithm": "sha3-256",
  "value": "4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
}
```

| Field       | Type   | Description                                           |
| ----------- | ------ | ----------------------------------------------------- |
| `algorithm` | String | MUST specify the algorithm used                       |
| `value`     | String | MUST contain the hash as lowercase hexadecimal digits |

Because the manifest holds the hash values, a signature over the manifest (see
[7.4](7-4-signatures.md#manifest-signature-as-trust-anchor)) covers the content of every file that
has a hash.

### Algorithms

| Requirement | Algorithm | Identifier    | Output Length     |
| ----------- | --------- | ------------- | ----------------- |
| **MUST**    | SHA3-256  | `sha3-256`    | 64 hex characters |
| **MAY**     | Any other | Freely chosen | Variable          |

A parser MUST support SHA3-256. A container SHOULD use SHA3-256, so that every parser can verify it.

A parser that encounters an algorithm it does not support MUST issue a warning and skip the
integrity check for that file.

### Canonical Representation for JSON Files

For consistent hash computation, JSON files in the container MUST be canonicalized according to
**RFC 8785 (JCS — JSON Canonicalization Scheme)**:

1. Object keys MUST be sorted lexicographically (by UTF-16 code units)
2. Whitespace outside of string values MUST be removed
3. Numbers MUST be specified in their shortest IEEE 754 representation

The hash is computed over the **canonicalized form**, not over the file as stored in the container.
The stored file MAY be formatted (pretty-printed) — this has no effect on the hash.

For non-JSON files (assets), the hash is computed over the **raw bytes**.

### Validation

During integrity verification, a parser MUST:

1. Load the source file and canonicalize it (for JSON) or read the raw bytes (for assets)
2. Compute the hash with the algorithm the manifest entry names
3. Compare it with the `value` in the manifest entry
4. In case of mismatch, an error MUST be raised — the file is considered compromised

A parser MUST perform the hash check when the manifest entry of a file has a `hash`. The hash check
is independent of the status of the RUML file (`draft`, `inForce`, etc.) — it is always performed.
