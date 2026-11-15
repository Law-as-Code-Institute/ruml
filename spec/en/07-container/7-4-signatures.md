<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.4 Signature Layer

### Purpose

Digital signatures provide **authenticity** and **non-repudiation** — they answer the questions:
_"Who published this file?"_ and _"Has it been modified since signing?"_

Unlike a hash (pure integrity verification), a signature requires the private key of the signer. A
signature cannot be easily recreated — it binds a specific identity to specific content.

### Detached Signatures

Signatures in a RUML container are **always detached** — the signature file contains only the
signature, not the signed content. The signed content resides as a separate file in the container.

```
rulemap.json                          ← signed content
signatures/rulemap.json.sig           ← signature (without content)
```

For verification, both files are needed: the parser loads the content and the signature, and
verifies the signature against the content.

**For JSON files**, the **canonicalized form** (RFC 8785) is signed — not the stored file. This
ensures that formatting differences (whitespace, key ordering) do not invalidate the signature.

**For non-JSON files** (assets), the **raw bytes** are signed.

### Signature Formats

This specification does not prescribe a signature format. The manifest names the format of each
signature in the `format` field; which formats a parser supports is up to the implementation.

| Identifier     | Format                           | Standard             |
| -------------- | -------------------------------- | -------------------- |
| `jws-detached` | JWS with detached content        | RFC 7515, Appendix F |
| `cms-detached` | CMS `SignedData` without content | RFC 5652             |

These two identifiers are reserved for the formats named. Any other format MUST use an identifier in
reverse-domain form, for example `com.example/ed25519-raw`.

A parser that does not support the format of a signature MUST report that the signature was not
verified and MUST NOT treat the file as signed.

How keys and certificates are obtained and trusted is outside this specification.

### Manifest Reference

The signature is declared in the manifest as follows:

```jsonc
"signature": {
  "path": "signatures/rulemap.json.sig",
  "format": "jws-detached"
}
```

| Field    | Type   | Description                                                  |
| -------- | ------ | ------------------------------------------------------------ |
| `path`   | String | MUST specify the path to the signature file in the container |
| `format` | String | MUST specify the signature format                            |

### Multiple Signatures

A file MAY be signed by multiple parties. In this case, `signature` MUST be an array:

```jsonc
"signature": [
  {
    "path": "signatures/rulemap.json.ministry.sig",
    "format": "cms-detached",
    "signer": "Federal Ministry of Justice"
  },
  {
    "path": "signatures/rulemap.json.auditor.sig",
    "format": "jws-detached",
    "signer": "Auditor"
  }
]
```

The optional `signer` field MAY contain a human-readable identifier of the signer. The cryptographic
identity is determined by the certificate in the signature file itself — `signer` serves only for
readability.

### Manifest Signature as Trust Anchor

The manifest MAY be signed like any other file in the container. The signature is declared in the
`files` entry of the manifest itself:

```jsonc
"manifest.json": {
  "hash": {
    "algorithm": "sha3-256",
    "value": "5d8e2b1f4a7c0e3b6d9f2a5c8e1b4d7f0a3c6e9b2d5f8a1c4e7b0d3f6a9c2e5b"
  },
  "signature": {
    "path": "signatures/manifest.json.sig",
    "format": "jws-detached"
  }
}
```

When the manifest is signed, a **chain of trust over the entire container** is established:

1. The manifest signature protects the manifest content
2. The manifest contains the hashes of all content files
3. The hashes protect the file contents

A signed manifest means: _"The signer confirms the integrity of all files referenced in the manifest
at the time of signing."_

**Computation:** When computing the hash and signing the manifest, the own entry (`"manifest.json"`)
MUST be excluded from the `files` object. Hash and signature are computed over the canonicalized
(RFC 8785) version of the manifest in which this key is not present. The entry is inserted into the
manifest only after signing.

**Recommendation:** For legally binding containers, the manifest SHOULD be signed. For maximum
security, a container SHOULD both sign individual files (per-file responsibility) and the manifest
(container integrity as a whole).

### Integration with Qualified Signatures

For legally binding signatures (e.g., under eIDAS, ZertES, ESIGN Act), the following workflow is
typically used:

1. Canonicalize the file in the container (RFC 8785 for JSON)
2. Compute the hash of the canonicalized file
3. Send the hash to a qualified trust service provider (QTSP)
4. The QTSP signs the hash with the signer's private key (on an HSM)
5. The signature is returned and stored as a `.sig` file in the container
6. The manifest is updated with `"format": "cms-detached"`

This workflow requires no changes to the RUML format — the qualified signature is simply a CMS file
in the `signatures/` directory.

### Validation

During signature verification, a parser MUST:

1. Load the signature file and the source file from the container
2. Canonicalize the source file (for JSON) or use the raw bytes (for assets)
3. Verify the signature against the canonicalized content
4. If the signature is invalid, an error MUST be raised

A parser SHOULD additionally:

- Validate the certificate chain (for CMS signatures)
- Verify the timestamp (if present)
- Check the revocation status of the certificate (OCSP/CRL)

The depth of signature validation depends on the application context. A development tool MAY limit
itself to cryptographic validity. A system for legally binding documents MUST verify the complete
certificate chain and revocation status.
