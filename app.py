import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

########### Define your variables ######

tabtitle = 'Old McDonald'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/samanthabretouswork/306-agriculture-exports-dropdown'
# here's the list of possible columns to choose from.
# list_of_columns =['total exports', 'beef', 'pork', 'poultry',
    #    'dairy', 'fruits fresh', 'fruits proc', 'total fruits', 'veggies fresh',
    #    'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton']


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/social-media-influencers-youtube-june-2022.csv')
list_of_columns = df['Category'].unique()
# create column based on range
df['Subscribers count Range'] = df['Subscribers count'].values
df['Views avg. Range'] = df['Views avg.'].values

# df['Views avg.'].sort
for ind in df.index:
    df['Subscribers count Range'][ind] = round(float(df['Subscribers count'][ind][:-1]), -1)
    string = df['Views avg. Range'][ind]
    last_char = string[len(string)-1]
    if last_char == "K":
        df['Views avg. Range'][ind] = float(string[:-1]) * 1000
    elif last_char == "M":
        df['Views avg. Range'][ind] = float(string[:-1]) * 1000000
    else:
        df['Views avg. Range'][ind] = 0

    
df.sort_values(by=['Views avg. Range'], inplace=True)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('Social Media Influencers on YouTube june-2022'),
    html.Div([
        html.Div([
                html.H6('Select a variable for analysis:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=list_of_columns,
                    value=list_of_columns[0]
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'Exports of {varname} in 2011'
    mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
    mycolorbartitle = "YouTubers subscribers by Category"

    # print(df.groupby(['Category','Name']).sum())
    filterData = df[df['Category'] == varname]


    fig = px.bar(filterData, y="Views avg.", x='Subscribers count Range', barmode="group")

    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
