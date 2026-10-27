import pytest
from livekit.protocol import sip

from livekit_voice_call_runner.outbound.sip_uri import is_sip_uri, parse_sip_uri


def test_parse_sip_uri_with_port_and_transport():
    uri = parse_sip_uri("sip:+15076691718@host.example.com:5060;transport=tcp")

    assert uri.user == "+15076691718"
    assert uri.hostname == "host.example.com:5060"
    assert uri.transport == sip.SIPTransport.SIP_TRANSPORT_TCP


def test_parse_sip_uri_defaults_to_auto_transport():
    assert parse_sip_uri("sip:user@host").transport == sip.SIPTransport.SIP_TRANSPORT_AUTO


def test_parse_sips_uri_uses_tls():
    assert parse_sip_uri("sips:user@host").transport == sip.SIPTransport.SIP_TRANSPORT_TLS


@pytest.mark.parametrize("value", ["+15076691718", "user@host", "sip:host", "sip:user@host;transport=sctp"])
def test_parse_sip_uri_rejects_invalid(value):
    with pytest.raises(ValueError):
        parse_sip_uri(value)


def test_is_sip_uri():
    assert is_sip_uri("SIP:user@host")
    assert not is_sip_uri("+15076691718")
