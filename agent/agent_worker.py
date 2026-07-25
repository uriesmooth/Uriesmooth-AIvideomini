import os
from dotenv import load_dotenv
from livekit.agents import Agent, AgentServer, AgentSession, JobContext, cli
from livekit.plugins import google, deepgram, cartesia, tavus

load_dotenv()

server = AgentServer()

@server.rtc_session(agent_name="uriesmoothai-videomini-agent")
async def my_agent(ctx: JobContext):
    await ctx.connect()

    # Initialize the modern multimodal session container
    session = AgentSession(
        stt=deepgram.STT(model="deepgram/nova-3:multi"),
        llm=google.realtime.RealtimeModel(voice="kore"),
        tts=cartesia.TTS(voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"), 
    )

    # Attach the real-time visual avatar layer
    avatar = tavus.AvatarSession(
        face_id="r90bbd427f71", 
    )

    try:
        await avatar.start(session, ctx.room)
    except Exception as exc:
        print(f"Warning: Visual avatar workspace failed to hook: {exc}")

    # Launch agent instructions and greeting sequence
    await session.start(
        agent=Agent(
            instructions="You are UriesmoothAI-videomini, an advanced digital clone assistant with real-time voice and video tracking."
        ),
        room=ctx.room,
    )
    
    await session.generate_reply(instructions="Greet the user and confirm the UriesmoothAI-videomini secure video and audio stream is live.")

if __name__ == "__main__":
    cli.run_app(server)
