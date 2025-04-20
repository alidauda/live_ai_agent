from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from agentipy.agent import SolanaAgentKit
from solana_agent_agentipy.tools.custom_tool import make_balance_tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import yaml

load_dotenv()

@CrewBase
class SolanaWalletCrew:
    """SolanaAgentAgentipy crew"""

    # Define static paths
    agents_config_path = os.path.join(os.path.dirname(__file__), 'config/agents.yaml')
    tasks_config_path = os.path.join(os.path.dirname(__file__), 'config/tasks.yaml')

    def __init__(self):
        self.kit = SolanaAgentKit(
            private_key=os.getenv("SOLANA_PRIVATE_KEY"),
            rpc_url="https://api.devnet.solana.com"
        )

    def _load_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    @agent
    def solana_operator(self) -> Agent:
        config = self._load_yaml(self.agents_config_path)['solana_operator']
        print("✅ Loaded agent config:", type(config))
        return Agent(
            config=config,
            tools=[
                make_balance_tool(agent=self.kit),
            ],
            llm=ChatOpenAI(model=os.getenv("MODEL"), temperature=0),
            verbose=True
        )

    @task
    def wallet_intel(self) -> Task:
        config = self._load_yaml(self.tasks_config_path)['wallet_intel']
        print("✅ Loaded task config:", type(config))
        return Task(
            config=config,
            agent=self.solana_operator
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.solana_operator],
            tasks=[self.wallet_intel]
        )
