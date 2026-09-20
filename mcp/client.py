"""Google Play Developer API v3 client engine."""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/androidpublisher"]


class PlayConsoleClient:
    """Encapsulates authenticated operations for Google Play Developer API v3."""

    def __init__(self, key_path: Optional[str] = None):
        self.key_path = self._resolve_key_path(key_path)
        self.credentials = service_account.Credentials.from_service_account_file(
            self.key_path, scopes=SCOPES
        )
        self.service = build("androidpublisher", "v3", credentials=self.credentials)

    @staticmethod
    def _resolve_key_path(custom_path: Optional[str] = None) -> str:
        """Resolve service account JSON key path strictly from sovereign external quarantine locations."""
        candidates = []
        if custom_path:
            candidates.append(Path(custom_path).expanduser())
        if os.getenv("PLAY_CONSOLE_KEY_PATH"):
            candidates.append(Path(os.getenv("PLAY_CONSOLE_KEY_PATH")).expanduser())
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            candidates.append(Path(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")).expanduser())
        
        # Sovereign External Quarantine locations (strictly outside git repository tree)
        candidates.append(Path.home() / ".gemini" / "keys" / "google-play-service-account.json")
        candidates.append(Path.home() / ".gemini" / "config" / "play_console" / "service_account.json")
        candidates.append(Path.home() / ".config" / "play_console" / "service_account.json")

        for p in candidates:
            if p.is_file():
                return str(p.resolve())

        raise FileNotFoundError(
            "Google Play Service Account JSON key not found! Please place key in external quarantine at "
            "~/.gemini/keys/google-play-service-account.json or set PLAY_CONSOLE_KEY_PATH."
        )

    # =========================================================================
    # App Edits Context Manager Lifecycle
    # =========================================================================
    def create_edit(self, package_name: str) -> str:
        """Create a new edit transaction for an app."""
        edit_request = self.service.edits().insert(packageName=package_name, body={})
        result = edit_request.execute()
        return result["id"]

    def commit_edit(self, package_name: str, edit_id: str, changes_not_sent_for_review: bool = False) -> Dict[str, Any]:
        """Commit an edit transaction."""
        return self.service.edits().commit(
            packageName=package_name,
            editId=edit_id,
            changesNotSentForReview=changes_not_sent_for_review
        ).execute()

    def validate_edit(self, package_name: str, edit_id: str) -> Dict[str, Any]:
        """Validate an edit transaction without committing."""
        return self.service.edits().validate(
            packageName=package_name,
            editId=edit_id
        ).execute()

    def delete_edit(self, package_name: str, edit_id: str) -> None:
        """Delete / discard an edit transaction."""
        self.service.edits().delete(
            packageName=package_name,
            editId=edit_id
        ).execute()

    # =========================================================================
    # App Listings & Details
    # =========================================================================
    def get_app_details(self, package_name: str) -> Dict[str, Any]:
        """Fetch general app details and default language."""
        edit_id = self.create_edit(package_name)
        try:
            details = self.service.edits().details().get(
                packageName=package_name, editId=edit_id
            ).execute()
            return {"package_name": package_name, "details": details}
        finally:
            self.delete_edit(package_name, edit_id)

    def get_listings(self, package_name: str) -> List[Dict[str, Any]]:
        """List all localized store listings for an app."""
        edit_id = self.create_edit(package_name)
        try:
            response = self.service.edits().listings().list(
                packageName=package_name, editId=edit_id
            ).execute()
            return response.get("listings", [])
        finally:
            self.delete_edit(package_name, edit_id)

    def update_listing(
        self,
        package_name: str,
        language: str,
        title: Optional[str] = None,
        short_description: Optional[str] = None,
        full_description: Optional[str] = None,
        video_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update or create a localized store listing."""
        edit_id = self.create_edit(package_name)
        try:
            body: Dict[str, Any] = {"language": language}
            if title is not None:
                body["title"] = title
            if short_description is not None:
                body["shortDescription"] = short_description
            if full_description is not None:
                body["fullDescription"] = full_description
            if video_url is not None:
                body["video"] = video_url

            updated = self.service.edits().listings().update(
                packageName=package_name,
                editId=edit_id,
                language=language,
                body=body
            ).execute()

            self.validate_edit(package_name, edit_id)
            self.commit_edit(package_name, edit_id)
            return {"status": "success", "listing": updated}
        except Exception:
            self.delete_edit(package_name, edit_id)
            raise

    # =========================================================================
    # Bundle & APK Uploads
    # =========================================================================
    def upload_bundle(
        self,
        package_name: str,
        aab_path: str,
        ack_bundle_installation_warning: bool = False
    ) -> Dict[str, Any]:
        """Upload an Android App Bundle (.aab)."""
        file_path = Path(aab_path).expanduser()
        if not file_path.is_file():
            raise FileNotFoundError(f"AAB file not found at: {aab_path}")

        edit_id = self.create_edit(package_name)
        try:
            media = MediaFileUpload(str(file_path), mimetype="application/octet-stream", resumable=True)
            upload_req = self.service.edits().bundles().upload(
                packageName=package_name,
                editId=edit_id,
                media_body=media,
                ackBundleInstallationWarning=ack_bundle_installation_warning
            )
            bundle_result = upload_req.execute()
            self.commit_edit(package_name, edit_id)
            return {
                "status": "success",
                "versionCode": bundle_result.get("versionCode"),
                "sha256": bundle_result.get("sha256"),
            }
        except Exception:
            self.delete_edit(package_name, edit_id)
            raise

    # =========================================================================
    # Tracks & Releases (Internal, Closed, Production)
    # =========================================================================
    def list_tracks(self, package_name: str) -> List[Dict[str, Any]]:
        """List all tracks and active releases."""
        edit_id = self.create_edit(package_name)
        try:
            res = self.service.edits().tracks().list(
                packageName=package_name, editId=edit_id
            ).execute()
            return res.get("tracks", [])
        finally:
            self.delete_edit(package_name, edit_id)

    def create_track_release(
        self,
        package_name: str,
        track_name: str,
        version_code: int,
        release_name: Optional[str] = None,
        release_notes: Optional[Dict[str, str]] = None,
        status: str = "completed",
        user_fraction: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Deploy a version code to a release track.
        track_name: 'internal', 'alpha', 'beta', 'production', or 'closed:<name>'
        status: 'draft', 'inProgress', 'halted', 'completed'
        release_notes: dict mapping language code to notes (e.g. {"en-US": "Bug fixes"})
        """
        edit_id = self.create_edit(package_name)
        try:
            release: Dict[str, Any] = {
                "versionCodes": [str(version_code)],
                "status": status,
            }
            if release_name:
                release["name"] = release_name
            if user_fraction is not None and status == "inProgress":
                release["userFraction"] = user_fraction
            if release_notes:
                release["releaseNotes"] = [
                    {"language": lang, "text": text} for lang, text in release_notes.items()
                ]

            body = {
                "track": track_name,
                "releases": [release]
            }

            result = self.service.edits().tracks().update(
                packageName=package_name,
                editId=edit_id,
                track=track_name,
                body=body
            ).execute()

            self.commit_edit(package_name, edit_id)
            return {"status": "success", "track": result}
        except Exception:
            self.delete_edit(package_name, edit_id)
            raise

    # =========================================================================
    # Reviews & Feedback
    # =========================================================================
    def list_reviews(self, package_name: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """List user reviews for an app."""
        res = self.service.reviews().list(
            packageName=package_name,
            maxResults=max_results
        ).execute()
        return res.get("reviews", [])

    def reply_review(self, package_name: str, review_id: str, reply_text: str) -> Dict[str, Any]:
        """Reply to a user review."""
        res = self.service.reviews().reply(
            packageName=package_name,
            reviewId=review_id,
            body={"replyText": reply_text}
        ).execute()
        return {"status": "success", "result": res}
