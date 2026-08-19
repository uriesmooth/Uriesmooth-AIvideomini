import asyncio
import logging
from livekit import agents
from livekit.agents import AgentSession, Agent, JobContext
from livekit.plugins import openai

logger = logging.getLogger("urielsmooth-voice")

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(voice="coral")
    )

    async def safe_tool_wrapper(coro_func, *args, **kwargs):
        try:
            return await coro_func(*args, **kwargs)
        except asyncio.TimeoutError:
            logger.error("Financial API timeout during tool execution.")
            await session.generate_reply(instructions="Apologize briefly and ask to retry.")
        except Exception as e:
            logger.exception(f"Unhandled error: {e}")
            await session.generate_reply(instructions="Inform the user of a temporary ledger fault.")

    try:
        await session.start(
            room=ctx.room,
            agent=Agent(instructions="You are Urielsmooth Financial Voice Assistant.")
        )
        await session.generate_reply(instructions="Greet the user, confirm secure connection.")
    except Exception as e:
        logger.critical(f"Critical session crash: {e}")
        raise

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
