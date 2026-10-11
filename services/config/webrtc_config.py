import os
import json
import base64
import urllib.request
import urllib.error
import streamlit as st

DEFAULT_ICE_SERVERS = [
    {
        "urls": [
            "stun:stun.l.google.com:19302",
            "stun:stun1.l.google.com:19302",
            "stun:stun2.l.google.com:19302",
            "stun:stun3.l.google.com:19302",
            "stun:stun4.l.google.com:19302",
        ]
    },
    {
        "urls": ["stun:openrelay.metered.ca:80"]
    },
    {
        "urls": [
            "turn:openrelay.metered.ca:80",
            "turn:openrelay.metered.ca:443",
            "turn:openrelay.metered.ca:443?transport=tcp",
        ],
        "username": "openrelayproject",
        "credential": "openrelayproject",
    },
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


@st.cache_data(ttl=3600, show_spinner=False)
def get_rtc_configuration():
    """
    Returns an RTCConfiguration dictionary containing STUN and TURN iceServers.
    Prioritizes:
    1. Twilio Network Traversal Service (if TWILIO_ACCOUNT_SID & TWILIO_AUTH_TOKEN configured)
    2. Custom TURN configuration in st.secrets (if specified)
    3. High-availability public STUN + free OpenRelay TURN fallback (ensures connectivity on Streamlit Cloud)
    """
    # 1. Check Twilio credentials
    twilio_sid = _get_secret_or_env("TWILIO_ACCOUNT_SID")
    twilio_token = _get_secret_or_env("TWILIO_AUTH_TOKEN")
    if twilio_sid and twilio_token:
        try:
            twilio_servers = _fetch_twilio_ice_servers(twilio_sid, twilio_token)
            if twilio_servers:
                return {"iceServers": twilio_servers}
        except Exception:
            pass

    # 2. Check custom iceServers / rtc_configuration in secrets
    if hasattr(st, "secrets"):
        if "rtc_configuration" in st.secrets:
            return dict(st.secrets["rtc_configuration"])
        if "ice_servers" in st.secrets:
            return {"iceServers": list(st.secrets["ice_servers"])}

    # 3. Check custom TURN server environment variables
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

    # 4. Default: Multi-STUN + Open Relay Project TURN servers
    return {"iceServers": DEFAULT_ICE_SERVERS}
