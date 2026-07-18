from crewai import Crew, Task

from agents.supervisor_agent import supervisor_agent
from agents.data_analyst_agent import data_analyst_agent
from agents.data_scientist_agent import data_scientist_agent

supervisor_task = Task(
    description="""
    User Request:
    {user_request}

    Use your tools to classify the request and create a work plan.
    """,
    expected_output="Classification and work plan.",
    agent=supervisor_agent
)

analyst_task = Task(
    description="""
    User Request:
    {user_request}

    Dataset:
    {dataset_path}

    Use your tools to:
    - Profile the dataset
    - Suggest KPIs
    - Recommend dashboard layout
    - Validate SQL if required
    """,
    expected_output="Business analytics report.",
    agent=data_analyst_agent,
    context=[supervisor_task]
)

scientist_task = Task(
    description="""
    User Request:
    {user_request}

    Dataset:
    {dataset_path}

    Use your tools to:
    - Determine ML problem
    - Suggest feature engineering
    - Detect ML risks
    - Recommend evaluation metrics
    """,
    expected_output="Machine learning report.",
    agent=data_scientist_agent,
    context=[supervisor_task]
)

final_task = Task(
    description="""
    Combine the outputs into one professional response.
    """,
    expected_output="Final report.",
    agent=supervisor_agent,
    context=[analyst_task, scientist_task]
)

def create_analytics_crew():
    return Crew(
        agents=[
            supervisor_agent,
            data_analyst_agent,
            data_scientist_agent
        ],
        tasks=[
            supervisor_task,
            analyst_task,
            scientist_task,
            final_task
        ],
        verbose=True
    )