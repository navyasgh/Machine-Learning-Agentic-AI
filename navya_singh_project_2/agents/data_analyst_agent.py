from crewai import Agent
from llm import llm
import yaml
from config.config_loader import load_agents_config
from function_tools.analyst_tools import (
    profile_dataframe,
    suggest_kpi_metrics,
    generate_dashboard_layout,
    validate_sql_safety
)
tools=[
    profile_dataframe,
    suggest_kpi_metrics,
    generate_dashboard_layout,
    validate_sql_safety
]


def load_agent_config():
    with open("config/agents.yaml", "r") as file:
        return yaml.safe_load(file)


config = load_agent_config()["data_analyst"]

data_analyst_agent = Agent(
    role=config["role"],
    goal=config["goal"],
    backstory=config["backstory"],
    llm=llm,
    tools=tools,
    verbose=True
)