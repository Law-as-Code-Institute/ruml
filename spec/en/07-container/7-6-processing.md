<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.6 Processing Order

### The Three Layers

The RUML container format defines three independent layers that are applied in a fixed order:

| Layer             | Question                           | Purpose             |
| ----------------- | ---------------------------------- | ------------------- |
| **1. Hash**       | "Is the file unmodified?"          | Technical integrity |
| **2. Signature**  | "Who published the file?"          | Authenticity        |
| **3. Encryption** | "Who is allowed to read the file?" | Confidentiality     |

**Order:** Plaintext → Hash → Signature → Encryption → Container (ZIP)

### Creation Order (Authoring)

When creating a container, the following order MUST be observed:

1. **Compute hash** — over the canonicalized plaintext file (RFC 8785 for JSON, raw bytes for
   assets). The value goes into the manifest in step 4.
2. **Create signature** — over the canonicalized plaintext file. Write to the signature file.
3. **Encrypt** — encrypt the plaintext file. Place the encrypted version in `encrypted/`. Remove the
   plaintext file from the container.
4. **Create manifest** — document all files, their hashes and their layers in the manifest.
5. **Hash/sign manifest** — optional, as the final step.

### Processing Order (Consuming)

When opening a container, the following order MUST be observed:

1. **Read manifest** — load and parse the manifest.
2. **Verify manifest** — if the manifest has a signature entry for itself, verify it first.
   Algorithm declarations in the manifest (`"algorithm"` fields) are only trustworthy after this
   verification: without a verified manifest signature, any algorithm declaration can be substituted
   by an attacker with write access to the container.
3. **Per file**, in this order:
   - **Decrypt** — if the file is encrypted, decrypt the `.enc` file.
   - **Verify signature** — if a signature is present, verify the signature against the (decrypted)
     plaintext file.
   - **Verify hash** — if a hash is present, compute the hash of the (decrypted) plaintext file and
     compare.

### Layers Are Optional and Independent

Each layer is optional. The following combinations are valid:

| Hash | Signature | Encryption | Use Case                                                   |
| ---- | --------- | ---------- | ---------------------------------------------------------- |
| ✗    | ✗         | ✗          | Simple container (bundling only)                           |
| ✓    | ✗         | ✗          | Integrity verification without authenticity                |
| ✓    | ✓         | ✗          | Signed distribution                                        |
| ✓    | ✓         | ✓          | Integrity-verified, signed, and encrypted                  |
| ✗    | ✓         | ✗          | Signed without explicit hash (signature implies integrity) |
| ✗    | ✗         | ✓          | Encrypted only (e.g., confidential results)                |

### Error Behavior

| Situation                                          | Behavior                                                                                    |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Hash mismatch                                      | MUST raise an error. File is considered compromised.                                        |
| Invalid signature                                  | MUST raise an error. File is considered not authentic.                                      |
| Unsupported hash algorithm                         | MUST issue a warning. Skip hash verification.                                               |
| Unsupported signature format                       | MUST report that the signature was not verified. The file MUST NOT be treated as signed.    |
| Unsupported encryption format or no decryption key | MUST report the file as not readable. Other files in the container MUST remain processable. |
