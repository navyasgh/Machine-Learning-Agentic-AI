import yaml


def load_agents_config():
    with open("config/agents.yaml", "r") as file:
        return yaml.safe_load(file)


def load_tasks_config():
    with open("config/tasks.yaml", "r") as file:
        return yaml.safe_load(file)