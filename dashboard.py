import dash

import pandas as pd
import plotly.express as px

from dash import dcc, html
from dash.dependencies import Output, Input, State

df = pd.read_csv('./required_skills.csv') 

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Div([
        html.H1("Job skill analyzer")
    ], className="banner"),

    html.Div([

        html.Div([
        
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
        )
        ], className="drop"),
        dcc.Graph(
                id="degree_graph",
            ),
        ], className="six columns"),

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
        ], className="six columns"),

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
        ], className="five columns"),

         html.Div([
            html.Label("Cloud"),
            dcc.Checklist(
                id="cloud_checklist",
                options= ["Amazon","Google","Azure"],
                value=["Amazon","Google","Azure"],
                inline=True
            ),
            dcc.Graph(
                id="cloud_graph"
            ),
        ], className="five columns"),

    ], className="container"),
])

@app.callback(
    Output(component_id="cloud_graph",component_property="figure"),
    [Input(component_id="cloud_checklist",component_property="value")]
)
def cloud_checklist(checklist_values):
    dff = df

    dff["Google"] = dff["Google"] + dff["GCP"]
    dff["Amazon"] = dff["Amazon"] + dff["AWS"]

    return px.bar(dff, x="Title", y=checklist_values, barmode="group")

@app.callback(
    Output(component_id="visualisation_graph",component_property="figure"),
    [Input(component_id="visualisation_checklist",component_property="value")]
)
def visualisation_checklist(checklist_values):

    if "Power Bi" in checklist_values:
        checklist_values = [item.replace("Power Bi", "Power") for item in checklist_values]

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