import dash

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from dash import dcc, html
from dash.dependencies import Output, Input

df = pd.read_csv('./required_skills.csv') 


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
            html.Div([
                html.H1("Job skill analyzer", style={'textAlign':"center"})
            ]),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                            dbc.Col([
                                html.Label(html.B("Degrees")),
                                dcc.Dropdown(
                                    id="degree_dropdown",
                                    options= [
                                        {"label":"Master","value":"Master"},
                                        {"label":"Bachelor","value":"Bachelor"},
                                        {"label":"All degrees","value":"both"}
                                    ],
                                    value="both",
                                    clearable=False,
                                ),
                            ], width={"size":6, "offset":3}),
                        
                    ]),
                        dcc.Graph(
                                id="degree_graph",
                            ),
           
                ]),
            ], width=6),
        
            dbc.Col([
                html.Div([
                        dbc.Col([
                            html.Label(html.B("Programming languages")),
                            dcc.Checklist(
                                id="programming_checklist",
                                options= ["SQL","Python","R","Java"],
                                value=["SQL","Python","R","Java"],
                                inline=True
                            ),
                        ], width={"size":6, "offset":4}),
                            dcc.Graph(
                                id="programming_graph"
                            ),
        
            
                ]),
            ], width=6),
        ]),

        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Col([
                        html.Label(html.B("Visualisation techniques")),
                        dcc.Checklist(
                            id="visualisation_checklist",
                            options= ["Power Bi","Tableau","Dash"],
                            value=["Power Bi","Tableau","Dash"],
                            inline=True
                        ),
                    ], width={"size":6, "offset":4}),
                    
                    dcc.Graph(
                        id="visualisation_graph"
                    ),
                ]),
            ], width=6),

            dbc.Col([
                html.Div([
                    dbc.Col([
                        html.Label(html.B("Cloud")),
                        dcc.Checklist(
                            id="cloud_checklist",
                            options= ["Amazon","Google","Azure"],
                            value=["Amazon","Google","Azure"],
                            inline=True
                        ),
                    ], width={"size":6, "offset":4}),
                    
                    dcc.Graph(
                        id="cloud_graph"
                    ),
                ]),
            ], width=6),
        ])
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