# 📱 Play Console Hub: Core Invariants

1. **Sovereign Credential Quarantine**: Service account keys (`*.json`) live strictly in `%USERPROFILE%\.gemini\credentials\play-console\service_account.json`. Never commit keys to git or log key IDs.
2. **Production Release Guard & Staged Rollouts**:
   - Verify deployment on `internal` test track before `production`.
   - Never roll out 100% initially on production. Use staged fraction between `0.05` (5%) and `0.20` (20%).
   - Prompt operator for explicit confirmation before committing any edit to `production`.
3. **Store Listing Boundaries**:
   - Title: $\le$ 30 chars | Short Desc: $\le$ 80 chars | Full Desc: $\le$ 4,000 chars | Standard BCP-47 tags (`en-US`, `hi-IN`).
