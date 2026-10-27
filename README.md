# livekit-voice-call-runner

A LiveKit-powered voice call runner that supports both **outbound** (dial-out) and **inbound** (listen for incoming) call directions, driven by a configurable AI agent.

## Prerequisites

- Pyenv 2.6.27: `brew install pyenv`
- Python 3.13.13: `pyenv install 3.13.13`
- Poetry 2.1.3: `brew install poetry`
- direnv 2.37.1: `brew install direnv`
- LiveKit Project
- Azure OpenAI Subscription

## Setup

```bash
cp .env.template .env # hint: update placeholders
poetry install --with dev
poetry config virtualenvs.in-project true
poetry run pre-commit install
direnv allow
```

## Run it

### Outbound — dial out to a phone number or a SIP URI

```bash
poetry run livekit_voice_call_runner \
    --direction outbound \
    --phone-number +1234567890 \
    --instructions-path examples/instructions/discuss_car_issue.md

poetry run livekit_voice_call_runner \
    --direction outbound \
    --sip-uri "sip:+12345678901@a.b.c;transport=tcp" \
    --instructions-path examples/instructions/discuss_car_issue.md
```

### Inbound — listen for incoming calls

```bash
poetry run livekit_voice_call_runner \
    --direction inbound \
    --instructions-path examples/instructions/answer_service_call.md
```

## CLI flags

| Flag | Required | Description |
|---|---|---|
| `--direction` | yes | `outbound` or `inbound` |
| `--instructions-path` | yes | Path to the agent instructions file |
| `--phone-number` | outbound only | Phone number to dial |
| `--sip-uri` | outbound only | SIP URI(s), e.g. `sip:user@host;transport=tcp`, to dial directly |
