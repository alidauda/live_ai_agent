from solana_agent_agentipy.crew import SolanaWalletCrew
import asyncio

async def main():
    print("🚀 Starting main execution")
    print("🔧 Creating SolanaWalletCrew instance")
    crew_instance = SolanaWalletCrew()
    print("✅ SolanaWalletCrew instance created")
    
    print("🔧 Getting crew")
    crew = crew_instance.crew()
    print("✅ Got crew")
    
    print("🔧 Starting crew execution")
    result = await crew.kickoff(inputs={
        "user_input": "Check my balance and send 1 SOL if I'm above $1000"
    })
    print("✅ Crew execution completed")
    print("\n✅ Final Output:\n", result.raw if hasattr(result, "raw") else result)

if __name__ == "__main__":
    print("🏁 Starting application")
    asyncio.run(main())
