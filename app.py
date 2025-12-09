from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


DATA_FILE = Path(__file__).parent / "pink_morsels_sales.csv"
PRICE_CHANGE_DATE = pd.Timestamp("2021-01-15")


def load_data() -> pd.DataFrame:
    """Load the processed sales data and ensure correct types."""

    df = pd.read_csv(DATA_FILE)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Sales"] = pd.to_numeric(df["Sales"])
    return df


df_sales = load_data()
REGIONS = sorted(df_sales["Region"].unique())


def make_figure(selected_regions: list[str] | None) -> px.line:
    """Create a line chart of daily sales, filtered by region."""

    if selected_regions:
        data = df_sales[df_sales["Region"].isin(selected_regions)]
    else:
        data = df_sales

    daily_sales = (
        data.groupby("Date", as_index=False)["Sales"].sum().sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        labels={"Date": "Date", "Sales": "Sales ($)"},
        title="Daily Pink Morsel Sales",
    )

    # Manual line + annotation avoids plotly Timestamp sum issue in add_vline
    fig.add_shape(
        type="line",
        x0=PRICE_CHANGE_DATE,
        x1=PRICE_CHANGE_DATE,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="#ff6b6b", dash="dash"),
    )
    fig.add_annotation(
        x=PRICE_CHANGE_DATE,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase (2021-01-15)",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        bgcolor="rgba(255,255,255,0.6)",
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    return fig


app = Dash(__name__)
app.title = "Pink Morsels Sales"

app.layout = html.Div(
    className="container",
    children=[
        html.H1("Pink Morsels Sales Visualiser"),
        html.P(
            "Track daily sales and compare performance before and after the 2021-01-15 price increase."
        ),
        html.Label("Filter by region"),
        dcc.Dropdown(
            id="region-dropdown",
            options=[{"label": region.title(), "value": region} for region in REGIONS],
            value=REGIONS,
            multi=True,
            placeholder="Select regions",
        ),
        dcc.Graph(id="sales-graph", figure=make_figure(REGIONS)),
    ],
    style={"maxWidth": "900px", "margin": "0 auto", "padding": "24px"},
)


@app.callback(Output("sales-graph", "figure"), Input("region-dropdown", "value"))
def update_graph(selected_regions: list[str] | None):
    return make_figure(selected_regions)


server = app.server


if __name__ == "__main__":
    app.run(debug=True)
