from pathlib import Path
import pandas as pd
from crewai.tools import tool

@tool("profile_dataframe")
def profile_dataframe(file_path: str) -> dict:
    """
    Generate a summary profile of a CSV dataset.
    """
    print("PROFILE TOOL CALLED")

    try:
        path = Path(file_path)

        if not path.exists():
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }

        df = pd.read_csv(path)

        return {
            "status": "success",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "numeric_columns": list(df.select_dtypes(include="number").columns),
            "categorical_columns": list(df.select_dtypes(exclude="number").columns)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    

@tool("suggest_kpi_metrics")
def suggest_kpi_metrics(file_path: str) -> dict:
    """
    Suggest KPIs based on the dataset columns.
    """

    df = pd.read_csv(file_path)

    kpis = []

    columns = [col.lower() for col in df.columns]

    if "sales" in columns:
        kpis.extend([
            "Total Sales",
            "Average Sales",
            "Sales Growth"
        ])

    if "profit" in columns:
        kpis.extend([
            "Total Profit",
            "Average Profit"
        ])

    if "quantity" in columns:
        kpis.extend([
            "Units Sold",
            "Average Order Quantity"
        ])

    if "customer" in columns:
        kpis.append("Customer Count")

    if "region" in columns:
        kpis.append("Sales by Region")

    if "product" in columns:
        kpis.append("Top Selling Products")

    if any(col in columns for col in ["date", "orderdate", "order_date"]):
        kpis.append("Monthly Sales Trend")

    if not kpis:
        kpis.append("No specific KPIs detected. Review dataset manually.")

    return {
        "recommended_kpis": kpis
    }

@tool("generate_dashboard_layout")
def generate_dashboard_layout(file_path: str) -> dict:
    """
    Recommend a dashboard layout based on the dataset columns.
    """

    df = pd.read_csv(file_path)
    columns = [col.lower() for col in df.columns]

    dashboard = {
        "kpi_cards": [],
        "charts": [],
        "tables": []
    }

    # KPI Cards
    if "sales" in columns:
        dashboard["kpi_cards"].append("Total Sales")

    if "profit" in columns:
        dashboard["kpi_cards"].append("Total Profit")

    if "customer" in columns:
        dashboard["kpi_cards"].append("Customer Count")

    # Charts
    if "region" in columns and "sales" in columns:
        dashboard["charts"].append({
            "type": "Bar Chart",
            "title": "Sales by Region"
        })

    if "product" in columns and "sales" in columns:
        dashboard["charts"].append({
            "type": "Bar Chart",
            "title": "Top Selling Products"
        })

    if any(col in columns for col in ["date", "orderdate", "order_date"]) and "sales" in columns:
        dashboard["charts"].append({
            "type": "Line Chart",
            "title": "Sales Trend"
        })

    if "profit" in columns:
        dashboard["charts"].append({
            "type": "Histogram",
            "title": "Profit Distribution"
        })

    # Tables
    dashboard["tables"].append("Detailed Transaction Table")

    return dashboard

import re

@tool("validate_sql_safety")
def validate_sql_safety(query: str) -> dict:
    """
    Validate whether a SQL query is safe to execute.
    """

    query = query.strip()

    dangerous_keywords = [
        "DROP",
        "DELETE",
        "TRUNCATE",
        "ALTER",
        "UPDATE",
        "INSERT",
        "CREATE",
        "EXEC",
        "MERGE"
    ]

    upper_query = query.upper()

    detected = [
        keyword for keyword in dangerous_keywords
        if re.search(rf"\b{keyword}\b", upper_query)
    ]

    if detected:
        return {
            "status": "unsafe",
            "allowed": False,
            "reason": f"Dangerous SQL keyword(s) detected: {', '.join(detected)}"
        }

    if not upper_query.startswith("SELECT"):
        return {
            "status": "warning",
            "allowed": False,
            "reason": "Only SELECT queries are permitted."
        }

    return {
        "status": "safe",
        "allowed": True,
        "reason": "Query is safe to execute."
    }