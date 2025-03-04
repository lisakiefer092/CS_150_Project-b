from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from numpy.ma.core import minimum

df2 = pd.read_csv("Share-of-firms-invest.-in-measures-to-improve-energy-2018-21.csv")
df= pd.read_csv("Adjusted_savings_energy_depletion_%ofGNI.csv", on_bad_lines='skip')

df1= df[["Country Name", "Country Code","2018","2019","2020","2021"]]

europe_countries = {'Austria','Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden'}
df1 = df1[df1['Country Name'].isin(europe_countries)]

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label(
                        "Energy Depletion in Europe",
                        className="fw-bold",
                        style={"textDecoration": "underline", "fontSize": 20, "align": "center"},
                    ),
                    html.H2(

                    ),
                    dcc.Graph(id="my-choropleth", figure= {}),
                ],
                width=12,
            )
        ),
        dbc.Row([
            dbc.Col(
                [
                    dbc.Label(
                        "Select the year:",
                        className="fw-bold",
                        style={"textDecoration": "underline", "fontSize": 20},
                    ),
                    dcc.Slider(
                        id="year",
                        min=2018,
                        max=2021,
                        step=1,
                        value=2018,
                        marks={
                            2018: "'2018",
                            2019: "'19",
                            2020: "'20",
                            2021: "2021",
                        },

                    ),
                ],
                width=8
            ),
            dbc.Col(
                [
                    dbc.Button("Download Data as CSV", id="btn-download-data"),
                    dcc.Download(id="my-download-data"),
                ],
                width = 3
            ),
        ]),## this was supposed to be the code for my secondary graph that would show up when you click on a specific country, showing the share of firms investing in measures to improve energy efficiency
#         dbc.Row(
#             dbc.Col(
#                 [
#                     dbc.Label(
#                         "Share of firms investing in measures to improve energy efficiency ",
#                         className="fw-bold",
#                         style={"textDecoration": "underline", "fontSize": 10, "align": "center"},
#                     ),
#                     dcc.Graph(id="new-graph", figure={}),
#                 ],
#                 width=12,
#             )
#         ),
    ]
)


@app.callback(Output("my-choropleth", "figure"),Input("year", "value"))
def update_figure(year):
    fig = px.choropleth(
        data_frame=df1,
        locations="Country Code",
        color= str(year),
        scope="europe",
        color_continuous_scale=px.colors.sequential.Greens,
        hover_data={"Country Name": True},

    )
    fig.update_layout(
        geo={"projection": {"type": "natural earth"}},
        margin=dict(l=15, r=15, t=15, b=15),
    )
    return fig
## this was the callback for the secondary graph, it gave me an error saying that the input graph my-choropleth does not have the property "clickData" which I was not able to solve
# @app.callback(Output("new-graph", "figure"), [Input("my-choropleth", "clickData")], prevent_initial_call=True)
# def update_figure(click_data):
#     if not click_data:
#         return px.bar(title="Click on a state to see the share of firms  investing to improve energy efficiency")
#     country_name = click_data["points"][0]["location"]
#     country_data = df[df["Country name"] == country_name]
#
#     fig = px.bar(data_frame=df2, x="Year", y=str(country_data), title="Share of firms investing in energy efficiency in %")
#     return fig

@app.callback(Output("my-download-data", "data"), Input("btn-download-data", "n_clicks"), prevent_initial_call=True)
def download_data(n_clicks):
    return dcc.send_data_frame(df.to_csv, "Adjusted_savings_energy_depletion_%ofGNI.csv")

if __name__ == "__main__":
    app.run_server(debug=True)

