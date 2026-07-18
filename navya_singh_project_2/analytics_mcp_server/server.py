from mcp.server.fastmcp import FastMCP

from function_tools.analyst_tools import (
    profile_dataframe,
    suggest_kpi_metrics,
    generate_dashboard_layout,
    validate_sql_safety
)

from function_tools.scientist_tools import (
    recommend_ml_problem_type,
    suggest_feature_engineering,
    detect_ml_data_risks,
    recommend_evaluation_metrics
)

mcp = FastMCP("analytics_mcp_server")


# ---------------------------
# Data Analyst Tools
# ---------------------------

@mcp.tool()
def mcp_profile_csv(file_path: str):
    """Profile a CSV dataset."""
    return profile_dataframe.run(file_path)


@mcp.tool()
def mcp_generate_kpi_catalog(file_path: str):
    """Generate KPI recommendations."""
    return suggest_kpi_metrics.run(file_path)


@mcp.tool()
def mcp_generate_dashboard(file_path: str):
    """Generate dashboard recommendations."""
    return generate_dashboard_layout.run(file_path)


@mcp.tool()
def mcp_validate_sql(query: str):
    """Validate SQL safety."""
    return validate_sql_safety.run(query)


# ---------------------------
# Data Scientist Tools
# ---------------------------

@mcp.tool()
def mcp_recommend_ml_use_cases(file_path: str, target_column: str):
    """Recommend ML problem type."""
    return recommend_ml_problem_type.run(file_path, target_column)


@mcp.tool()
def mcp_feature_engineering_suggestions(file_path: str):
    """Suggest feature engineering."""
    return suggest_feature_engineering.run(file_path)


@mcp.tool()
def mcp_detect_data_quality_issues(file_path: str):
    """Detect ML/data quality issues."""
    return detect_ml_data_risks.run(file_path)


@mcp.tool()
def mcp_recommend_evaluation_metrics(problem_type: str):
    """Recommend evaluation metrics."""
    return recommend_evaluation_metrics.run(problem_type)


if __name__ == "__main__":
    mcp.run(transport="stdio")