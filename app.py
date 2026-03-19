from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# Load and sort the data
df = pd.read_csv("pink_morsel_sales.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# Define the layout
app.layout = html.Div(className="dash-container", children=[
    html.Header(
        html.H1("Pink Morsel Sales Visualizer", id="header"),
    ),
    
    html.Div([
        html.Label("Select Region:"),
        dcc.RadioItems(
            id="region-picker",
            options=[
                {"label": "North", "value": "north"},
                {"label": "South", "value": "south"},
                {"label": "East", "value": "east"},
                {"label": "West", "value": "west"},
                {"label": "All", "value": "all"}
            ],
            value="all",
            inline=True
        )
    ], className="control-section"),

    dcc.Graph(id="sales-line-chart")
])

# Define the callback to update the graph
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-picker", "value")
)
def update_graph(region):
    if region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == region]

    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=f"Sales for {region.capitalize()} Region" if region != "all" else "Total Sales (All Regions)",
        labels={"sales": "Total Sales ($)", "date": "Date"},
        template="plotly_white"
    )
    
    fig.update_layout(
        font_family="Inter, sans-serif",
        title_font_size=24,
        xaxis_title="Date",
        yaxis_title="Total Sales",
        hovermode="x unified"
    )
    
    fig.update_traces(line_color="#e74c3c", line_width=3)
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)
