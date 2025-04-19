from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from agentipy.agent import SolanaAgentKit
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from solana_agent_agentipy.tools.custom_tool import make_balance_tool

load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SolanaWalletCrew():
    """SolanaAgentAgentipy crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    def __init__(self):
        self.kit = SolanaAgentKit(
        private_key=os.getenv("SOLANA_PRIVATE_KEY"),
        rpc_url="https://api.devnet.solana.com"
    )

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    

    @agent
    def solana_operator(self) -> Agent:
        return Agent(
            config=self.agents_config['solana_operator'],
            tools=[
                make_balance_tool(agent=self.kit),
               
            ],
            llm=ChatOpenAI(model=os.getenv("MODEL"), temperature=0),
        verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    

    @task
    def wallet_intel(self) -> Task:
        return Task(
        config=self.tasks_config['wallet_intel'],
        agent=self.solana_operator
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
        agents=[self.solana_operator],
        tasks=[self.wallet_intel],
        process=Process.sequential,
        verbose=True
    )
