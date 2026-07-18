from crewai.tools import tool
import pandas as pd


@tool("recommend_ml_problem_type")
def recommend_ml_problem_type(file_path: str, target_column: str) -> dict:
    """
    Recommend the appropriate machine learning problem type.
    """

    try:
        df = pd.read_csv(file_path)

        if target_column not in df.columns:
            return {
                "status": "error",
                "message": f"Target column '{target_column}' not found."
            }

        target = df[target_column]

        # Numeric target
        if pd.api.types.is_numeric_dtype(target):

            unique_ratio = target.nunique() / len(target)

            if unique_ratio < 0.10:
                return {
                    "status": "success",
                    "problem_type": "Classification",
                    "reason": "Numeric target has relatively few unique values."
                }

            return {
                "status": "success",
                "problem_type": "Regression",
                "reason": "Target is continuous numeric."
            }

        # Categorical target
        return {
            "status": "success",
            "problem_type": "Classification",
            "reason": "Target is categorical."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
@tool("suggest_feature_engineering")
def suggest_feature_engineering(file_path: str) -> dict:
    """
    Suggest feature engineering techniques based on the dataset.
    """

    try:
        df = pd.read_csv(file_path)

        suggestions = []

        # Missing values
        if df.isnull().sum().sum() > 0:
            suggestions.append("Handle missing values using imputation or removal.")

        # Categorical columns
        categorical = df.select_dtypes(include=["object", "category"]).columns

        if len(categorical) > 0:
            suggestions.append(
                f"Apply One-Hot Encoding or Label Encoding to: {list(categorical)}"
            )

        # Numeric columns
        numeric = df.select_dtypes(include="number").columns

        if len(numeric) > 0:
            suggestions.append(
                "Consider scaling numeric features using StandardScaler or MinMaxScaler."
            )

        # Duplicate rows
        if df.duplicated().sum() > 0:
            suggestions.append("Remove duplicate rows.")

        # Date columns
        for col in df.columns:
            if "date" in col.lower():
                suggestions.append(
                    f"Extract year, month, day, and weekday from '{col}'."
                )

        if not suggestions:
            suggestions.append("No major feature engineering recommendations detected.")

        return {
            "status": "success",
            "recommendations": suggestions
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
@tool("detect_ml_data_risks")
def detect_ml_data_risks(file_path: str) -> dict:
    """
    Detect common machine learning data quality risks.
    """

    try:
        df = pd.read_csv(file_path)

        risks = []

        # Missing values
        missing = df.isnull().sum().sum()
        if missing > 0:
            risks.append(f"Dataset contains {missing} missing value(s).")

        # Duplicate rows
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            risks.append(f"Dataset contains {duplicates} duplicate row(s).")

        # Constant columns
        constant_columns = [
            col for col in df.columns
            if df[col].nunique() == 1
        ]

        if constant_columns:
            risks.append(
                f"Constant columns detected: {constant_columns}"
            )

        # High-cardinality categorical columns
        for col in df.select_dtypes(include=["object", "category"]).columns:
            if df[col].nunique() > 50:
                risks.append(
                    f"High-cardinality categorical column: {col}"
                )

        # Very small dataset
        if len(df) < 100:
            risks.append(
                "Dataset is very small; model performance may be unreliable."
            )

        if not risks:
            risks.append("No significant ML risks detected.")

        return {
            "status": "success",
            "risks": risks
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
@tool("recommend_evaluation_metrics")
def recommend_evaluation_metrics(problem_type: str) -> dict:
    """
    Recommend evaluation metrics based on the machine learning problem type.
    """

    metrics = {
        "Classification": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1-Score",
            "ROC-AUC"
        ],
        "Regression": [
            "MAE",
            "MSE",
            "RMSE",
            "R² Score"
        ],
        "Clustering": [
            "Silhouette Score",
            "Davies-Bouldin Index",
            "Calinski-Harabasz Score"
        ],
        "Time Series": [
            "MAE",
            "RMSE",
            "MAPE"
        ]
    }

    return {
        "status": "success",
        "problem_type": problem_type,
        "recommended_metrics": metrics.get(
            problem_type,
            ["No recommendation available."]
        )
    }