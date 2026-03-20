from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Load the data we processed in Task 2
df = pd.read_csv("pink_morsel_sales.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")

app.layout = html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
    html.H1(
        children='Pink Morsel Sales Visualizer',
        id='header',
        style={'textAlign': 'center', 'color': '#2c3e50', 'fontFamily': 'Arial'}
    ),

    # This picker allows the user to see sales by region
    html.Div(style={'textAlign': 'center', 'marginBottom': '30px'}, children=[
        dcc.RadioItems(
            id='region-picker',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            inline=True
        ),
    ]),

    dcc.Graph(id='sales-line-chart')
])

@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-picker', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    fig = px.line(filtered_df, x="date", y="sales", title=f"Sales Trend ({selected_region.capitalize()})")
    
    # Add a vertical line for the price increase date (Jan 15, 2021)
    fig.add_shape(
        type="line",
        x0="2021-01-15", x1="2021-01-15",
        y0=0, y1=1, yref="paper",
        line=dict(color="Red", dash="dash")
    )
    fig.add_annotation(
        x="2021-01-15", y=1, yref="paper",
        text="Price Increase", showarrow=False, xanchor="left"
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)