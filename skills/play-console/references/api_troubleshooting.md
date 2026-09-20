# 🔧 Google Play Developer API Troubleshooting

## 1. Common Error Codes & Resolutions

### `401 Unauthorized` / `Invalid Credentials`
- **Cause**: The service account key is invalid, expired, or not granted API access.
- **Resolution**:
  1. Verify the service account is added to Google Play Console under **Users and permissions**.
  2. Grant the service account permissions: **Release apps to testing tracks**, **Manage store presence**, and **Manage production releases**.
  3. Verify the key exists in `%USERPROFILE%\.gemini\keys\google-play-service-account.json`.

### `400 Invalid Version Code`
- **Cause**: The uploaded `.aab` has a `versionCode` less than or equal to an existing release.
- **Resolution**: Increment `flutter build appbundle --build-number=<N>` or bump `versionCode` in `build.gradle.kts`.

### `403 Access Not Configured`
- **Cause**: The Google Play Developer API is not enabled on the associated Google Cloud project.
- **Resolution**: Open Google Cloud Console -> APIs & Services -> Enable **Google Play Android Developer API**.
