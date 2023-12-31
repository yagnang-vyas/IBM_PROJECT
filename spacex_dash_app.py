# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"C:\Users\toner\Documents\LSN\tech.dir\Data_Science\IBM_Capstone\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                             options= [
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                             ],
                                             placeholder='Select a Launch Site',
                                             value='ALL',
                                             searchable=True),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def pie_chart(launch_site):
    if launch_site == 'ALL':
        site_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        site_df.columns = ['Launch Site', 'Successful Launches']
        fig = px.pie(site_df, values='Successful Launches', names='Launch Site', title='Total Successful Launches by Site')
        return fig
    else:
        launch_df = spacex_df.loc[spacex_df['Launch Site'] == launch_site]['class'].value_counts().reset_index()
        launch_df.columns = ['Outcome', 'Count']
        fig = px.pie(launch_df, values='Count', names=['Success', 'Failure'], color=['Success', 'Failure'],color_discrete_map={'Success': 'green', 'Failure':'red'},title=f'Launch Outcomes At {launch_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='payload-slider', component_property='value'),
     Input(component_id='site-dropdown', component_property='value')])
def payload_scatter(payload_range, launch_site):
    # Set range variables
    sample_max = payload_range[1]
    sample_min = payload_range[0]
    if launch_site == 'ALL':
        payload_df = spacex_df.loc[(spacex_df['Payload Mass (kg)'] > sample_min) & 
                                   (spacex_df['Payload Mass (kg)'] < sample_max)]
        fig = px.scatter(payload_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation Between Payload and Outcome for All Sites')
        return fig
    else:
        payload_df = spacex_df.loc[(spacex_df['Payload Mass (kg)'] > sample_min) & 
                                   (spacex_df['Payload Mass (kg)'] < sample_max) &
                                   (spacex_df['Launch Site'] == launch_site)]
        fig = px.scatter(payload_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Correlation Between Payload and Outcome At {launch_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()