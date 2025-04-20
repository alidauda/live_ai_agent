from crewai.tools import tool
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_balance import BalanceFetcher
import asyncio

def make_balance_tool(agent: SolanaAgentKit):
    @tool("get_sol_balance")
    def get_sol_balance() -> str:
        """Fetches and returns the SOL balance of the agent's wallet."""
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            balance = loop.run_until_complete(BalanceFetcher.get_balance(agent))
            loop.close()
            return f"The current SOL balance is {balance:.4f} SOL"
        except Exception as e:
            return f"Error fetching balance: {str(e)}"
    return get_sol_balance
