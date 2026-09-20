---
name: play-console
description: >-
  Google Play Console & Android Developer API automation skill.
  Use when uploading Android App Bundles (.aab), managing release tracks (internal, alpha, beta, production),
  configuring phased rollouts, updating store listing copy/metadata, checking service account health,
  or replying to user reviews.
---

# 📱 Play Console Hub: Android Publishing & Store Governor

The authoritative management skill and runbook for automating the Google Play Developer API v3 with sovereign credential isolation and production release safety barriers.

---

## 🏛️ Core Principles & Invariants

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PLAY CONSOLE GOVERNANCE                         │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 🔑 ZERO KEY LEAKS │ 🚀 STAGED ROLLOUT │ 📝 METADATA COMPLIANCE         │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ • External Keys   │ • Internal First  │ • Title ≤ 30 Chars             │
│ • No Keys in Git  │ • Phased Rollouts │ • Short Desc ≤ 80 Chars        │
│ • %LOCALAPPDATA%  │ • Operator Barrier│ • Full Desc ≤ 4000 Chars       │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

1. **🔑 Sovereign External Quarantine**:
   - Google Play service account keys must reside outside the repository tree in `%USERPROFILE%\.gemini\credentials\play-console\service_account.json` or `PLAY_CONSOLE_KEY_PATH` (legacy `~/.gemini/keys/` supported as fallback).
   - Never stage, commit, or print credentials.
2. **🛡️ Production Release Guard**:
   - Always upload and verify builds on the `internal` test track first.
   - Initial production releases must use staged rollouts (`user_fraction` between `0.05` and `0.20`).
3. **Deterministic Stdio MCP Server**:
   - All operations are backed by the bundled Python MCP server (`mcp/server.py`).

---

## 🔄 Core Operations

### 1. 🔍 Status & Authentication Health
Verifies connection status, service account email, and API endpoint readiness:
- **MCP Tool**: `play_check_status`
- **Expected Result**: `status: "online"`, valid `service_account` email.

### 2. 📦 Uploading Android App Bundles (.aab)
Uploads an Android App Bundle and extracts the assigned `version_code`:
- **MCP Tool**: `play_upload_bundle`
- **Arguments**:
  - `package_name`: e.g. `"com.company.app"`
  - `aab_path`: Absolute path to the `.aab` file on disk.
- **Safety Tip**: Confirm the version code is strictly greater than the currently active release.

### 3. 🚀 Track Management & Phased Rollouts
Creates or updates a release on a track (`internal`, `alpha`, `beta`, `production`):
- **MCP Tool**: `play_create_release`
- **Arguments**:
  - `package_name`: e.g. `"com.company.app"`
  - `track`: Target track (`"internal"`, `"alpha"`, `"beta"`, or `"production"`).
  - `version_code`: Integer version code returned from upload.
  - `status`: `"completed"`, `"draft"`, or `"inProgress"`.
  - `user_fraction`: Float between `0.0` and `1.0` (required for `inProgress` staged rollout, e.g. `0.1` for 10%).
  - `release_notes`: Object mapping language codes to notes text (e.g. `{"en-US": "Bug fixes and performance improvements."}`).

### 4. 📝 Store Listing Metadata & Localization
Updates localized store metadata adhering to Google Play character limits:
- **MCP Tool**: `play_update_listing`
- **Arguments**:
  - `package_name`: e.g. `"com.company.app"`
  - `language`: BCP-47 tag (e.g. `"en-US"`, `"hi-IN"`, `"es-419"`).
  - `title`: App Title (max 30 characters).
  - `short_description`: Promotional summary (max 80 characters).
  - `full_description`: App description (max 4,000 characters).
  - `video_url`: Optional YouTube video link.

### 5. ⭐ User Reviews & Customer Feedback Triage
Fetches ratings and posts developer replies:
- **MCP Tools**: `play_list_reviews`, `play_reply_review`
- **Arguments**:
  - `package_name`: e.g. `"com.company.app"`
  - `review_id`: Unique review identifier.
  - `reply_text`: Developer reply text (max 350 characters).
