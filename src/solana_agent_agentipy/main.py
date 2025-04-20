from solana_agent_agentipy.crew import SolanaWalletCrew
import asyncio

async def main():
    crew = SolanaWalletCrew().crew()
    result = await crew.kickoff(inputs={
        "user_input": "Check my balance and send 1 SOL if I'm above $1000"
    })
    print("\n✅ Final Output:\n", result.raw if hasattr(result, "raw") else result)

if __name__ == "__main__":
    asyncio.run(main())
