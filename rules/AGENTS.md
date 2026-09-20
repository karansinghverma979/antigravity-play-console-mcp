# 📱 Play Console Hub: Agent Rules & Publishing Invariants

Whenever invoking Google Play Console tools or managing Android application lifecycles, all Antigravity agents must strictly obey these directives:

---

### 1. 🔑 Sovereign External Credential Quarantine (Rule Zero)
* **MANDATORY**: Google Play service account keys (`*.json`) must **NEVER** be committed, created, or staged inside the git repository tree.
* Keys must reside strictly in the sovereign external quarantine vault:
  - `%USERPROFILE%\.gemini\credentials\play-console\service_account.json` (Windows)
  - `~/.gemini/credentials/play-console/service_account.json` (Linux / macOS)
  - Or specified via `PLAY_CONSOLE_KEY_PATH` environment variable (legacy `~/.gemini/keys/` supported as fallback).
* Never print or log private key strings, client emails, or key IDs into chat context or public logs.

---

### 2. 🛡️ The Production Release Guard & Staged Rollouts
* **Internal Test Track Mandate**: Before promoting an Android App Bundle (`.aab`) to `production`, always verify deployment on the `internal` or `closed` test track first.
* **Staged Rollout Invariant**: When creating a release on the `production` track, never set a 100% immediate rollout on initial release. Always start with a staged rollout fraction (`user_fraction` between `0.05` [5%] and `0.20` [20%]).
* **Explicit Confirmation Barrier**: Prior to committing any edit (`commit_edit`) on the `production` track, the agent must prompt the operator with:
  - App Package Name
  - Version Code
  - Target Track (`production`)
  - Rollout Percentage
  - Localized Release Notes Summary

---

### 3. 📝 Store Listing Metadata Constraints
Before executing `play_update_listing`, validate all fields against official Google Play policy boundaries:
- **Title**: Maximum **30 characters**.
- **Short Description**: Maximum **80 characters**.
- **Full Description**: Maximum **4,000 characters**.
- **Language Tags**: Must use standard BCP-47 codes (e.g. `en-US`, `hi-IN`, `es-419`, `de-DE`).

---

### 4. 🛣️ Zero Machine Path Portability
* Never commit local machine paths (e.g. `C:\Users\<user>\...`) in release notes, store copy, or documentation.
* Always use dynamic expansion or standard placeholders.
