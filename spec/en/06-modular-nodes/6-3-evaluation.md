<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.3 Evaluation and Copy Behavior

---

**Evaluation with multiple referencing:**

Since a modular node exists only once in the `nodes` object, all structural properties (`label`,
`operator`, `children`, `capabilities`, etc.) are automatically identical at every reference
location.

The evaluation result **MAY**, however, differ per reference location. During evaluation, the tool
**MUST** consider the context — i.e., through which path the modular node was reached. The paths are
computed at runtime from the tree structure (`children` arrays).

---

**Example:** A modular node "Bonitätsprüfung" (`lexId: 8`) is referenced at two locations:

| Path    | Context                                                     | Result  |
| ------- | ----------------------------------------------------------- | ------- |
| `1.2`   | Direct call from root — preceding conditions fulfilled      | `true`  |
| `1.3.1` | Call via "Alternative Prüfungen" — different data situation | `false` |

---

**Storage of results:**

Since a modular node can have different results per path, the evaluation results in the `results`
object of the RUML result file are indexed by **path** (see
[Chapter 5.1.2](../05-result-format/5-1-result-model.md)):

```jsonc
"results": {
  "1.2": {
    "lexId": "8",
    "status": "true",
    "reason": "AND: alle Kinder true"
  },
  "1.3.1": {
    "lexId": "8",
    "status": "false",
    "reason": "AND: Schufa-Score nicht erreicht"
  }
}
```

The `lexId` is stored as a mandatory field in each result entry to enable mapping back to the node
object.

---
