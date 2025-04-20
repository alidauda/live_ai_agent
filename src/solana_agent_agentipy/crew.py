from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from agentipy.agent import SolanaAgentKit
from solana_agent_agentipy.tools.custom_tool import make_balance_tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai.process import Process
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@CrewBase
class SolanaWalletCrew:
    """SolanaAgentAgentipy crew"""

    def __init__(self):
        logger.info("🔧 Initializing SolanaWalletCrew")
        try:
            self.kit = SolanaAgentKit(
                private_key=os.getenv("SOLANA_PRIVATE_KEY"),
                rpc_url="https://api.devnet.solana.com"
            )
            logger.info("✅ SolanaAgentKit initialized")
            self._operator = None
            self._balance_tool = None
        except Exception as e:
            logger.error(f"Failed to initialize SolanaWalletCrew: {str(e)}")
            raise

    def _get_balance_tool(self):
        if self._balance_tool is None:
            logger.info("🔧 Creating balance tool")
            self._balance_tool = make_balance_tool(agent=self.kit)
            logger.info("✅ Balance tool created")
        return self._balance_tool

    @agent
    def solana_operator(self) -> Agent:
        if self._operator is None:
            logger.info("🔧 Creating solana_operator agent")
            try:
                balance_tool = self._get_balance_tool()
                
                self._operator = Agent(
                    role="Solana Wallet Agent",
                    goal="Help the user with natural language wallet actions using planning and real-time tools.",
                    backstory="You are a powerful AI wallet assistant that can fetch balances, prices, and conditionally send tokens.",
                    tools=[balance_tool],
                    llm=ChatOpenAI(model=os.getenv("MODEL"), temperature=0),
                    verbose=True,
                    allow_delegation=False
                )
                logger.info("✅ solana_operator agent created")
            except Exception as e:
                logger.error(f"Failed to create solana_operator agent: {str(e)}")
                raise
        return self._operator

    
    @task
    def wallet_intel(self):
        return {
        "description": """
            Analyze the following instruction and take appropriate action using tools: {user_input}
            Handle balance checks, valuation, and conditional transfers.
        """,
        "expected_output": """
            Respond with SOL balance, current valuation, or transfer confirmation.
        """,
        "agent": self.solana_operator()
    }


    @crew
    def crew(self) -> Crew:
        logger.info("🔧 Creating crew")
        try:
            operator = self.solana_operator()
            logger.info("✅ Got operator agent for crew")
            
            task = self.wallet_intel()
            logger.info("✅ Got wallet_intel task")
            
            crew = Crew(
                agents=[operator],
                tasks=[task],
                process=Process.sequential,
                verbose=True,
                memory=False
            )
            logger.info("✅ Crew created")
            return crew
        except Exception as e:
            logger.error(f"Failed to create crew: {str(e)}")
            raise
