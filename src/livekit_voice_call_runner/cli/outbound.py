import asyncio
import sys
import uuid

from livekit_voice_call_runner import config, factory
from livekit_voice_call_runner.logger import create_logger
from livekit_voice_call_runner.outbound.call_runner import OutboundCallRunner

logger = create_logger(name=__name__, correlation_id=str(uuid.uuid4()))


async def _run(args) -> None:
    instructions = open(args.instructions_path, encoding="utf-8").read()

    cfg = config.base.get_config()
    outbound_cfg = config.outbound.get_config()
    livekit_api = factory.create_livekit_api(cfg=cfg)

    try:
        call_runner_props = factory.create_call_runner_props(
            instructions=instructions,
            phone_number_to=args.phone_number,
            sip_uri=args.sip_uri,
            correlation_id=str(uuid.uuid4()),
            cfg=cfg,
            outbound_cfg=outbound_cfg,
            livekit_api=livekit_api,
        )
        await OutboundCallRunner(props=call_runner_props).run()
        logger.info("Successfully ran.")
        sys.exit(0)
    except Exception as e:
        logger.error("Failed to run.", extra={"error": str(e)})
        sys.exit(1)


def run(args) -> None:
    asyncio.run(_run(args))
