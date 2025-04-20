from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from agentipy.agent import SolanaAgentKit
from solana_agent_agentipy.tools.custom_tool import make_balance_tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai.process import Process

load_dotenv()

@CrewBase
class SolanaWalletCrew:
    """SolanaAgentAgentipy crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.kit = SolanaAgentKit(
            private_key=os.getenv("SOLANA_PRIVATE_KEY"),
            rpc_url="https://api.devnet.solana.com"
        )
        

   

    @agent
    def solana_operator(self) -> Agent:
        return Agent(
                config=self.agents_config["solana_operator"],
                tools=[ make_balance_tool(agent=self.kit)],
                llm=ChatOpenAI(model=os.getenv("MODEL"), temperature=0),
                verbose=True,
                allow_delegation=False
            )
       

    @task
    def solana_operation(self) -> Task:
        return Task(
            description=self.tasks_config['solana_operation']['description'],
            expected_output=self.tasks_config['solana_operation']['expected_output'],
            agent=self.solana_operator(),
            async_execution=True
        )

    @crew
    def crew(self) -> Crew:
   
        
        return Crew(
            agents=[self.solana_operator()],
            tasks=[self.solana_operation()],
            process=Process.sequential,
            verbose=True,
            memory=False
        )
