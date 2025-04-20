from solana_agent_agentipy.crew import SolanaWalletCrew


def run():
    """
    Run the crew.
    """
    inputs = {"user_input": "Check my balance and send 1 SOL if I’m above $1000"}
    SolanaWalletCrew().crew().kickoff(inputs=inputs)

