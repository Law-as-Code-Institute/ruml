<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.5 Encryption Layer

### Purpose

Encryption provides **confidentiality** — it answers the question: _"Who is allowed to read this
file?"_

Encryption in a RUML container operates at the **file level**: a complete file is encrypted and
stored as an `.enc` file in the `encrypted/` directory. The plaintext file is removed from the
container.

For field-level encryption within a file (e.g., individual capability payloads), the respective
capability itself is responsible — not the container.

### Encrypted Files

When a file is encrypted, it no longer exists as plaintext in the container. Instead, the encrypted
version resides in the `encrypted/` directory:

```
Container WITHOUT encryption:
├── results/2026-03-15.json           ← plaintext

Container WITH encryption:
├── encrypted/results/2026-03-15.json.enc   ← encrypted
```

The plaintext file (`results/2026-03-15.json`) MUST NOT exist simultaneously with its encrypted
version in the container.

### Encryption Formats

This specification does not prescribe an encryption format. The manifest names the format in the
`format` field; which formats a parser supports is up to the implementation.

| Identifier      | Format              | Standard |
| --------------- | ------------------- | -------- |
| `jwe`           | JSON Web Encryption | RFC 7516 |
| `cms-enveloped` | CMS `EnvelopedData` | RFC 5652 |

These two identifiers are reserved for the formats named. Any other format MUST use an identifier in
reverse-domain form.

How keys are obtained and distributed is outside this specification.

### Manifest Reference

Encryption is declared in the manifest as follows:

```jsonc
"encryption": {
  "path": "encrypted/results/2026-03-15.json.enc",
  "format": "jwe",
  "algorithm": "RSA-OAEP-256"
}
```

| Field       | Type   | Description                                                  |
| ----------- | ------ | ------------------------------------------------------------ |
| `path`      | String | MUST specify the path to the encrypted file in the container |
| `format`    | String | MUST specify the encryption format                           |
| `algorithm` | String | MAY name the algorithm used, as the format defines it        |

### Order: Signature Before Encryption

When a file is both signed and encrypted, the signature MUST be created over the **plaintext** — not
over the encrypted version. The processing order is:

**Creation:** Hash → Signature → Encryption (on plaintext) **Verification:** Decryption → Signature
verification → Hash verification (on plaintext)

This means: hash and signature always refer to the plaintext. The signature file resides in the
`signatures/` directory and refers to the logical file (e.g., `results/2026-03-15.json`), not to the
encrypted file.

### Validation

When accessing an encrypted file, a parser MUST:

1. Check whether a matching decryption key is available
2. Decrypt the `.enc` file
3. Provide the decrypted file for further processing (signature verification, hash verification,
   parsing)

A parser that does not support the format, or does not have a matching key, MUST report the file as
not readable. The remaining files in the container MUST remain processable — a single
non-decryptable file MUST NOT render the entire container unusable.
