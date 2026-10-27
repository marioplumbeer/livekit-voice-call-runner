from typing import Optional
from urllib.parse import unquote

from livekit.protocol import sip
from pydantic import BaseModel

_SCHEMES = ("sip:", "sips:")
_TRANSPORTS = {
    "udp": sip.SIPTransport.SIP_TRANSPORT_UDP,
    "tcp": sip.SIPTransport.SIP_TRANSPORT_TCP,
    "tls": sip.SIPTransport.SIP_TRANSPORT_TLS,
}


class SipUri(BaseModel):
    user: str
    hostname: str
    transport: int


def is_sip_uri(value: str) -> bool:
    return value.lower().startswith(_SCHEMES)


def parse_sip_uri(uri: str) -> SipUri:
    """Parse `sip[s]:user@host[:port][;transport=tcp]` into its dialable parts."""
    if not is_sip_uri(value=uri):
        raise ValueError(f"Not a SIP URI: {uri}")

    scheme, rest = uri.split(":", 1)
    address, *params = rest.split(";")
    user, sep, hostname = address.rpartition("@")
    if not sep or not user or not hostname:
        raise ValueError(f"SIP URI must be in the form sip:user@host: {uri}")

    transport: Optional[int] = _TRANSPORTS["tls"] if scheme.lower() == "sips" else None
    for param in params:
        key, _, value = param.partition("=")
        if key.lower() == "transport":
            if value.lower() not in _TRANSPORTS:
                raise ValueError(f"Unsupported SIP transport '{value}': {uri}")
            transport = _TRANSPORTS[value.lower()]

    return SipUri(
        user=unquote(user),
        hostname=hostname,
        transport=transport
        if transport is not None
        else sip.SIPTransport.SIP_TRANSPORT_AUTO,
    )
