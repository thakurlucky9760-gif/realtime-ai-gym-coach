import os
import json
import base64
import urllib.request
import urllib.error
import streamlit as st

# Reliable, active public STUN servers for NAT discovery
DEFAULT_ICE_SERVERS = [
    {
        "urls": [
            "stun:stun.l.google.com:19302",
            "stun:stun1.l.google.com:19302",
            "stun:stun2.l.google.com:19302",
            "stun:stun3.l.google.com:19302",
            "stun:stun4.l.google.com:19302",
            "stun:stun.cloudflare.com:3478",
            "stun:global.stun.twilio.com:3478",
        ]
    }
]

MEDIA_STREAM_CONSTRAINTS = {
    "video": {
        "width": {"ideal": 640, "max": 1280},
        "height": {"ideal": 480, "max": 720},
        "frameRate": {"ideal": 30, "max": 30},
    },
    "audio": False,
}


def _get_secret_or_env(key: str, default: str = "") -> str:
    """Helper to fetch a secret from st.secrets or os.environ."""
    if hasattr(st, "secrets") and key in st.secrets:
        return str(st.secrets[key])
    return os.environ.get(key, default)


def _fetch_cloudflare_turn(key_id: str, api_token: str):
    """Fetch temporary ICE servers from Cloudflare Realtime TURN API."""
    url = f"https://rtc.live.cloudflare.com/v1/turn/keys/{key_id}/credentials/generate-ice-servers"
    req = urllib.request.Request(
        url,
        data=json.dumps({"ttl": 7200}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
        if "iceServers" in data:
            return data["iceServers"]
    return None


def _fetch_twilio_ice_servers(account_sid: str, auth_token: str):
    """Fetch temporary ICE servers from Twilio Network Traversal API."""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Tokens.json"
    req = urllib.request.Request(url, data=b"", method="POST")
    auth_str = f"{account_sid}:{auth_token}"
    auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
    req.add_header("Authorization", f"Basic {auth_b64}")

    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
        if "ice_servers" in data:
            return data["ice_servers"]
    return None


def _fetch_metered_turn(domain: str, api_key: str):
    """Fetch temporary ICE servers from Metered TURN API."""
    url = f"https://{domain}.metered.live/api/v1/turn/credentials?apiKey={api_key}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
        if isinstance(data, list):
            return data
    return None


def is_turn_configured() -> bool:
    """Returns True if any TURN relay service credentials are configured."""
    # Cloudflare
    if _get_secret_or_env("CLOUDFLARE_TURN_KEY_ID") and _get_secret_or_env("CLOUDFLARE_TURN_KEY_API_TOKEN"):
        return True
    # Twilio
    if _get_secret_or_env("TWILIO_ACCOUNT_SID") and _get_secret_or_env("TWILIO_AUTH_TOKEN"):
        return True
    # Metered
    if _get_secret_or_env("METERED_DOMAIN") and _get_secret_or_env("METERED_API_KEY"):
        return True
    # Custom
    if _get_secret_or_env("TURN_SERVER_URL"):
        return True
    # Secrets object
    if hasattr(st, "secrets") and ("rtc_configuration" in st.secrets or "ice_servers" in st.secrets):
        return True
    return False


@st.cache_data(ttl=3600, show_spinner=False)
def get_rtc_configuration():
    """
    Returns an RTCConfiguration dictionary containing STUN and TURN iceServers.
    Supports Cloudflare Realtime TURN, Twilio, Metered, and custom TURN servers.
    """
    # 1. Check Cloudflare Realtime TURN credentials
    cf_key = _get_secret_or_env("CLOUDFLARE_TURN_KEY_ID")
    cf_token = _get_secret_or_env("CLOUDFLARE_TURN_KEY_API_TOKEN")
    if cf_key and cf_token:
        try:
            cf_servers = _fetch_cloudflare_turn(cf_key, cf_token)
            if cf_servers:
                return {"iceServers": cf_servers}
        except Exception:
            pass

    # 2. Check Twilio credentials
    twilio_sid = _get_secret_or_env("TWILIO_ACCOUNT_SID")
    twilio_token = _get_secret_or_env("TWILIO_AUTH_TOKEN")
    if twilio_sid and twilio_token:
        try:
            twilio_servers = _fetch_twilio_ice_servers(twilio_sid, twilio_token)
            if twilio_servers:
                return {"iceServers": twilio_servers}
        except Exception:
            pass

    # 3. Check Metered credentials
    metered_domain = _get_secret_or_env("METERED_DOMAIN")
    metered_key = _get_secret_or_env("METERED_API_KEY")
    if metered_domain and metered_key:
        try:
            metered_servers = _fetch_metered_turn(metered_domain, metered_key)
            if metered_servers:
                return {"iceServers": metered_servers}
        except Exception:
            pass

    # 4. Check custom iceServers / rtc_configuration in secrets
    if hasattr(st, "secrets"):
        if "rtc_configuration" in st.secrets:
            return dict(st.secrets["rtc_configuration"])
        if "ice_servers" in st.secrets:
            return {"iceServers": list(st.secrets["ice_servers"])}

    # 5. Check custom TURN server environment variables
    custom_turn_url = _get_secret_or_env("TURN_SERVER_URL")
    custom_turn_user = _get_secret_or_env("TURN_USERNAME")
    custom_turn_cred = _get_secret_or_env("TURN_PASSWORD") or _get_secret_or_env("TURN_CREDENTIAL")

    if custom_turn_url:
        custom_entry = {"urls": [custom_turn_url]}
        if custom_turn_user and custom_turn_cred:
            custom_entry["username"] = custom_turn_user
            custom_entry["credential"] = custom_turn_cred

        return {
            "iceServers": [
                {"urls": ["stun:stun.l.google.com:19302"]},
                custom_entry,
            ]
        }

    # 6. Default: Multi-provider verified STUN servers
    return {"iceServers": DEFAULT_ICE_SERVERS}
