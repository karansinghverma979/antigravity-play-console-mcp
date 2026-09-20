#!/usr/bin/env python3
"""
Antigravity Play Console Model Context Protocol (MCP) Server
High-speed, robust Python MCP server for Google Play Console and Android Developer API automation.
Author: Karan Singh Verma
Repository: https://github.com/karansinghverma979/antigravity-play-console-mcp
"""

import sys
import json
import os
import traceback
from typing import Any, Dict, Optional

# Ensure src module can be resolved regardless of execution path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from client import PlayConsoleClient

_CLIENT: Optional[PlayConsoleClient] = None

def get_client() -> PlayConsoleClient:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = PlayConsoleClient()
    return _CLIENT

# =============================================================================
# Tool Handlers
# =============================================================================

def handle_play_get_app_details(args: Dict[str, Any]) -> Dict[str, Any]:
    package_name = args.get("package_name")
    if not package_name:
        raise ValueError("package_name is required")
    client = get_client()
    return client.get_app_details(package_name)

def handle_play_get_listings(args: Dict[str, Any]) -> Dict[str, Any]:
    package_name = args.get("package_name")
    if not package_name:
        raise ValueError("package_name is required")
    client = get_client()
    listings = client.get_listings(package_name)
    return {"package_name": package_name, "count": len(listings), "listings": listings}

def handle_play_update_listing(args: Dict[str, Any]) -> Dict[str, Any]:
    package_name = args.get("package_name")
    language = args.get("language", "en-US")
    if not package_name:
        raise ValueError("package_name is required")
    client = get_client()
    return client.update_listing(
        package_name=package_name,
        language=language,
        title=args.get("title"),
        short_description=args.get("short_description"),
        full_description=args.get("full_description"),
        video_url=args.get("video_url")
    )

def handle_play_upload_bundle(args: Dict[str, Any]) -> Dict[str, Any]:
    package_name = args.get("package_name")
    aab_path = args.get("aab_path")
    if not package_name or not aab_path:
        raise ValueError("package_name and aab_path are required")
    client = get_client()
    ack = args.get("ack_bundle_installation_warning", False)
    return client.upload_bundle(package_name, aab_path, ack_bundle_installation_warning=ack)

def handle_play_list_tracks(args: Dict[str, Any]) -> Dict[str, Any]:
    package_name = args.get("package_name")
    if not package_name:
        raise ValueError("package_name is required")
    client = get_client()
    tracks = client.list_tracks(package_name)
    return {"package_name": package_name, "count": len(tracks), "tracks": tracks}

def handle_play_create_release(args: Dict[str, Any]) -> Dict[str, Any]:
    package_name = args.get("package_name")
    track_name = args.get("track", "internal")
    version_code = args.get("version_code")
    if not package_name or version_code is None:
        raise ValueError("package_name and version_code are required")
    client = get_client()
    return client.create_track_release(
        package_name=package_name,
        track_name=track_name,
        version_code=int(version_code),
        release_name=args.get("release_name"),
        release_notes=args.get("release_notes"),
        status=args.get("status", "completed"),
        user_fraction=args.get("user_fraction")
    )

def handle_play_list_reviews(args: Dict[str, Any]) -> Dict[str, Any]:
    package_name = args.get("package_name")
    if not package_name:
        raise ValueError("package_name is required")
    max_results = args.get("max_results", 10)
    client = get_client()
    reviews = client.list_reviews(package_name, max_results=int(max_results))
    return {"package_name": package_name, "count": len(reviews), "reviews": reviews}

def handle_play_reply_review(args: Dict[str, Any]) -> Dict[str, Any]:
    package_name = args.get("package_name")
    review_id = args.get("review_id")
    reply_text = args.get("reply_text")
    if not package_name or not review_id or not reply_text:
        raise ValueError("package_name, review_id, and reply_text are required")
    client = get_client()
    return client.reply_review(package_name, review_id, reply_text)

def handle_play_check_status(args: Dict[str, Any]) -> Dict[str, Any]:
    client = get_client()
    return {
        "status": "online",
        "service_account": client.credentials.service_account_email,
        "key_path": client.key_path,
        "api_endpoint": "https://androidpublisher.googleapis.com/androidpublisher/v3/"
    }

# =============================================================================
# Tool Schema Declarations
# =============================================================================

