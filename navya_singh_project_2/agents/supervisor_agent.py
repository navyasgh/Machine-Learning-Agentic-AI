import yaml

from crewai import Agent

from llm import llm

from function_tools.supervisor_tools import (
    classify_user_request,
    create_agent_work_plan,
    summarize_chat_history,
    validate_final_response_structure
)


def load_config():
    with open("config/agents.yaml", "r") as file:
        return yaml.safe_load(file)


config = load_config()["supervisor"]


supervisor_agent = Agent(
    role=config["role"],
    goal=config["goal"],
    backstory=config["backstory"],
    llm=llm,
    tools=[
        classify_user_request,
        create_agent_work_plan,
        summarize_chat_history,
        validate_final_response_structure
    ],
    verbose=True
)