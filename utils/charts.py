"""
charts.py
Pure figure-building functions. Every function takes data in and returns a
Plotly figure — no Streamlit calls in here, so these are easy to reuse and
test across pages.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.styles import PLOTLY_COLORWAY

MINT = "#58C9A8"
CORAL = "#FF6B6B"
SKY = "#77B7E8"


def _base_layout(fig, title=None, height=380):
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=10, r=10, t=50 if title else 20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Nunito, sans-serif", color="#2E3B40"),
        colorway=PLOTLY_COLORWAY,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def risk_distribution_pie(df: pd.DataFrame, col: str = "risk_level") -> go.Figure:
    counts = df[col].value_counts().reset_index()
    counts.columns = ["Risk Level", "Count"]
    fig = px.pie(
        counts,
        names="Risk Level",
        values="Count",
        hole=0.55,
        color="Risk Level",
        color_discrete_map={"Healthy": MINT, "At Risk": CORAL},
    )
    fig.update_traces(textinfo="percent+label", textfont_size=13)
    return _base_layout(fig, height=340)


def probability_gauge(prob: float, label: str) -> go.Figure:
    """Gauge chart showing confidence % for the predicted class."""
    color = MINT if label == "Healthy" else CORAL
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(prob * 100, 1),
            number={"suffix": "%", "font": {"size": 36}},
            title={"text": f"Confidence: {label}", "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#2E3B40"},
                "bar": {"color": color},
                "bgcolor": "white",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "#F1F5F4"},
                    {"range": [50, 100], "color": "#E4F4F0"},
                ],
            },
        )
    )
    return _base_layout(fig, height=260)


def feature_importance_bar(df: pd.DataFrame, top_n: int = 12) -> go.Figure:
    plot_df = df.head(top_n).sort_values("importance")
    fig = px.bar(
        plot_df,
        x="importance",
        y="label",
        orientation="h",
        color="importance",
        color_continuous_scale=["#BFEAE2", MINT, "#2E6E68"],
    )
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Importance")
    return _base_layout(fig, height=420)


def confusion_matrix_heatmap(matrix, labels=("At Risk", "Healthy")) -> go.Figure:
    fig = px.imshow(
        matrix,
        x=list(labels),
        y=list(labels),
        text_auto=True,
        color_continuous_scale=["#F3FBF9", MINT, "#1F4E48"],
        labels=dict(x="Predicted", y="Actual", color="Count"),
    )
    fig.update_layout(coloraxis_showscale=False)
    return _base_layout(fig, height=380)


def model_comparison_bar(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df,
        x="Model",
        y="Accuracy",
        color="Model",
        text_auto=".2%",
    )
    fig.update_layout(showlegend=False, yaxis_tickformat=".0%", xaxis_title="")
    return _base_layout(fig, height=380)


def numeric_distribution_hist(df: pd.DataFrame, column: str, label: str) -> go.Figure:
    fig = px.histogram(
        df,
        x=column,
        color="risk_level",
        color_discrete_map={"Healthy": MINT, "At Risk": CORAL},
        barmode="overlay",
        opacity=0.75,
        nbins=30,
    )
    fig.update_layout(xaxis_title=label, yaxis_title="Count")
    return _base_layout(fig, height=380)


def category_by_risk_bar(df: pd.DataFrame, column: str, label: str) -> go.Figure:
    counts = df.groupby([column, "risk_level"]).size().reset_index(name="count")
    fig = px.bar(
        counts,
        x=column,
        y="count",
        color="risk_level",
        barmode="group",
        color_discrete_map={"Healthy": MINT, "At Risk": CORAL},
    )
    fig.update_layout(xaxis_title=label, yaxis_title="Count")
    return _base_layout(fig, height=380)


def growth_bullet_chart(item: dict) -> go.Figure:
    """
    Compact horizontal bullet gauge: shaded band = typical (10th-90th
    percentile) range for babies of a similar age in the dataset, bar =
    this baby's value, thin line = the dataset median.
    """
    color = MINT if item["status"] == "normal" else CORAL
    lo_axis = min(item["p10"] * 0.75, item["value"] * 0.9)
    hi_axis = max(item["p90"] * 1.25, item["value"] * 1.1)

    fig = go.Figure(
        go.Indicator(
            mode="number+gauge",
            value=item["value"],
            number={"suffix": f" {item['unit']}", "font": {"size": 20}},
            domain={"x": [0.32, 1], "y": [0, 1]},
            title={"text": item["label"], "font": {"size": 13}},
            gauge={
                "shape": "bullet",
                "axis": {"range": [lo_axis, hi_axis]},
                "bar": {"color": color, "thickness": 0.55},
                "bgcolor": "white",
                "steps": [
                    {"range": [lo_axis, item["p10"]], "color": "#FFE3D6"},
                    {"range": [item["p10"], item["p90"]], "color": "#E4F4F0"},
                    {"range": [item["p90"], hi_axis], "color": "#FFE3D6"},
                ],
                "threshold": {
                    "line": {"color": "#2E3B40", "width": 2},
                    "thickness": 0.8,
                    "value": item["p50"],
                },
            },
        )
    )
    fig.update_layout(
        height=110,
        margin=dict(l=10, r=10, t=28, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Nunito, sans-serif", color="#2E3B40"),
    )
    return fig


def risk_factor_bar(factors: list) -> go.Figure:
    df = pd.DataFrame(factors).sort_values("score")
    fig = px.bar(
        df,
        x="score",
        y="label",
        orientation="h",
        color="score",
        color_continuous_scale=["#FFD5C7", CORAL, "#B8302F"],
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_title="Relative contribution", yaxis_title="")
    return _base_layout(fig, height=max(220, 60 * len(df)))


def correlation_heatmap(df: pd.DataFrame, numeric_cols) -> go.Figure:
    corr = df[numeric_cols].corr()
    fig = px.imshow(
        corr,
        color_continuous_scale=["#FF6B6B", "#FDF6F0", "#58C9A8"],
        zmin=-1,
        zmax=1,
        aspect="auto",
    )
    return _base_layout(fig, height=520)