TOOLS = [
    {
        "name": "play_check_status",
        "description": "Check connection status and active service account for Google Play Developer API.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "play_get_app_details",
        "description": "Retrieve app metadata, package info, and default settings from Google Play.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "The Android application package name (e.g. com.example.app)"}
            },
            "required": ["package_name"]
        }
    },
    {
        "name": "play_get_listings",
        "description": "List all localized store listings (titles, short/full descriptions) for an application.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "Android application package name"}
            },
            "required": ["package_name"]
        }
    },
    {
        "name": "play_update_listing",
        "description": "Update store presence (title, short description, full description, promo video) for a language locale.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "Android application package name"},
                "language": {"type": "string", "description": "BCP-47 language tag (e.g. en-US, hi-IN)", "default": "en-US"},
                "title": {"type": "string", "description": "App display title in Google Play Store"},
                "short_description": {"type": "string", "description": "Short promo summary (max 80 chars)"},
                "full_description": {"type": "string", "description": "Full detailed store description (max 4000 chars)"},
                "video_url": {"type": "string", "description": "YouTube promo video URL"}
            },
            "required": ["package_name", "language"]
        }
    },
    {
        "name": "play_upload_bundle",
        "description": "Upload an Android App Bundle (.aab) to Google Play Console.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "Android application package name"},
                "aab_path": {"type": "string", "description": "Absolute or relative path to the .aab bundle file"},
                "ack_bundle_installation_warning": {"type": "boolean", "description": "Acknowledge installation warnings if present", "default": False}
            },
            "required": ["package_name", "aab_path"]
        }
    },
    {
        "name": "play_list_tracks",
        "description": "List all release tracks (internal, closed, alpha, beta, production) and current active releases.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "Android application package name"}
            },
            "required": ["package_name"]
        }
    },
    {
        "name": "play_create_release",
        "description": "Deploy a version code to a release track (internal, closed, production) with release notes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "Android application package name"},
                "track": {"type": "string", "description": "Target track name: 'internal', 'alpha', 'beta', 'production', or 'closed:<name>'", "default": "internal"},
                "version_code": {"type": "integer", "description": "The versionCode of the uploaded bundle"},
                "release_name": {"type": "string", "description": "Optional human-readable release label (e.g. 1.0.0-rc1)"},
                "release_notes": {"type": "object", "description": "Dictionary of localized release notes (e.g. {\"en-US\": \"New features!\"})"},
                "status": {"type": "string", "enum": ["completed", "draft", "inProgress", "halted"], "default": "completed"},
                "user_fraction": {"type": "number", "description": "Fraction of users for staged rollouts (0.0 to 1.0) when status is inProgress"}
            },
            "required": ["package_name", "version_code"]
        }
    },
    {
        "name": "play_list_reviews",
        "description": "Fetch user reviews, ratings, and comments for an app.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "Android application package name"},
                "max_results": {"type": "integer", "description": "Maximum number of reviews to retrieve", "default": 10}
            },
            "required": ["package_name"]
        }
    },
    {
        "name": "play_reply_review",
        "description": "Reply to a user review on Google Play Store.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "Android application package name"},
                "review_id": {"type": "string", "description": "The unique review ID"},
                "reply_text": {"type": "string", "description": "Response text to publish"}
            },
            "required": ["package_name", "review_id", "reply_text"]
        }
    }
]

DISPATCH_MAP = {
    "play_check_status": handle_play_check_status,
    "play_get_app_details": handle_play_get_app_details,
    "play_get_listings": handle_play_get_listings,
    "play_update_listing": handle_play_update_listing,
    "play_upload_bundle": handle_play_upload_bundle,
    "play_list_tracks": handle_play_list_tracks,
    "play_create_release": handle_play_create_release,
    "play_list_reviews": handle_play_list_reviews,
    "play_reply_review": handle_play_reply_review,
}

# =============================================================================
# JSON-RPC Server Engine
# =============================================================================

def send_json(data: Dict[str, Any]) -> None:
    body = json.dumps(data)
    sys.stdout.write(body + "\n")
    sys.stdout.flush()

def handle_jsonrpc(raw_line: str) -> None:
    line = raw_line.strip()
    if not line:
        return

    try:
        req = json.loads(line)
    except Exception as e:
        send_json({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
        })
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        send_json({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "antigravity-play-console-mcp",
                    "version": "1.0.0"
                }
            }
        })
    elif method == "notifications/initialized":
        pass
    elif method == "tools/list":
        send_json({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        })
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})

        if tool_name not in DISPATCH_MAP:
            send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."}
            })
            return

        try:
            handler = DISPATCH_MAP[tool_name]
            res_data = handler(tool_args)
            send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res_data, indent=2, default=str)
                        }
                    ],
                    "isError": False
                }
            })
        except Exception as err:
            err_details = traceback.format_exc()
            send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error in '{tool_name}': {str(err)}\n\n{err_details}"
                        }
                    ],
                    "isError": True
                }
            })
    elif method == "ping":
        send_json({"jsonrpc": "2.0", "id": req_id, "result": {}})
    else:
        if req_id is not None:
            send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not implemented."}
            })

def main() -> None:
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    for line in sys.stdin:
        handle_jsonrpc(line)

if __name__ == "__main__":
    main()
