# Security Policy

## Supported Versions
Only the latest release receives active security patches.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Invariants
`play-console-plugin` enforces strict operational security boundaries:
1. **Sovereign External Credential Quarantine**: Google Play service account keys (`*.json`) must strictly reside outside the git working tree in `%USERPROFILE%\.gemini\keys\google-play-service-account.json` or via `PLAY_CONSOLE_KEY_PATH`.
2. **Path Portability**: Absolute machine paths (e.g. `C:\Users\<user>`) are forbidden in git-tracked code and documentation.
3. **Production Safety Barrier**: Direct unconfirmed releases to Google Play production tracks are blocked by operational policy.

## Reporting a Vulnerability
**Please do not report security vulnerabilities through public GitHub issues.**

To report a vulnerability or credential handling defect:
1. Use GitHub's private vulnerability reporting feature on this repository.
2. Provide a clear description of the vulnerability, reproduction steps, and potential impact.

Reports will be acknowledged within 48 hours and resolved promptly.
