from crewai.tools import tool

@tool("classify_user_request")
def classify_user_request(user_request: str) -> dict:
    """
    Classify the user request and recommend which agent should handle it.
    """

    request = user_request.lower()

    if any(word in request for word in ["sql", "query", "select"]):
        return {
            "intent": "sql",
            "recommended_agent": "Data Analyst Agent",
            "reason": "The request involves SQL analysis or validation."
        }
    
    elif ("dashboard" in request or "kpi" in request) and (
        "machine learning" in request or "model" in request
    ):
        return {
            "intent": "mixed",
            "recommended_agent": "Both Agents",
            "reason": "The request requires business analytics and machine learning."
        }

    elif any(word in request for word in ["dashboard", "kpi", "revenue", "report"]):
        return {
            "intent": "dashboard",
            "recommended_agent": "Data Analyst Agent",
            "reason": "The request focuses on reporting or dashboard design."
        }

    elif any(word in request for word in ["machine learning", "predict", "classification",
                                          "regression", "model", "feature"]):
        return {
            "intent": "data_science",
            "recommended_agent": "Data Scientist Agent",
            "reason": "The request involves machine learning."
        }

    elif any(word in request for word in ["quality", "missing", "duplicates", "outliers"]):
        return {
            "intent": "data_quality",
            "recommended_agent": "Data Scientist Agent",
            "reason": "The request concerns data quality."
        }

    return {
        "intent": "analytics",
        "recommended_agent": "Supervisor Agent",
        "reason": "General analytics request."
    }

from crewai.tools import tool

@tool("create_agent_work_plan")
def create_agent_work_plan(intent: str) -> dict:
    """
    Generate a work plan based on the classified user intent.
    """

    work_plans = {
        "analytics": [
            "Ask Data Analyst Agent to analyze the dataset.",
            "Generate business insights.",
            "Prepare the final response."
        ],
        "mixed": [
            "Ask Data Analyst Agent to profile the dataset.",
            "Ask Data Analyst Agent to recommend KPIs.",
            "Ask Data Scientist Agent to recommend ML use cases.",
            "Ask Data Scientist Agent to suggest feature engineering ideas.",
            "Combine all responses into the final answer."
        ],
        "dashboard": [
            "Ask Data Analyst Agent to profile the dataset.",
            "Suggest KPIs.",
            "Recommend dashboard layout."
        ],
        "sql": [
            "Ask Data Analyst Agent to validate the SQL query.",
            "Suggest improvements if needed."
        ],
        "data_science": [
            "Ask Data Scientist Agent to identify the ML problem type.",
            "Suggest feature engineering ideas.",
            "Recommend evaluation metrics."
        ],
        "data_quality": [
            "Ask Data Scientist Agent to detect data quality issues.",
            "Summarize the identified risks."
        ]        
    }

    return {
        "intent": intent,
        "steps": work_plans.get(
            intent,
            ["Review the request and generate a response."]
        )
    }

@tool("summarize_chat_history")
def summarize_chat_history(chat_history: list[str]) -> str:
    """
    Summarize previous conversation messages.
    """

    if not chat_history:
        return "No previous conversation."

    if len(chat_history) <= 3:
        return "\n".join(chat_history)

    summary = (
        f"Conversation contains {len(chat_history)} messages.\n"
        f"First request: {chat_history[0]}\n"
        f"Latest request: {chat_history[-1]}"
    )

    return summary

@tool("validate_final_response_structure")
def validate_final_response_structure(response: str) -> dict:
    """
    Validate whether the final response is well-structured.
    """

    checks = {
        "has_content": len(response.strip()) > 0,
        "sufficient_length": len(response.split()) >= 20,
        "ends_properly": response.strip().endswith((".", "!", "?"))
    }

    checks["is_valid"] = all(checks.values())

    return checks