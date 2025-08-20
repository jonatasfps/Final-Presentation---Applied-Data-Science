import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Create app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Read the wildfire data into pandas dataframe
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

# Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Layout Section of Dash
app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),

    html.Div([
        html.Div([
            html.H2('Select Region:', style={'margin-right': '2em'}),
            dcc.RadioItems(
                options=[
                    {"label": "New South Wales", "value": "NSW"},
                    {"label": "Northern Territory", "value": "NT"},
                    {"label": "Queensland", "value": "QL"},
                    {"label": "South Australia", "value": "SA"},
                    {"label": "Tasmania", "value": "TA"},
                    {"label": "Victoria", "value": "VI"},
                    {"label": "Western Australia", "value": "WA"}
                ],
                value="NSW",
                id='region',
                inline=True
            )
        ]),

        html.Div([
            html.H2('Select Year:', style={'margin-right': '2em'}),
            dcc.Dropdown(
                options=[{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                value=2005,
                id='year'
            )
        ]),

        html.Div([
            html.Div(id='plot1', style={'width': '50%'}),
            html.Div(id='plot2', style={'width': '50%'})
        ], style={'display': 'flex'})
    ])
])

# Callback
@app.callback(
    [Output('plot1', 'children'),
     Output('plot2', 'children')],
    [Input('region', 'value'),
     Input('year', 'value')]
)
def reg_year_display(input_region, input_year):
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    # Plot 1 - Monthly Average Estimated Fire Area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month',
                  title=f"{input_region} : Monthly Average Estimated Fire Area in {input_year}")

    # Plot 2 - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count',
                  title=f"{input_region} : Average Count of Pixels for Presumed Vegetation Fires in {input_year}")

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

if __name__ == '__main__':
    app.run(debug=True, port=8054)
    
