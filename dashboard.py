import dash

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import dcc, html
from dash.dependencies import Output, Input, State

df = pd.read_csv('./required_skills.csv') 

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.H1("Job skill analyzer")
    ]),

    html.Div([
      dcc.Dropdown(
        id="degree_dropdown",
        options= [
            {"label":"Master","value":"Master"},
            {"label":"Bachelor","value":"Bachelor"},
            {"label":"All degrees","value":"both"}
        ],
        value="Bachelor",
        clearable=False
      ),  
    ]),

    html.Div([
        dcc.Graph(
            id="degree_graph",
        ),
    ]),
])

@app.callback(
    Output(component_id='degree_graph', component_property='figure'),
    [Input(component_id='degree_dropdown', component_property='value')]
)
def make_degree_graph(degree_dropdown_value):
    dff = df

    if degree_dropdown_value == "both":
        return px.bar(dff, x="Title", y=["Bachelor","Master"], barmode="group")

    fig = px.bar(dff, x="Title", y=degree_dropdown_value)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)