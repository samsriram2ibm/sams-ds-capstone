# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'Cape Canaveral Launch LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'Cape Canaveral Space Launch SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'Kennedy Space Center Launch Complex 39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'Vandenberg Space Launch Complex 4', 'value': 'VAFB SLC-4E'},
                                                    ],
                                                    value='ALL',
                                                    placeholder="Select a Launch Site",
                                                    searchable=True
                                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                                value=[min_payload, max_payload]
                                                ),
                                #html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                #html.Br()
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(selected_site):
    filtered_df = spacex_df
    if selected_site == 'ALL':
        # Select data
        pie_data =  filtered_df[filtered_df['class']==1]
        fig = px.pie(pie_data, values='class', 
        names='Launch Site', 
        title='Landing Success Counts by Launch Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        pie_data = filtered_df[filtered_df['Launch Site']==selected_site].groupby('class').count().reset_index()        
        fig = px.pie(pie_data, values='Unnamed: 0', 
        names='class', 
        title='Landing Success Counts for Launch Site {}'.format(selected_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(selected_site, payload_range):
    print('Params: {} {}'.format(selected_site, payload_range))
    low, high = payload_range
    slide=(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    scatter_data=spacex_df[slide]
    if selected_site == 'ALL':
        # Select data
        #scatter_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= int(payload_range[0])) &	
        #                        (spacex_df['Payload Mass (kg)'] <= int(payload_range[1]))	
        #                      ]	
        fig = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for ALL Sites between {:8,d}kg and {:8,d}kg'.format(int(low),int(high)))
        return fig
    else:
        # return the outcomes piechart for a selected site
        scatter_data = scatter_data[scatter_data['Launch Site'] == selected_site]       
        fig = px.scatter(scatter_data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
        title='Correlation between Payload and Success for Launch Site {} - payload between {:8,d}kg and {:8,d}'.format(selected_site,int(low),int(high)))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
