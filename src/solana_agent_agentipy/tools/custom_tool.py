from crewai_tools import tool
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_balance import BalanceFetcher
import asyncio

def make_balance_tool(agent: SolanaAgentKit):
    @tool("Get SOL Balance")
    def get_sol_balance() -> str:
        """Fetches and returns the SOL balance of the agent's wallet."""
        import asyncio

        async def fetch():
            try:
                balance = await BalanceFetcher.get_balance(agent)
                return f"The current SOL balance is {balance:.4f} SOL"
            except Exception as e:
                return f"Error fetching balance: {str(e)}"

        return asyncio.run(fetch())

    return get_sol_balance
