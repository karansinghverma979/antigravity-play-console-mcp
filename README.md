# 🚀 Antigravity Play Console MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Standard](https://img.shields.io/badge/MCP-2024--11--05-brightgreen.svg)](https://modelcontextprotocol.io/)

A production-grade **Model Context Protocol (MCP)** server providing autonomous AI agents and developer workflows with complete, programmatic control over the **Google Play Developer API v3**.

Deploy Android App Bundles (`.aab`), manage release tracks (`internal`, `closed`, `production`), update localized store presence, handle testing groups, and reply to user reviews effortlessly.

---

## 🏛️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│  AI Agent / MCP Client (Antigravity, Claude, Cursor)   │
└───────────────────────────┬────────────────────────────┘
                            │ Standard JSON-RPC (stdio)
                            ▼
┌────────────────────────────────────────────────────────┐
│         antigravity-play-console-mcp Engine            │
│  • Tool Dispatcher     • Track Lifecycle Manager       │
│  • Bundle Validator    • Localized Metadata Engine     │
└───────────────────────────┬────────────────────────────┘
                            │ Google Play Developer API v3
                            ▼
┌────────────────────────────────────────────────────────┐
│             Google Play Console Ecosystem              │
│  • Internal / Closed / Open / Production Tracks        │
│  • Store Listings (Title, Descriptions, Videos)        │
│  • Android Vitals & Reviews Feedback                   │
└────────────────────────────────────────────────────────┘
```

---

## ⚡ Available MCP Tools

| Tool Name | Scope & Purpose |
| :--- | :--- |
| `play_check_status` | Verifies active API connection, service account credentials, and endpoint health. |
| `play_get_app_details` | Retrieves app metadata, default locale, and status for a given `package_name`. |
| `play_get_listings` | Fetches all localized store listings (titles, short/full descriptions, graphics). |
| `play_update_listing` | Updates or creates localized store presence (Title, Short/Full Description, Promo Video). |
| `play_upload_bundle` | Uploads an Android App Bundle (`.aab`) to Google Play and returns the generated `versionCode`. |
| `play_list_tracks` | Lists all active release tracks (`internal`, `alpha`, `beta`, `production`, `closed:*`). |
| `play_create_release` | Deploys a `versionCode` to a track with release notes and staged rollout control (`user_fraction`). |
| `play_list_reviews` | Queries user ratings, feedback, and reviews with pagination. |
| `play_reply_review` | Publishes an official developer response to a user review on Google Play. |

---

## 🛠️ Prerequisites & Setup

### 1. Enable Google Play Developer API in Google Cloud
1. In the [Google Cloud Console](https://console.cloud.google.com/), select or create a project.
2. Enable the **Google Play Android Developer API** (`androidpublisher.googleapis.com`):
   ```bash
   gcloud services enable androidpublisher.googleapis.com --project <YOUR_PROJECT_ID>
   ```

### 2. Create Service Account & Download Key
1. Create a service account:
   ```bash
   gcloud iam service-accounts create play-automation --display-name="Play Store Automation"
   ```
2. Generate the private JSON key:
   ```bash
   gcloud iam service-accounts keys create ~/keys/google-play-service-account.json \
       --iam-account="play-automation@<YOUR_PROJECT_ID>.iam.gserviceaccount.com"
   ```

### 3. Grant Permissions in Google Play Console
1. Navigate to **Google Play Console $\rightarrow$ Users and Permissions**.
2. Click **Invite new users** and enter your Service Account email.
3. Under **Account permissions**, grant **Admin** (or *Release to production*, *Release to testing tracks*, *Manage store presence*).
4. Send invitation / Save changes.

---

## 📦 Installation & MCP Client Configuration

### Dependencies
```bash
pip install -r requirements.txt
```

### Antigravity / Claude Desktop / Cursor (`mcp_config.json`)

Add the following to your MCP client configuration file:

```json
{
  "mcpServers": {
    "play-console": {
      "command": "python",
      "args": [
        "-u",
        "C:/Users/karan/.gemini/antigravity-play-console-mcp/src/server.py"
      ],
      "env": {
        "PLAY_CONSOLE_KEY_PATH": "C:/Users/karan/.gemini/keys/google-play-service-account.json"
      }
    }
  }
}
```

### Credential Resolution Order
The server automatically searches for credentials in the following order:
1. `PLAY_CONSOLE_KEY_PATH` environment variable.
2. `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
3. `~/.gemini/keys/google-play-service-account.json`
4. `./service_account.json` (Local repo directory).

---

## 💻 Tool Usage Examples

### 1. Upload App Bundle (`.aab`)
```json
{
  "name": "play_upload_bundle",
  "arguments": {
    "package_name": "com.example.myapp",
    "aab_path": "build/app/outputs/bundle/release/app-release.aab"
  }
}
```

### 2. Promote to Internal Testing Track
```json
{
  "name": "play_create_release",
  "arguments": {
    "package_name": "com.example.myapp",
    "track": "internal",
    "version_code": 104,
    "release_name": "1.0.4-beta",
    "release_notes": {
      "en-US": "Added dark mode and offline sync engine.",
      "hi-IN": "डार्क मोड और ऑफलाइन सिंक जोड़ा गया।"
    },
    "status": "completed"
  }
}
```

### 3. Update Store Listing
```json
{
  "name": "play_update_listing",
  "arguments": {
    "package_name": "com.example.myapp",
    "language": "en-US",
    "title": "My Super App",
    "short_description": "Fast, privacy-friendly notes & tasks.",
    "full_description": "Full detailed store description with markdown features..."
  }
}
```

---

## 🛡️ Security & Zero-Leak Invariant
* **Never commit service account JSON keys (`.json`) or keystore files (`.jks`, `.keystore`)** to version control.
* This repository includes a hardened `.gitignore` ensuring that credential patterns are ignored by default.

---

## 📄 License
Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 👤 Author
**Karan Singh Verma**
* GitHub: [@karansinghverma979](https://github.com/karansinghverma979)
