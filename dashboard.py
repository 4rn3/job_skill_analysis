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
    html.Label("Degrees"),
      dcc.Dropdown(
        id="degree_dropdown",
        options= [
            {"label":"Master","value":"Master"},
            {"label":"Bachelor","value":"Bachelor"},
            {"label":"All degrees","value":"both"}
        ],
        value="both",
        clearable=False
      ),
      dcc.Graph(
            id="degree_graph",
        ),
    ]),

    html.Div([
        html.Label("Programming languages"),
        dcc.Checklist(
            id="programming_checklist",
            options= ["SQL","Python","R","Java"],
            value=["SQL","Python","R","Java"],
            inline=True
        ),
        dcc.Graph(
            id="programming_graph"
        ),
    ]),

    html.Div([
        html.Label("Visualisation techniques"),
        dcc.Checklist(
            id="visualisation_checklist",
            options= ["Power Bi","Tableau","Dash"],
            value=["Power Bi","Tableau","Dash"],
            inline=True
        ),
        dcc.Graph(
            id="visualisation_graph"
        ),
    ]),
])

@app.callback(
    Output(component_id="visualisation_graph",component_property="figure"),
    [Input(component_id="visualisation_checklist",component_property="value")]
)
def visualisation_checklist(checklist_values):

    if "Power Bi" in checklist_values:
        checklist_values = checklist_values.replace("Power Bi", "Power")

    dff = df
    return px.bar(dff, x="Title", y=checklist_values, barmode="group")

@app.callback(
    Output(component_id="programming_graph",component_property="figure"),
    [Input(component_id="programming_checklist",component_property="value")]
)
def programming_checklist(checklist_values):
    dff = df
    return px.bar(dff, x="Title", y=checklist_values, barmode="group")

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