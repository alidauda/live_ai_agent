from src.solana_agent_agentipy.crew import SolanaWalletCrew
import asyncio

if __name__ == "__main__":
    crew = SolanaWalletCrew().crew()
    result = asyncio.run(crew.kickoff(inputs={
        "user_input": "Check my balance and send 1 SOL if I’m above $1000"
    }))
    print(result)
