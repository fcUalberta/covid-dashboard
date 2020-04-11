# Importing libraries
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime as dt
from datetime import date
import numpy as np
import datetime

# import plotly.plotly as py
from plotly.graph_objs import *
from dateutil.relativedelta import relativedelta

# Importing dependencies
from data_ingest import data_ingest
from forecasting import forecast

# df-> Countries and provinces with All days
# countryDays_df -> Country Df with all days
# latest_df -> Countries and provinces with latest date
# country_df -> Countries with latest date
df,countryDays_df,latest_df, country_df,canada_df = data_ingest()
#added for tab-1

# alldf = pd.read_csv("countryDays_df.csv",sep='\t')
new_df = country_df[['Country/Region','Confirmed','Death','Recovered']]
# df = pd.read_csv("covid.csv",sep='\t')
sumdf = pd.read_csv("sumdf.csv",sep='\t')

countries = country_df["Country/Region"]

newdf = sumdf.loc[sumdf['Date'] == '2020-04-08']

confirmedVal = newdf["Confirmed"].astype(int).apply(str)
ActiveVal = newdf["Active"].astype(int).apply(str)
DeathVal = newdf["Death"].astype(int).apply(str)
RecoveredVal = newdf["Recovered"].astype(int).apply(str)

template = 'plotly'
epoch = datetime.datetime.utcfromtimestamp(0)



def unix_time_millis(dt):
    return (dt - epoch).total_seconds() #* 1000.0

def get_marks_from_start_end(start, end):
    ''' Returns dict with one item per month
    {1440080188.1900003: '2015-08',
    '''
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += relativedelta(months=1)
    return {unix_time_millis(m):(str(m.strftime('"%m/%d/%Y'))) for m in result}

def create_divs(case):
    return_divs = []
    for country in countries:
        newdf = country_df.loc[country_df['Country/Region'] == country]
        return_divs.append(html.Div(html.P(country+" "+newdf[case].astype(int).apply(str), style = {'font-size': '10px'})))
    return return_divs


# Initializing Variables

target_options = [{'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Active', 'value': 'Active'},
                        {'label': 'Death', 'value': 'Death'},
                        {'label': 'Recovered', 'value': 'Recovered'}]

target_options1 = [{'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Death', 'value': 'Death'},
                        {'label': 'Recovered', 'value': 'Recovered'}]
target_options2 = [{'label': i, 'value': i} for i in [
                    'Confirmed','Active','Death','Recovered',
                    'New Confirmed', 'New Death', 'New Recovered']]
target_options3 = [{'label': i, 'value': i} for i in [
                    'New Confirmed', 'New Death', 'New Recovered']]
target_options4 = [{'label': i, 'value': i} for i in [
                    'Confirmed','Active','Death','Recovered','Fatality Rate',
                    'New Confirmed', 'New Death', 'New Recovered']]

top_options =  [{'label': 'Top 20', 'value': 'Top 20'},
                        {'label': 'Top 30', 'value': 'Top 30'},
                        {'label': 'Top 40', 'value': 'Top 40'}]

countries_options = [{'label': 'Top 10', 'value': 'Top 10'},
                        {'label': 'G7', 'value': 'G7'},
                        {'label': 'BRICS', 'value': 'BRICS'}]
scale_options = [{'label': i, 'value': i} for i in ['Linear', 'Log']]
moving_average_options = [{'label': i, 'value': i} for i in ['Simple',
                        'Cumulative', 'Exponential']]

country_options = [{'label': 'Global', 'value': 'Global'}]
option_df = latest_df.loc[latest_df['Province/State']!=0]
cols = list(option_df['Country/Region'].unique())
for i in range(len(cols)):
    country_options.append({'label':cols[i],'value':cols[i]})

country_options1 = [{'label': 'Global', 'value': 'Global'}]
# option_df = latest_df.loc[latest_df['Province/State']!=0]
cols = list(country_df['Country/Region'])
for i in range(len(cols)):
    country_options1.append({'label':cols[i],'value':cols[i]})

""" ###################################################
Custom Styling
###################################################"""

colors = {
    'page_color': '#000000',
    'background': '#75D5FF',
    'bg': '#DCF3FF',
    'text': '#000000',
    'text1':'#000000',
    'graph_bg_color':'#FFFFFF',
    'graph_text':'#000000',
    'heading':'#C01414',
    'Confirmed': '#192AB4',
    'Active': '#ff6f00',
    'Death': '#da5657',
    'Recovered': '#45df7e',
    'graph_title1':'#C01414',
    'titlebox_border':'thin lightgrey solid',
    'titlebox_background':'rgb(250, 250, 250)',
    # 'analytics_tab_color':''
}

title_box = {
    'borderBottom': colors['titlebox_border'],
    'backgroundColor': colors['titlebox_background'],
    'padding': '10px 5px'}

heading2 = {
    'text-align':'center',
    'color': colors["heading"],
    }
small_italics = {
'font-style': 'italic',
'text-align':'center',
'font-size': '18px'
}

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'color':'#000000'
}
page_style = {
'overflowY': 'scroll',
'height': 200
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#C01414',
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold'
}
inner_tab_style = {
    'text-align':'center',
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#C01414',
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold'
}
graph_style = {
# 'borderTop': '1px solid #d6d6d6',
# 'borderBottom': '1px solid #d6d6d6',
'padding': '2px',
# 'display': 'inline-block',
'box-shadow': '3px 3px 3px 3px lightgrey',
'padding-top':'2px',
'float':'center',
'backgroundColor':colors['graph_bg_color'],
'plot_bgcolor': colors['graph_bg_color']

}

it_content = {
'text-align':'center',
'font-family':'sans-serif',
'font-style': 'italic'
}

content = {
'text-align':'center',
'font-family':'sans-serif',
'font-style': 'bold'
}
chart_box = {
  'box-shadow': '3px 3px 3px 3px lightgrey',
  'padding-top':'2px',"width": "900px",
  "margin": "0 auto",
  'backgroundColor':colors['background'],
  'plot_bgcolor': colors['background']
}
chart_box1 = {
  'box-shadow': '3px 3px 3px 3px lightgrey',
  'padding-top':'2px',
  'padding-left':'10px',
  "margin": "5px",
  'backgroundColor':colors['graph_bg_color'],
  'plot_bgcolor': colors['graph_bg_color']
}
overlay = {'opacity':'0.8',
'background-color':'#000000',
'position':'fixed',
'width':'100%',
'height':'100%',
'top':'0px',
'left':'0px',
'z-index':'1000',
'overflowY':'scroll',
'height':500
}
page = {
'overflowY':'scroll',
'height':5000

}

# Mapbox
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
MAPBOX_STYLE = "mapbox://styles/plotlymapbox/cjyivwt3i014a1dpejm5r7dwr"

# Calling external stylesheet
# external_stylesheets=['https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-web-trader/assets/style.css']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Initializing Dash app
app = dash.Dash(__name__)
server = app.server


""" ###################################################
App Layout Creation
###################################################"""
# Creating the app layout
app.layout = html.Div(children=[

    html.H2("COVID-19 Dashboard",
    style={'text-align':'center','font-family':'sans-serif','color': colors['text']}),

    # Parent of all tabs
    dcc.Tabs(id="tabs-styled-with-inline",
    value='tab-1',
    children=[
        # Tab 1
        dcc.Tab(label='Global Trends',
        value='tab-1',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div(
                children=[
                        # Left-Most-Panel
                                    html.Div(
                                        className="two columns div-left-panel",
                                        children = [
                                                    #Global-Cases-div
                                                    html.Div(
                                                        children = [
                                                            #Global-Confirmed-Cases
                                                                html.Div(
                                                                    children = [
                                                                                    html.Div([html.P('Confirmed Cases')],
                                                                                    style = {'padding-top': "13px", 'color': colors["Confirmed"],
                                                                                    'font-weight': 'bold'},
                                                                                    className = "GlobalName"),
                                                                                    html.Div([html.P(''+confirmedVal)], style = {'color': colors["Confirmed"], 'font-weight': 'bold'},className = "GlobalValue")
                                                                                ],
                                                                     className="first",
                                                                ),
                                                            #Global-Active-Cases
                                                                html.Div(
                                                                    children = [
                                                                                    html.Div([html.P('Active Cases')],style = {'color': colors['Active'], 'font-weight': 'bold'}, className = "GlobalName"),
                                                                                    html.Div([html.P(''+ActiveVal)], style = {'color': colors['Active'], 'font-weight': 'bold'}, className = "GlobalValue"),
                                                                                ],
                                                                    className="first",
                                                                ),
                                                            #Global-Death
                                                                html.Div(
                                                                    children = [
                                                                                    html.Div([html.P('Deaths')], style = {"color": colors['Death'], 'font-weight': 'bold'}, className = "GlobalName"),
                                                                                    html.Div([html.P(''+DeathVal)], style = {"color": colors['Death'], 'font-weight': 'bold'}, className = "GlobalValue"),
                                                                                ],
                                                                    className="first",
                                                                ),
                                                            #Global-Recovered
                                                                html.Div(
                                                                    children = [
                                                                                    html.Div([html.P('Recovered')], style = {'color': colors['Recovered'], 'font-weight': 'bold'}, className = "GlobalName"),
                                                                                    html.Div([html.P(''+RecoveredVal)], style = {'color': colors['Recovered'], 'font-weight': 'bold'}, className = "GlobalValue"),
                                                                                ],
                                                                    className="first",
                                                                ),
                                                                ],style={"display": "flex", "flex-direction": "column"}
                                                            ),# End of Global-Cases div

                                                #Div-for-spacing
                                                html.Div(style = {"padding":20}),

                                                #Top-5-Countries-Div
                                                html.Div(
                                                    children = [
                                                        #Div-for-title
                                                        html.Div([html.P('Top 5 Countries',style= inner_tab_style)]),
                                                        #US-Div
                                                        html.Div(
                                                            children = [
                                                                        html.Div([html.P('US', style = {'font-size': '12px'})],className = "top-count-name"),
                                                                        html.Div(id = "us"),
                                                                    ],className="topcount",
                                                                ),
                                                        #Spain-Div
                                                        html.Div(
                                                            children = [
                                                                        html.Div([html.P('Spain', style = {'font-size': '12px'})], className = "top-count-name"),
                                                                        html.Div(id = "spain"),
                                                                    ],className="topcount",
                                                                ),
                                                        #Italy-Div
                                                        html.Div(
                                                            children = [
                                                                        html.Div([html.P('Italy', style = {'font-size': '12px'})], className = "top-count-name"),
                                                                        html.Div(id = "italy"),
                                                                    ],className="topcount",
                                                                ),
                                                        #Germany-Div
                                                        html.Div(
                                                            children = [
                                                                        html.Div([html.P('Germany', style = {'font-size': '12px'})], className = "top-count-name"),
                                                                        html.Div(id = "germany"),
                                                                    ],className="topcount",
                                                                ),
                                                        #France-Div
                                                        html.Div(
                                                            children = [
                                                                        html.Div([html.P('France', style = {'font-size': '12px'})], className = "top-count-name" ),
                                                                        html.Div(id = "france"),
                                                                    ],className="topcount",
                                                                ),
                                                        #China-Div
                                                        html.Div(
                                                        children = [
                                                                        html.Div([html.P('China', style = {'font-size': '12px'})], className = "top-count-name"),
                                                                        html.Div(id = "china"),
                                                                    ],className="topcount",
                                                                ),
                                                        #Iran-Div
                                                        html.Div(
                                                            children = [
                                                                        html.Div([html.P('Iran', style = {'font-size': '12px'})], className = "top-count-name"),
                                                                        html.Div(id = "iran"),
                                                                    ],className="last",
                                                                ),
                                                    ])#End-of-Top-5-Countries-Div
                                            ]),#End-of-Left-Most-Div

                                            # Maps-Div
                                            html.Div(
                                                className="seven columns",
                                                children = [
                                                    #Drop-Down-1-Div
                                                    html.Div([
                                                                html.P('Select from the drop down'
                                                                ,style={'text-align':'center','font-family':'sans-serif', 'color': colors['text']}),
                                                                dcc.Dropdown(id='option',
                                                                             options=target_options,
                                                                             value ='Confirmed',
                                                                             style={'width':'55%', 'margin-left': '120px', 'text-align':'center', 'color':colors["text1"]}),
                                                                html.Div(style = {"padding":3}),# For vertical space
                                                            ],className = "drop-down"),
                                                    #Chlorepath-Div
                                                    html.Div([
                                                                dcc.Graph(id='chlorepath',
                                                                          style = {"height":"70vh"}, hoverData={'points': [{'customdata': ''}]}),
                                                              ], style = graph_style,className = "twelve columns"),
                                                    #Drop-Down-2-Div
                                                    html.Div([
                                                                html.P('Select from the drop down'
                                                                        ,style={'text-align':'center','font-family':'sans-serif', 'color': colors['text']}),
                                                                dcc.Dropdown(id='optionbubble',
                                                                             options=target_options,
                                                                             value ='Confirmed',
                                                                             style={'width':'55%', 'margin-left': '120px', 'text-align':'center', 'color':colors["text1"]}),
                                                                html.Div(style = {"padding":3}),# For vertical space
                                                            ],className = "drop-down"),
                                                    #Vertical-Space
                                                    html.Div(style = {"padding":10}),# For vertical space
                                                    #Bubble Map
                                                    html.Div([
                                                               dcc.Graph(id='bubblemap',
                                                                         style = {"height":"70vh"}),
                                                            ],style = graph_style, className = "twelve columns"),
                                            ]),#End-of-Map-Panel

                                            #Right-Most-Panel
                                            html.Div(
                                                className = "special columns div-right-panel",
                                                children = [

                                                    #Table-Div
                                                    html.Div(
                                                        children = [
                                                            #World/Country Name
                                                            html.Div(id = "type"),

                                                            #Column-Name-Country/Province-Confirmed-Death-Recovered
                                                            html.Div(
                                                                children = [
                                                                    #Country/Province
                                                                    html.Div([html.P('Country/Province',style={'text-align':'center','font-family':'sans-serif', 'width' : '19vh', 'font-size': '11px', 'color': '#303030'})]),
                                                                    #Confirmed
                                                                    html.Div(
                                                                              children = [html.P('Confirmed',style={'text-align':'center','font-family':'sans-serif', 'width' : '11vh', 'font-size': '11px', 'color': '#303030'}),
                                                                                          html.Div(id = "count_total_comfirmed")
                                                                              ]),
                                                                    #Death
                                                                    html.Div(
                                                                              children = [html.P('Death',style={'text-align':'center','font-family':'sans-serif', 'width' : '11vh', 'font-size': '11px', 'color': '#303030'}),
                                                                                          html.Div(id = "count_total_death")
                                                                              ]),
                                                                    #Recovered
                                                                    html.Div(
                                                                              children = [html.P('Recovered',style={'text-align':'center','font-family':'sans-serif', 'width' : '11vh', 'font-size': '11px', 'color': '#303030'}),
                                                                                          html.Div(id = "count_total_recovered")
                                                                              ])
                                                                ],style={"display": "flex", "flex-direction": "rows"}),

                                                            #Column-Values-Country/Province-Confirmed-Death-Recovered
                                                            html.Div(
                                                                children = [
                                                                    html.Div(
                                                                        children = [
                                                                                        html.Div(
                                                                                                    id = "div-1"),
                                                                                    ],style = {'width' : '19vh'},
                                                                            ),
                                                                    html.Div(
                                                                        children = [
                                                                                        html.Div(
                                                                                                    id = "div-2"),
                                                                                    ],style = {'width' : '11vh'},
                                                                            ),
                                                                    html.Div(
                                                                        children = [
                                                                                        html.Div(
                                                                                                    id = "div-3"),
                                                                                    ],style = {'width' : '11vh'},
                                                                            ),
                                                                    html.Div(
                                                                        children = [
                                                                                        html.Div(
                                                                                                    id = "div-4"),
                                                                                    ],style = {'width' : '11vh'},
                                                                            ),
                                                                ],style={"display": "flex", "flex-direction": "rows", 'height': '20vh', 'overflowY': 'scroll'})
                                                        ]),#End-of-Table-div

                                                        #Vertical-Space
                                                        html.Div(style = {"padding":7}),

                                                        #Bar-Chart
                                                        html.Div([
                                                                    dcc.Graph(id = 'onebar',style = {"height":"40vh"})
                                                        ]),

                                                        #Vertical-Space
                                                        html.Div(style = {"padding":8}),

                                                        #Line-Chart
                                                        html.Div([
                                                                    dcc.Graph(id = 'oneline',style = {"height":"40vh"})
                                                        ]),

                                                        #Vertical-Space
                                                        html.Div(style = {"padding":10}),

                                                        #Doughnut-Chart
                                                        html.Div([
                                                                    dcc.Graph(id = 'doughnut',style = {"height":"40vh"})
                                                        ]),

                                                        #Vertical-Space
                                                        html.Div(style = {"padding":45}),
                                                ],style = {"height":"100%"})#End-of-Right-Most-Panel
                                    ],className = "page", style={"display": "flex", "flex-direction": "row"}),
        ]), # End of Tab 1

        # Tab 2
        dcc.Tab(label='Canada Trends',
        value='tab-2',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div([
            html.Div(style = {"padding":10}),# For vertical space
            html.Div([
                html.H2("Corona Virus Canada Cases by Province",
                style=heading2, className = "container"),
                html.P("Hover over the provinces to view the trends in the graphs",
                    style = small_italics)
            ], style= title_box),
            html.Div(style = {"padding":10}),# For vertical space
            html.Div([

                html.Div([
                    dcc.Graph(id='canada1',style = {"height":"55vh"},hoverData={'points': [{'customdata': 'Alberta'}]}),

                ],style = graph_style,className="six columns"),
                html.Div([
                    dcc.Graph(id='canada2',style = {"height":"55vh"},hoverData={'points': [{'customdata': 'Alberta'}]}),
                ],style = graph_style,className="six columns"),

            ],className="row"),
            html.Div(style = {"padding":10}),# For vertical space
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='canada1-line',style = {"height":"40vh"}),
                    ],className="three columns"),
                    html.Div([
                        dcc.Graph(id='canada1-bar',style = {"height":"40vh"}),
                    ],className="three columns"),
                ]),
                html.Div([
                    html.Div([
                        dcc.Graph(id='canada2-line',style = {"height":"40vh"}),
                    ],className="three columns"),
                    html.Div([
                        dcc.Graph(id='canada2-bar',style = {"height":"40vh"}),
                    ],className="three columns"),
                ]),
            ],style = graph_style),
            ]),
        ]), # End of Tab 2

        # Tab 3
        dcc.Tab(label='Analytics',
        value='tab-3',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div([ # outer div tag for the page
                html.Div([ # start of graph
                    html.Div(style = {"padding":20}),# For vertical space
                    html.Div([
                        html.H2("Number of days since first case Vs current figures",
                        style=heading2, className = "container"),
                    ], style= title_box,),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([
                        html.Div([
                            html.P("Select the data"),
                            dcc.Dropdown(
                                   id='tab-3-Dropdown1',
                                   options=target_options1,
                                   value='Confirmed',
                                   style={'width':'60%', 'text-align':'left', 'color':colors["text1"],'float':'center'}
                               ),
                        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                        html.Div([

                              html.P("Select the number"),
                              dcc.Dropdown(
                                  id='tab-3-Dropdown2',
                                  options=top_options,
                                  value="Top 20",
                                  style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                              ),
                          ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                    ], style=title_box,className = "container"),

                    html.Div(style = {"padding":20}),# For vertical space
                    html.Div([
                       dcc.Graph(
                                   id='no-of-days',
                                   style = {"height":"80vh",'float':'center'}),
                    ],style=graph_style),

                ]), # End of Div for first graph

            html.Div([
                html.Div(style = {"padding":20}),# For vertical space
                    html.Div([
                        html.H2("Calendar Heatmap of New Cases",
                        style=heading2, className = "container"),
                        html.P("By World and Countries", style = small_italics)
                    ], style= title_box,className = "container"),
                html.Div(style = {"padding":10}),# For vertical space


                # html.Div(style = {"padding":20}),# For vertical space
                # html.Div([
                #     html.Div(style = {"padding":20}),# For vertical space
                #     html.Div([
                #         html.H2("Calendar Heatmap of New Cases",
                #         style=heading2, className = "container"),
                #         # html.P("Globally and by Countries", style = small_italics)
                #     ], style= title_box,className = "container"),
                #
                #     # ], style= title_box,className = "container"),
                #
                #
                #     html.Div(style = {"padding":10}),# For vertical space
                html.Div([
                    html.Div([
                        html.P("Select Global/Country"),
                        dcc.Dropdown(
                               id='tab-3-Dropdown5',
                               options=country_options1,
                               value='Global',
                               style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                           ),
                    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                html.Div([

                          html.P("Select the data"),
                           dcc.Dropdown(
                                  id='tab-3-Dropdown6',
                                  options=target_options3,
                                  value="New Confirmed",
                                  style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                              ),
                     ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

                ],style = title_box, className = "container"),

                html.Div(style = {"padding":20}),# For vertical space
                    # html.Div(style = {"padding":20}),# For vertical space
                html.Div([
                       dcc.Graph(
                                   id='heatmap',
                                   style = {"height":"80vh",'float':'center'}),
                ],style=graph_style),

                ]), # End of Div for third graph
            html.Div([
                html.Div(style = {"padding":20}),# For vertical space
                html.Div([
                html.H2("Hierarchical contribution Of Cases",
                    style=heading2, className = "container"),
                html.P("By Countries and Province/States", style = small_italics)
                ], style= title_box,className = "container"),
                html.Div(style = {"padding":10}),# For vertical space
                html.Div([
                html.Div([
                    html.P("Select Global/Country"),
                    dcc.Dropdown(
                           id='tab-3-Dropdown3',
                           options=country_options,
                           value='Global',
                           style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                       ),
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                html.Div([

                      html.P("Select the data"),
                       dcc.Dropdown(
                              id='tab-3-Dropdown4',
                              options=target_options,
                              value="Confirmed",
                              style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                          ),
                  ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

                ],style = title_box, className = "container"),

                html.Div(style = {"padding":20}),# For vertical space
                # html.Div(style = {"padding":20}),# For vertical space
                html.Div([
                    html.Div([
                       dcc.Graph(
                                   id='treemap',
                                   style = {"height":"80vh",'float':'center'}),
                    ],className = "six columns"),

                    html.Div([
                       dcc.Graph(
                                   id='sunburst',
                                   style = {"height":"80vh",'float':'center'}),
                    ],className = "six columns"),
                ],style = graph_style),
            ]), # End of Div for second graph
            ]),


            ]), # End of Tab 3
        # Tab 4
        dcc.Tab(label='Weekly Forecast & Trends',
        value='tab-4',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div([
                html.Div([
                    html.Div(style = {"padding":20}),# For vertical space
                    html.Div([
                        html.H2("Current Trend and Forecast for a Week",
                            style=heading2, className = "container"),

                    ], style=title_box,className = "container"),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([
                        html.Div([
                            html.P("Select the data"),
                            dcc.Dropdown(
                                   id='tab-4-Dropdown1',
                                   options=target_options,
                                   value='Confirmed',
                                   style={'width':'70%', 'text-align':'left', 'color':colors["text1"]}
                               ),
                        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
                        html.Div([

                              html.P("Select the group of Countries"),
                               dcc.Dropdown(
                                      id='tab-4-Dropdown2',
                                      options=countries_options,
                                      value='Top 10',
                                      style={'width':'70%', 'text-align':'left', 'color':colors["text1"]}
                                  ),
                          ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
                        # html.Div([
                        #       html.P("Select the Scale"),
                        #        dcc.RadioItems(
                        #               id='tab-4-scale',
                        #               options=scale_options,
                        #               value='Linear',
                        #               labelStyle={'display': 'inline-block'},
                        #               style={'width':'100%', 'text-align':'left', 'color':colors["text1"]}
                        #           ),
                        #   ], style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),
                    ], style=title_box,className = "container"),

                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([
                       dcc.Graph(
                                   id='forecast',
                                   style = {"height":"80vh"},
                                   className = "twelve columns"),
                    ],style = chart_box1,className="row"),

                html.Div([ # starting next row
                    html.Div([
                        html.Div(style = {"padding":20}),# For vertical space
                        html.H2("Weekly Moving Average of New Cases Vs Total",
                            style=heading2, className = "container"),

                    ], style=title_box,className = "container"),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([
                        # html.Div([
                        #     html.P("Select the type of Moving Average"),
                        #     dcc.Dropdown(
                        #            id='tab-4-Dropdown3',
                        #            options= moving_average_options,
                        #            value='Simple',
                        #            style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
                        #        ),
                        # ], style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),
                        html.Div([
                              html.P("Select the Scale"),
                               dcc.RadioItems(
                                      id='tab-4-scale',
                                      options=scale_options,
                                      value='Linear',
                                      labelStyle={'display': 'inline-block'},
                                      style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
                                  ),
                          ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),
                        html.Div([
                            html.P("Select the data"),
                            dcc.Dropdown(
                                   id='tab-4-Dropdown4',
                                   options=target_options1,
                                   value='Confirmed',
                                   style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
                               ),
                        ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),
                        # html.P('Linear scale shows linear progression on both axes and log scale shows logarithmic progression.'+
                        #  "Linear scale gives overall trend of new cases. Logarithmic scale goes a steep upward trend and then gives a "+
                        #  " huge dip when there is a regular decrease")
                        # html.Div([
                        #
                        #       html.P("Select the Countries"),
                        #        dcc.Dropdown(
                        #               id='tab-4-Dropdown5',
                        #               options=countries_options,
                        #               value='Top 10',
                        #               style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
                        #           ),
                        #   ], style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),

                    ], style=title_box,className = "container"),

                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([
                       dcc.Graph(
                                   id='moving-average',
                                   style = {"height":"80vh"},
                                   className = "twelve columns"),
                    ],style = chart_box1,className="row"),

                    ]),

                ]), # End of Div for first graph
            ])

            ]), # End of Tab 4

        # Tab 5
        dcc.Tab(label='COVID Research Clustering ',
        value='tab-5',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [

            ]) # End of Tab 5
    ])


])


@app.callback(Output('us','children'),
            [Input('optionbubble','value')])
def update_div(case):
    country = country_df.loc[country_df['Country/Region'] == "US"]
    return_divs = []
    return_divs.append(html.P(''+country[case].astype(int).apply(str),style={'text-align':'center','font-family':'sans-serif', 'color': colors[case], 'font-size': '20px'}))
    return return_divs

@app.callback(Output('spain','children'),
            [Input('optionbubble','value')])
def update_div(case):
    country = country_df.loc[country_df['Country/Region'] == "Spain"]
    return_divs = []
    return_divs.append(html.P(''+country[case].astype(int).apply(str),style={'text-align':'center','font-family':'sans-serif', 'color': colors[case], 'font-size': '20px'}))
    return return_divs

@app.callback(Output('italy','children'),
            [Input('optionbubble','value')])
def update_div(case):
    country = country_df.loc[country_df['Country/Region'] == "Italy"]
    return_divs = []
    return_divs.append(html.P(''+country[case].astype(int).apply(str),style={'text-align':'center','font-family':'sans-serif', 'color': colors[case], 'font-size': '20px'}))
    return return_divs

@app.callback(Output('germany','children'),
            [Input('optionbubble','value')])
def update_div(case):
    country = country_df.loc[latest_df['Country/Region'] == "Germany"]
    return_divs = []
    return_divs.append(html.P(''+country[case].astype(int).apply(str),style={'text-align':'center','font-family':'sans-serif', 'color': colors[case], 'font-size': '20px'}))
    return return_divs

@app.callback(Output('france','children'),
            [Input('optionbubble','value')])
def update_div(case):
    country = country_df.loc[country_df['Country/Region'] == "France"]
    return_divs = []
    return_divs.append(html.P(''+country[case].astype(int).apply(str),style={'text-align':'center','font-family':'sans-serif', 'color': colors[case], 'font-size': '20px'}))
    return return_divs

@app.callback(Output('china','children'),
            [Input('optionbubble','value')])
def update_div(case):
    country = country_df.loc[country_df['Country/Region'] == "China"]
    return_divs = []
    return_divs.append(html.P(''+country[case].astype(int).apply(str),style={'text-align':'center','font-family':'sans-serif', 'color': colors[case], 'font-size': '20px'}))
    return return_divs

@app.callback(Output('iran','children'),
            [Input('optionbubble','value')])
def update_div(case):
    country = country_df.loc[country_df['Country/Region'] == "Iran"]
    return_divs = []
    return_divs.append(html.P(''+country[case].astype(int).apply(str),style={'text-align':'center','font-family':'sans-serif', 'color': colors[case], 'font-size': '20px'}))
    return return_divs

@app.callback(
    Output('chlorepath','figure'),
    [Input('option', 'value')])
def update_table(column):
        # fig = px.choropleth_mapbox()
        fig = go.Figure(go.Choropleth(locationmode = 'country names', locations=country_df['Country/Region'], z=country_df[column],
                                            colorscale= "portland",
                                            zmin=country_df[column].min(), zmax=country_df[column].max(),
                                            marker_opacity=1, marker_line_width=0.5, customdata = country_df['Country/Region']))
        fig["layout"].update(paper_bgcolor=colors["graph_bg_color"], plot_bgcolor=colors["graph_bg_color"])
        fig.update_layout(
                            geo=dict(
                                showframe=False,
                                showcoastlines=False,
                                projection_type='equirectangular',
                                ),
                                dragmode= False,
                                margin={"r":0,"t":0,"l":0,"b":0}
                        )

        return fig

@app.callback(
    Output('bubblemap','figure'),
    [Input('optionbubble', 'value')])
def update_table(column):
        alldf = countryDays_df
        print(alldf.dtypes)
        # alldf['Date'] = alldf['Date'].dt.strftime('%x')
        fig = px.scatter_geo(alldf,
                    lat = "Lat",
                    lon = "Long",
                    # animation_frame="Date",
                    size_max = 100,
                    hover_data = ['Country/Region', column],
                    size=alldf[column],
                    color = 'Country/Region',
                    # color_continuous_scale= 'portland'
                    # colorscale = "portland"

                    )
        fig.update_layout(
                            geo=dict(
                                showframe=False,
                                showcoastlines=False,
                                projection_type='equirectangular'),
                            dragmode = False,
                            showlegend=False,
                            margin={"r":0,"t":0,"l":0,"b":0},
                            paper_bgcolor=colors["graph_bg_color"], plot_bgcolor=colors["graph_bg_color"]
                        )

        return fig

@app.callback(Output('type','children'),
            [Input('chlorepath','hoverData')])
def update_div(hoverData):
    country = hoverData['points'][0]['customdata']
    if country == "Canada":
        country = ""
    return_divs = []
    provincedf = latest_df.loc[latest_df['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if len(provinces) == 1 or country == "" or country == "Canada":
            return_divs.append(html.P('World',style={'text-align':'center','font-family':'sans-serif', 'color': '#303030', 'font-size': '15px'}))
    if len(provinces) != 1 and country != "Canada":
        return_divs.append(html.P(country,style={'text-align':'center','font-family':'sans-serif', 'color': '#303030', 'font-size': '15px'}))
    return return_divs

@app.callback(Output('div-1','children'),
            [Input('chlorepath','hoverData')])
def update_div(hoverData):
    country = hoverData['points'][0]['customdata']
    if country == "Canada" or country == "Syria":
        country = ""
    return_divs = []
    provincedf = latest_df.loc[latest_df['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if len(provinces) != 1:
        if provinces.iloc(0) == 0:
            provinces = provinces[1:]
    if len(provinces) == 1 or country == "" or country == "Canada":
        for country in countries:
            newdf = country_df.loc[country_df['Country/Region'] == country]
            return_divs.append(html.Div(html.P(""+country.upper(), style = {'font-size': '10px', 'text-align':'center', 'color': "#585858"})))
    else:
        for province in provinces:
            if province != "0":
                newdf = latest_df.loc[latest_df['Province/State'] == province]
                return_divs.append(html.Div(html.P(""+province.upper(), style = {'font-size': '10px', 'text-align':'center', 'color': "#585858"})))
    return return_divs

@app.callback(Output('count_total_comfirmed','children'),
            [Input('chlorepath','hoverData')])
def update_div(hoverData):
    country = hoverData['points'][0]['customdata']
    if country == "Canada" or country == "Syria":
        country = ""
    return_divs = []
    provincedf = latest_df.loc[latest_df['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if len(provinces) == 1 or country == "" or country == "Canada":
        return_divs.append(html.P(""+confirmedVal, style = {'font-size': '13px', 'text-align':'center', 'color': '#383838'}))
    else:
        ndf = country_df.loc[country_df['Country/Region'] == country]
        return_divs.append(html.P(""+ndf["Confirmed"].astype(int).apply(str), style = {'font-size': '13px', 'text-align':'center', 'color': '#383838'}))
    return return_divs

@app.callback(Output('count_total_death','children'),
            [Input('chlorepath','hoverData')])
def update_div(hoverData):
    country = hoverData['points'][0]['customdata']
    if country == "Canada" or country == "Syria":
        country = ""
    return_divs = []
    provincedf = latest_df.loc[latest_df['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if len(provinces) == 1 or country == "" or country == "Canada":
        return_divs.append(html.P(""+DeathVal, style = {'font-size': '13px', 'text-align':'center', 'color': '#da5657'}))
    else:
        ndf = country_df.loc[country_df['Country/Region'] == country]
        return_divs.append(html.P(""+ndf["Death"].astype(int).apply(str), style = {'font-size': '13px', 'text-align':'center', 'color': '#da5657'}))
    return return_divs

@app.callback(Output('count_total_recovered','children'),
            [Input('chlorepath','hoverData')])
def update_div(hoverData):
    country = hoverData['points'][0]['customdata']
    if country == "Canada" or country == "Syria":
        country = ""
    return_divs = []
    provincedf = latest_df.loc[latest_df['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if len(provinces) == 1 or country == "" or country == "Canada":
        return_divs.append(html.P(""+RecoveredVal, style = {'font-size': '13px', 'text-align':'center', 'color': '#45df7e'}))
    else:
        ndf = country_df.loc[country_df['Country/Region'] == country]
        return_divs.append(html.P(""+ndf["Recovered"].astype(int).apply(str), style = {'font-size': '13px', 'text-align':'center', 'color': '#45df7e'}))
    return return_divs


@app.callback(Output('div-2','children'),
            [Input('chlorepath','hoverData')])
def update_div(hoverData):
    country = hoverData['points'][0]['customdata']
    if country == "Canada" or country == "Syria":
        country = ""
    return_divs = []
    provincedf = latest_df.loc[latest_df['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if len(provinces) != 1:
        if provinces.iloc(0) == 0:
            provinces = provinces[1:]
    if len(provinces) == 1 or country == "" or country == "Canada":
        for country in countries:
                newdf = country_df.loc[country_df['Country/Region'] == country]
                return_divs.append(html.Div(html.P(""+newdf["Confirmed"].astype(int).apply(str), style = {'font-size': '10px', 'text-align':'center', 'color' : '#383838'})))
    if len(provinces) != 1 and country != "Canada":
        for province in provinces:
            if province != "0":
                newdf = latest_df.loc[latest_df['Province/State'] == province]
                return_divs.append(html.Div(html.P(""+newdf["Confirmed"].astype(int).apply(str), style = {'font-size': '10px', 'text-align':'center', 'color' : '#383838'})))
    return return_divs


@app.callback(Output('div-3','children'),
            [Input('chlorepath','hoverData')])
def update_div(hoverData):
    country = hoverData['points'][0]['customdata']
    if country == "Canada" or country == "Syria":
        country = ""
    return_divs = []
    provincedf = latest_df.loc[latest_df['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if len(provinces) != 1:
        if provinces.iloc(0)==0:
            provinces = provinces[1:]
    if len(provinces) == 1 or country == "" or country == "Canada":
        for country in countries:
            newdf = country_df.loc[country_df['Country/Region'] == country]
            return_divs.append(html.Div(html.P(""+newdf["Death"].astype(int).apply(str), style = {'font-size': '10px', 'text-align':'center', 'color' : '#383838'})))
    if len(provinces) != 1 and country != "Canada":
        for province in provinces:
            if province != "0":
                newdf = latest_df.loc[latest_df['Province/State'] == province]
                return_divs.append(html.Div(html.P(""+newdf["Death"].astype(int).apply(str), style = {'font-size': '10px', 'text-align':'center', 'color' : '#383838'})))
    return return_divs

@app.callback(Output('div-4','children'),
            [Input('chlorepath','hoverData')])
def update_div(hoverData):
    country = hoverData['points'][0]['customdata']
    if country == "Canada" or country == "Syria" :
        country = ""
    return_divs = []
    provincedf = latest_df.loc[latest_df['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if len(provinces) != 1:
        if provinces.iloc(0) == 0:
            provinces = provinces[1:]
    if len(provinces) == 1 or country == "" or country == "Canada":
        for country in countries:
            newdf = country_df.loc[country_df['Country/Region'] == country]
            return_divs.append(html.Div(html.P(""+newdf["Recovered"].astype(int).apply(str), style = {'font-size': '10px', 'text-align':'center', 'color' : '#383838'})))
    if len(provinces) != 1 and country != "Canada":
        for province in provinces:
            if province != "0":
                newdf = latest_df.loc[latest_df['Province/State'] == province]
                return_divs.append(html.Div(html.P(""+newdf["Recovered"].astype(int).apply(str), style = {'font-size': '10px', 'text-align':'center', 'color' : '#383838'})))
    return return_divs

@app.callback(Output('onebar','figure'),
            [Input('option', 'value'),
             Input('chlorepath','hoverData')])
def update_figure(value, hoverData):
    country = hoverData['points'][0]['customdata']
    str = "New"+" "+value
    if str == "New Active":
        str = "New Confirmed"
        value = "Confirmed"
    if country == "":
        fig = go.Figure(go.Bar(x=sumdf['Date'], y=sumdf[str],name=value))
        country = "World"
    else:
        newcases_df = countryDays_df.loc[countryDays_df['Country/Region'] == country]
        fig = go.Figure(go.Bar(x=newcases_df['Date'], y=newcases_df[str],
                                name=value))
    fig.update_layout(
    title={
        'text': country+ " : " + str,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    font=dict(
        family="sans-serif",
        size=11.5,
        color= '#303030'
    ),
    paper_bgcolor= "rgb(250, 250, 250)",
    plot_bgcolor= "rgb(250, 250, 250)",)
    fig.update_layout(margin={"r":1,"t":45,"l":1,"b":0})
    # fig = px.bar(province_df,x="Date",y="New Death")
    return fig

@app.callback(Output('oneline','figure'),
            [Input('optionbubble', 'value')])
def update_figure(value):
    top_countries = ["US","Spain","Italy","Germany", "France", "China", "Iran"]
    g_data = []
    for country in top_countries:
        ndf = countryDays_df.loc[countryDays_df['Country/Region'] == country]
        trace = go.Scatter( x=ndf['Date'],
                            y=ndf[value],
                            mode='lines',
                            name=country)
        g_data.append(trace)

    layout = go.Layout(
                            xaxis = dict(title='Date'),
                            yaxis = dict(title ='Number of '+value+' Cases'),
                            hovermode = 'closest')
    # fig = px.bar(province_df,x="Date",y="New Death")
    fig = go.Figure(data = g_data,layout = layout)
    fig.update_layout(
    title={
        'text': value,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    font=dict(
        family="sans-serif",
        size=11.5,
        color= '#303030'
    ),
    paper_bgcolor= "rgb(250, 250, 250)",
    plot_bgcolor= "rgb(250, 250, 250)",)
    fig.update_layout(margin={"r":1,"t":45,"l":1,"b":0})
    return fig

@app.callback(Output('doughnut','figure'),
            [Input('optionbubble', 'value')])
def update_figure(value):
    labels = ["US","Spain","Italy","Germany", "France", "China", "Iran"]
    values = []
    for country in labels:
        ndf = country_df.loc[country_df['Country/Region'] == country]
        a = ndf[value].astype(int).to_numpy()
        values.append(a[0])
    # print(values)
    fig = go.Figure(data=[go.Pie(labels=labels, values= values, hole=.3)])
    fig.update_layout(
    font=dict(
        family="sans-serif",
        size=11.5,
        color= '#303030'
    ),
    paper_bgcolor= "rgb(250, 250, 250)",
    plot_bgcolor= "rgb(250, 250, 250)",)
    fig.update_layout(margin={"r":1,"t":45,"l":1,"b":0})
    return fig


def canada_map(column,n):
    fig = go.Figure()
    # py.sign_in('username', 'api_key')
    selected_df = canada_df[~canada_df['Location'].isin(['Canada','Diamond Princess','Grand Princess'])]
    # print(selected_df['Location'])


    my_text = [location+'<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+'<br>Deaths:'+'{:,d}'.format(deaths)+
  '<br>Recovered: '+'{:,d}'.format(recovered)+'<br>Fatality Rate:'+'{:.2f} %'.format(fatality)+
  '<br>Latest New Cases: '+'{:,d}'.format(new_cases)+'<br>Cases per 100,000 :'+'{:,d}'.format(ratio)
  for location, confirmed, deaths, recovered, fatality, new_cases, ratio
    in zip(list(selected_df['Location']),list(selected_df['Confirmed']), list(selected_df['Death']),
    list(selected_df['Recovered']), list(selected_df['Fatality Rate']),
      list(selected_df['New Confirmed']), list(selected_df['Cases Per Population'])) ]

    trace1 = {"uid": "1a57419c-8c71-11e8-b0f0-089e0178c4cf",
    "mode": "markers+text", "name": "",
    "type": "scattergeo",
    "lat": list(selected_df['Lat']),
    "lon": list(selected_df['Long']),
      "marker": {
        "line": {"width": 1},
        "size": list(selected_df[column]/n),
        "color": list(selected_df[column]/n),
        # "color": ["#bebada", "#fdb462", "#fb8072", "#d9d9d9", "#bc80bd", "#b3de69", "#8dd3c7", "#80b1d3", "#fccde5", "#ffffb3"]
      },
      'customdata': selected_df['Location'],
      'text':  selected_df['Location'],
      'hovertemplate' :my_text,
      "textfont": {
        "size":10,
        # "color": ["#bebada", "#fdb462", "#fb8072", "#d9d9d9", "#bc80bd", "#b3de69", "#8dd3c7", "#80b1d3", "#fccde5", "#ffffb3"],
        # "family": ["Arial, sans-serif", "Balto, sans-serif", "Courier New, monospace", "Droid Sans, sans-serif", "Droid Serif, serif", "Droid Sans Mono, sans-serif", "Gravitas One, cursive", "Old Standard TT, serif", "Open Sans, sans-serif", "PT Sans Narrow, sans-serif", "Raleway, sans-serif", "Times New Roman, Times, serif"]
      },
      "textposition": ["top center", "middle left", "top center", "bottom center", "top right", "middle left", "bottom right", "bottom left", "top right", "top right"]
    }

    data = Data([trace1])
    layout = {
          "geo": {
            "scope": "north america",
            "lataxis": {"range": [40, 70]},
            "lonaxis": {"range": [-140, -30]}
          },
          'clickmode': 'event+select',
          'dragmode': False,
          'margin': dict(l=60, r=10, t=20, b=5, autoexpand = True),
          "title": "Canada: "+column,
          'title_x':0.5,
          'title_y':0.96    ,
          'titlefont': dict(
              color=colors['text1'],
              size=22)
    }
    fig = Figure(data=data, layout=layout)
    return fig

@app.callback(Output('canada1','figure'),
        [Input('tab-3-Dropdown1','value')])
def update_figure(val):

    fig = canada_map("Confirmed",100)
    return fig

@app.callback(Output('canada2','figure'),
        [Input('tab-3-Dropdown1','value')])
def update_figure(val):
    # canada_df = latest_df.loc[latest_df['Country/Region'] == 'Canada']
    fig = canada_map("Death",5)
    return fig


@app.callback(Output('canada1-line','figure'),
        [Input('canada1','hoverData')])
def update_figure(hoverData):
    province = hoverData['points'][0]['customdata']
    province_df = df.loc[df['Location'] == province]
    province_df = province_df.loc[province_df['Confirmed'] != 0]

    fig = go.Figure(go.Scatter(x=province_df['Date'], y=province_df['Confirmed'],
                    mode='lines+markers',marker_color='orange',
                    name=province))
    fig.update_layout(
    title= province + " : Cumulative Confirmed Cases",
    title_x= 0.5,
    titlefont= dict(
        color=colors['heading'],
        size=18
    ),
    margin=dict(l=20, r=20, t=40, b=20, autoexpand = True),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)
    # fig = px.scatter(province_df,x="Date",y="Confirmed",mode = "line+markers")
    return fig

@app.callback(Output('canada1-bar','figure'),
        [Input('canada1','hoverData')])
def update_figure(hoverData):
    province = hoverData['points'][0]['customdata']
    province_df = df.loc[df['Location'] == province]
    province_df = province_df.loc[province_df['New Confirmed'] != 0]
    fig = go.Figure(go.Bar(x=province_df['Date'], y=province_df['New Confirmed'],
                        name=province, marker_color='orange'))
    fig.update_layout(
    title= province + " : New Confirmed Cases",
    title_x= 0.5,
    titlefont= dict(
        color=colors['heading'],
        size=18
    ),
    margin=dict(l=20, r=20, t=40, b=20, autoexpand = True),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)
    # fig = px.bar(province_df,x="Date",y="New Confirmed")
    return fig

@app.callback(Output('canada2-line','figure'),
        [Input('canada2','hoverData')])
def update_figure(hoverData):
    province = hoverData['points'][0]['customdata']
    province_df = df.loc[df['Location'] == province]
    province_df = province_df.loc[province_df['Death'] != 0]
    fig = go.Figure(go.Scatter(x=province_df['Date'], y=province_df['Death'],
                    mode='lines+markers',
                    name=province,marker_color='crimson'))
    fig.update_layout(
    title= province + " : Cumulative Deaths",
    title_x= 0.5,
    titlefont= dict(
        color=colors['heading'],
        size=18
    ),
    margin=dict(l=20, r=20, t=40, b=20, autoexpand = True),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)
    return fig

@app.callback(Output('canada2-bar','figure'),
        [Input('canada2','hoverData')])
def update_figure(hoverData):
    province = hoverData['points'][0]['customdata']
    province_df = df.loc[df['Location'] == province]
    province_df = province_df.loc[province_df['New Death'] != 0]
    fig = go.Figure(go.Bar(x=province_df['Date'], y=province_df['New Death'],
                            name=province, marker_color='crimson'))
    fig.update_layout(
    title= province + " : New Deaths",
    title_x= 0.5,
    titlefont= dict(
        color=colors['heading'],
        size=18
    ),
    margin=dict(l=20, r=20, t=40, b=20, autoexpand = True),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)
    return fig

@app.callback(Output('no-of-days','figure'),
        [Input('tab-3-Dropdown1','value'),
        Input('tab-3-Dropdown2','value')])
def update_figure(y_axis,top):

    if top == "Top 20":
        top_num = 20
    elif top == "Top 30":
        top_num = 30
    elif top == "Top 40":
        top_num = 40

    if y_axis == 'Recovered':
        line_color = "#21D12B"
        colorscale = "viridis"
    elif y_axis == 'Death':
        line_color = "red"
        colorscale = "reds"
    else:
        line_color = "orange"
        colorscale = "portland"
    # Copying the rows with rows ! = 0
    grouped_df = df.loc[df[y_axis] != 0].copy()
    grouped_df = grouped_df.sort_values(['Date'], ascending = True)
    # print(grouped_df)
    aggregations = {'Date':'first','Confirmed':'count','Active':'count','Death':'count','Recovered':'count'}
    count_df = grouped_df.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values
    count_df['NoOfDays'] = ((pd.to_datetime("now") - count_df['Date'])/np.timedelta64(1,'D')).astype(int)

    aggregations = {'Date':'first','Confirmed':'sum','Active':'sum','Death':'sum','Recovered':'sum'}
    current_df = latest_df.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values
    # print(current_df.head())

    count_df=count_df.sort_values(['NoOfDays'],ascending = True)
    # print(count_df.head())

    # count_df = count_df.set_index('NoOfDays')
    current_df = current_df.set_index('Country/Region')
    current_df = current_df.reindex(index=count_df['Country/Region'])
    current_df = current_df.reset_index()
    # print(current_df.head())
    limit = len(current_df.index)-top_num
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=False, vertical_spacing=0.001,)
                    # subplot_titles=('No. of days since first '+y_axis+' case','Total '+y_axis+' cases'))
    fig.append_trace(go.Bar(x=count_df['NoOfDays'].iloc[limit:],
                    y=count_df['Country/Region'].iloc[limit:],
                    marker=dict(
                        color=count_df['NoOfDays'].iloc[limit:],
                        colorscale = colorscale,
                        line=dict(
                            # color='rgba(50, 171, 96, 1.0)',
                            width=1),
                    ),
                    name='No. of days since the first ' +y_axis+' case',
                    orientation='h',
                ), 1, 1)

    fig.append_trace(go.Scatter(
        x=current_df[y_axis].iloc[limit:], y=current_df['Country/Region'].iloc[limit:],
        mode='lines+markers',
        line_color= line_color,
        line_width = 5,
        name='Total '+y_axis+' Cases',
        textposition="middle right",
    ), 1, 2)

    fig.update_layout(
    # title='Number of days since the first '+y_axis+' case and Current figure' ,
    yaxis=dict(
        showgrid=False, showline=True, showticklabels=True, domain=[0, 0.85], ),
    yaxis2=dict(
        showgrid=False, showline=True, showticklabels=False, linecolor='rgba(102, 102, 102, 0.8)',
        linewidth=2, domain=[0, 0.85],
    ),
    xaxis=dict(
        zeroline=False, showline=False, showticklabels=True, showgrid=True, domain=[0, 0.42],),
    xaxis2=dict(
        zeroline=False, showline=False, showticklabels=True, showgrid=True, domain=[0.47, 1], side='top', dtick=25000,
    ),
    # legend=dict(x=0.029, y=1.038, font_size=10),
    # margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)

    annotations = []
    # Adding labels
    for ydn, yd, xd in zip(current_df[y_axis].iloc[limit:], count_df['NoOfDays'].iloc[limit:], count_df['Country/Region'].iloc[limit:]):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2', y=xd, x=ydn+5*current_df[y_axis].mean(),
                                text=xd+": "+'{:,}'.format(ydn) ,
                                font=dict(family='Arial', size=12, color=colors['graph_text']),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1', y=xd, x=yd+3,
                                text=str(yd) ,
                                font=dict(family='Arial', size=12, color=colors['graph_text']),
                                showarrow=False))
        annotations.append(dict(xref='paper', yref='paper', x=0.1, y=0.94,
                                text='No. of days since first '+y_axis+' Case',
                                font=dict(size=22, color=colors['text1']),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='paper', yref='paper', x = 0.85, y = 0.94,
                                text='Total '+y_axis+' Cases' ,
                                font=dict(size=22, color=colors['text1']),
                                showarrow=False))
    # annotations.append({'text': "Number of Confirmed Cases", 'xref': 'paper', 'yref': 'paper',
    #                         'x': .5, 'y': max_pos, 'xanchor': 'center', 'yanchor': 'bottom', 'showarrow': False, 'font': dict(size = 22)}

    fig.update_layout(annotations=annotations,
    title_x= 0.5,
    titlefont= dict(
        color=colors['heading'],
        size=22
    ),
    margin=dict(l=20, r=20, t=20, b=20, autoexpand = True))




    return fig

@app.callback(Output('treemap','figure'),
        [Input('tab-3-Dropdown3','value'),
        Input('tab-3-Dropdown4','value')])
def update_figure(option,y_axis):
    # colorscale = "portland"
    if y_axis == 'Recovered':
        colorscale = "viridis"
    elif y_axis == 'Death':
        colorscale = "reds"
    elif y_axis == "Active":
        colorscale = 'peach'
    else:
        colorscale = "portland"


    if option == 'Global':
        selected_df = country_df
        # selected_df["World"] = "World" # in order to have a single root node
        pathlist = ['Country/Region']
        data = ['Country/Region', 'Confirmed','Death','Recovered','New Confirmed']
    else:
        selected_df = latest_df.loc[latest_df['Country/Region']==option]
        pathlist = ['Location']
        data = ['Country/Region','Province/State', 'Confirmed','Death','Recovered','New Confirmed']
        # selected_df["world"] = "world" # in order to have a single root node
    selected_df = selected_df[selected_df[y_axis]>0]

    my_text = ['Confirmed Cases: '+'{:,d}'.format(confirmed)+'<br>Deaths:'+'{:,d}'.format(deaths)+
  '<br>Recovered: '+'{:,d}'.format(recovered)+'<br>Fatality Rate:'+'{:.2f} %'.format(fatality)+
  '<br>Latest New Cases: '+'{:,d}'.format(new_cases)
  for confirmed, deaths, recovered, fatality, new_cases,
    in zip(list(selected_df['Confirmed']), list(selected_df['Death']),
    list(selected_df['Recovered']), list(selected_df['Fatality Rate']),
      list(selected_df['New Confirmed'])) ]

    fig = px.treemap(selected_df, path=pathlist, values=y_axis,template = template,
                          color=y_axis, color_continuous_scale=colorscale,
                          color_continuous_midpoint=np.average(selected_df[y_axis], weights=selected_df[y_axis]))
    # fig.data[0].customdata[:, 0] = my_text
    fig.update_layout(
    margin=dict(l=20, r=10, t=10, b=10))
    return fig

@app.callback(Output('sunburst','figure'),
        [Input('tab-3-Dropdown3','value'),
        Input('tab-3-Dropdown4','value')])
def update_figure(option,y_axis):

    if y_axis == 'Recovered':
        colorscale = "viridis"
    elif y_axis == 'Death':
        colorscale = "reds"
    elif y_axis == "Active":
        colorscale = 'peach'
    else:
        colorscale = "portland"



    if option == 'Global':
        selected_df = latest_df
        # selected_df["World"] = "World" # in order to have a single root node
        pathlist = ['Country/Region','Location']

    else:
        selected_df = latest_df.loc[latest_df['Country/Region']==option]
        pathlist = ['Location']

    selected_df = selected_df[selected_df[y_axis]>0]

    fig = px.sunburst(selected_df, path=pathlist,
                    values= y_axis, color=y_axis, color_continuous_scale=colorscale,
                  color_continuous_midpoint=np.average(selected_df[y_axis], weights=selected_df[y_axis]))

    fig.update_layout(
    margin=dict(l=10, r=10, t=10, b=10, autoexpand = True),
    uniformtext_minsize=12, uniformtext_mode='hide')
    return fig

@app.callback(Output('heatmap','figure'),
        [Input('tab-3-Dropdown5','value'),
        Input('tab-3-Dropdown6','value')])
def update_figure(option,y_axis):

    aggregations = { 'Confirmed':'sum','Active':'sum','Death':'sum','Recovered':'sum','Fatality Rate':'mean',
            'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}

    if option == 'Global':
        selected_df=df.groupby(["Date"],as_index=False).agg(aggregations) #groupby Country and Date values
    else:
        selected_df = countryDays_df.loc[countryDays_df['Country/Region']==option]

    selected_df[y_axis] = pd.to_numeric(selected_df[y_axis], errors='coerce',downcast='integer')
    selected_df = selected_df.sort_values(['Date'], ascending = True )
    # year = datetime.datetime.now().year

    d1 = selected_df['Date'].min()
    d2 = selected_df['Date'].max()

    delta = d2 - d1

    dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days+1)] #gives me a list with datetimes for each day a year
    # dates_in_year = sorted(dates_in_year)
    # print(dates_in_year)
    weekdays_in_year = [i.weekday() for i in dates_in_year] #gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,...] (ticktext in xaxis dict translates this to weekdays
    weeknumber_of_dates = [int(i.strftime("%V")) for i in dates_in_year] #gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,...] name is self-explanatory
    months = [(i.strftime("%b")) for i in dates_in_year] #gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,...] name is self-explanatory

    z = list(selected_df[y_axis])

    if y_axis == 'New Recovered':
        line_color = "white"
        colorscale = "viridis"
    elif y_axis == 'New Death':
        line_color =colors['text1']
        colorscale = "reds"
    else:
        line_color = "white"
        colorscale = "portland"

    y_ticks = ["Week "+ str(s) for s in weeknumber_of_dates]
    hover_text = ["Country: "+ option +"<br>"+"Date: "+d.strftime("%x")+"<br>"+y_axis+
    " Cases: "+ "{:,d}".format(value) for d,value in zip(dates_in_year,z)] #gives something like list of strings like '2018-01-25' for each date. Used in data trace to make good hovertext.
    cell_text = [s.strftime("%x") for s in dates_in_year]

    fig = go.Figure(data = go.Heatmap(
    		x = weekdays_in_year,
    		y = weeknumber_of_dates,
    		z = z,
    		text=hover_text,
    		hoverinfo="text",
    		xgap=3, # this
    		ygap=3, # and this is used to make the grid-like apperance
    		# showscale=False,
            colorscale = colorscale
    	))
    fig.add_trace(go.Scatter(
            x = weekdays_in_year,
            y = weeknumber_of_dates,
            text = cell_text,
            mode = 'text',
            textposition = "middle center",
            textfont=dict(
            # family="sans serif",
            size=12,
            color=line_color,

            )

    ))
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
    	# title='Calendar Heatmap for '+y_axis+" Cases",
    	# height=400,
    	xaxis=dict(
    		tickmode="array",
    		ticktext=["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"],
    		tickvals=[0,1,2,3,4,5,6],
    		title="Week Days",
            showline = False,
            showgrid = False,
            zeroline = False
    	),
    	yaxis=dict(
            ticktext= y_ticks,
    		tickvals= list(weeknumber_of_dates),
    		showline = False,
            showgrid = False,
            zeroline = False,
    		title="Week Number"
    	),
    	plot_bgcolor=colors['graph_bg_color'], #making grid appear black
        font = dict(color = colors['text1'], size =12),
        margin = dict(l=500,r=500,t=40,b=30),
        # yaxis_nticks=len(set(months)),
        title_x= 0.5,
        titlefont= dict(
            color=colors['heading'],
            size=22
        ),
    )

    # fig = go.Figure(data=data, layout=layout)
    return fig


# @app.callback(Output('sankey','figure'),
#         [Input('tab-3-Dropdown3','value')])
# def update_figure(y_axis):
#     selected_df = latest_df[['Province/State','Country/Region','Confirmed','Death','Recovered']]
#     print("Selected",selected_df)
#     fig = px.parallel_categories(df, color=y_axis, color_continuous_scale=px.colors.sequential.Inferno)
#     return fig






@app.callback(Output('forecast','figure'),
        [Input('tab-4-Dropdown1','value'),
        Input('tab-4-Dropdown2','value'),])
        # Input('tab-4-scale','value')])
def update_figure(y_axis,countries):

    countryAllDays_df = countryDays_df.loc[countryDays_df[y_axis] != 0].copy()
    countryAllDays_df = countryAllDays_df.sort_values(y_axis,ascending=False)
    selector_df = countryAllDays_df.groupby(["Country/Region"],as_index=False).agg({"Date":"first",y_axis:"max"})
    selector_df = selector_df.sort_values(y_axis,ascending=False)

    if countries == "Top 10":
        limit = 10
        selected_countries = list(selector_df[:limit]['Country/Region'])
    elif countries == "G7":
        selected_countries = ['Canada','France','Germany','Italy','Japan','United Kingdom','US']
    elif countries == "BRICS":
        selected_countries = ['Brazil','Russia','India','China','South Africa']


    selected_df = countryAllDays_df[countryAllDays_df["Country/Region"].isin(selected_countries)]
    ordered_countries = list(selected_df['Country/Region'].unique())

    # print(selected_df)

    latest_date = df['Date'].max()
    next_week = []
    for x in range(1,8):
        next_day = latest_date+datetime.timedelta(days=x)
        next_week.append(next_day.date())

    print(selected_df[y_axis])
    fig = px.line(selected_df, x="Date", y=y_axis, color="Country/Region",
               hover_name="Country/Region")
    # fig.add_trace(go.Scatter(x=countryAllDays_df['Date'], y=countryAllDays_df[y_axis],
    selected_df = selected_df.sort_values(y_axis,ascending=True)
    estimator = pd.DataFrame(columns = ['Country/Region','Date','Estimated '+y_axis])
    # copy = estimator.copy()
    for country in ordered_countries:
        timeseries_df = selected_df[selected_df['Country/Region']==country]
        # print(timeseries_df[y_axis])

        prediction = forecast(list(timeseries_df[y_axis]))
        row = []
        for i in range(len(next_week)):
            row.append([country + " Estimated",next_week[i],prediction[i]])
        copy =  pd.DataFrame(row,columns = ['Country/Region','Date','Estimated '+y_axis] )
        # print(copy)
        estimator = estimator.append(copy,ignore_index=True)
    # print(estimator)
    print(estimator)
    row = []
    for country in ordered_countries:
        estimate = estimator[estimator['Country/Region']==country + " Estimated"]['Estimated '+y_axis].max()
        current = selected_df[selected_df['Country/Region']==country][y_axis].max()
        diff = int(estimate - current)
        row.append([country,diff])
    diff_df = pd.DataFrame(row,columns = ['Country/Region',y_axis])


    fig2 = px.scatter(estimator, x="Date", y='Estimated '+y_axis, color="Country/Region",
                   hover_name="Country/Region")

    for i in range(len(selected_countries)):
        fig.add_trace(fig2.data[i])

    fig.add_shape(type="line",
            x0=selected_df['Date'].max(), x1=selected_df['Date'].max(), xref="x",
            y0=0, y1=estimator['Estimated '+y_axis].max(), yref="y",
            line = dict(color="salmon", width=1, dash="dot",)
    )
    fig.update_shapes(dict(xref='x', yref='y'))
    fig.add_shape(
            # filled Rectangle
                type="rect", x0=0.125,y0=0.63,x1=0.7,y1=0.95,xref="paper",yref="paper",
                line=dict(
                    color="#A21010",
                    width=1,
                ),
                fillcolor="#D6D8D5",
            )
    # fig.update_shapes(dict(xref='paper', yref='paper'))

    fig.add_annotation( # add a text callout with arrow
        text="Forecast begins!", x=selected_df['Date'].max(), y=estimator['Estimated '+y_axis].max()/2, arrowhead=1, showarrow=True
    )
    fig.add_annotation( x=0.15, y=0.9, showarrow=False,
        text= "Highest Estimated* "+y_axis+" Cases for Next Week" ,
        xref="paper", yref="paper",bordercolor='#A21010',
            borderwidth=1, font=dict(
                color="white",
                size=24,
            ),bgcolor="#A21010",
    )
    axes = [0.84,0.79,0.74]
    diff_df = diff_df.sort_values(y_axis,ascending = False)
    for i in range(len(axes)):
        fig.add_annotation( x=0.15, y=axes[i], showarrow=False,
            text= str(i+1) + ". "+list(diff_df['Country/Region'])[i] + ":  " + str("{:,d}".format(list(diff_df[y_axis])[i])) ,
            xref="paper", yref="paper",
            font=dict(
                color="#A21010",
                size=18
            ),
        )
    fig.add_annotation( x=0.15, y=0.69, showarrow=False,
        text= "* In "+ countries + " Countries" ,
        xref="paper", yref="paper",
        font=dict(
            color="#525252",
            size=14
        ))

    fig.update_layout(
    title= countries +" Countries : "+y_axis+" Cases",
    # yaxis={'type': 'linear' if scale == 'Linear' else 'log',
    #     'autorange': True},
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],
    title_x= 0.5,
    # yaxis_type="log",
    titlefont= dict(
        color=colors['heading'],
        size=22
    ),
    # title_y = 0.05,
    margin=dict(l=60, r=20, t=80, b=20, autoexpand = True))
    return fig

@app.callback(Output('moving-average','figure'),
        [Input('tab-4-scale','value'),
        Input('tab-4-Dropdown4','value')])
        # Input('tab-4-scale','value')])
def update_figure(scale, y_axis):
    total_cases = y_axis
    new_cases = "New "+y_axis
    selected_df =  countryDays_df[['Country/Region','Date',total_cases, new_cases]]
    selector_df = latest_df.sort_values(total_cases,ascending=False)

    selected_countries = list(selector_df[:10]['Country/Region'])

    movingAvg_df = selected_df[selected_df["Country/Region"].isin(selected_countries)]

    # ordered_countries = list(movingAvg_df['Country/Region'].unique()
    movingAvg_df = movingAvg_df.sort_values(['Country/Region','Date'], ascending = True)
    ordered_countries = list(movingAvg_df['Country/Region'].unique())

    estimator = pd.DataFrame(columns = ['Country/Region','Date',total_cases, new_cases])
    prediction = []
    # if mAvg_option == moving_average_options[0]['value']:
    for country in ordered_countries:
        timeseries_df = movingAvg_df[movingAvg_df['Country/Region']==country]
        # print("moving",timeseries_df.iloc[:,-1].rolling(window=7).mean())
        prediction.extend(list(timeseries_df.iloc[:,-1].rolling(window=7).mean()))

    movingAvg_df['Moving Average'] = np.array(prediction)
    movingAvg_df.fillna(0, inplace=True)

    fig = make_subplots(rows=2, cols=5, specs=[[{},]*5,[{},]*5], shared_xaxes=False,
                    shared_yaxes=False, vertical_spacing=0.1,)

    i=1
    c=1
    for country in selected_countries[0:5]:
        each_df = movingAvg_df[movingAvg_df['Country/Region']==country]
        if i==1:
            fig.append_trace(go.Scatter(
                                        x=each_df[total_cases],
                                        y=each_df[new_cases],
                                        mode="lines+markers",
                                        name = country,
                                        xaxis = 'x',
                                        yaxis = 'y',
                                    ), row=1, col=i)
        else:
            fig.append_trace(go.Scatter(
                                    x=each_df[total_cases],
                                    y=each_df[new_cases],
                                    mode="lines+markers",
                                    name = country,
                                    xaxis = 'x'+str(c),
                                    yaxis='y'+str(c)

                                ), row=1, col=i)
        i += 1
        c += 1
    i=1
    c=5
    for country in selected_countries[5:]:
        each_df = movingAvg_df[movingAvg_df['Country/Region']==country]
        fig.append_trace(go.Scatter(
                                    x=each_df[total_cases],
                                    y=each_df[new_cases],
                                    mode="lines+markers",
                                    name = country,
                                    xaxis = 'x'+str(c),
                                    yaxis='y'+str(c)
                                ), row=2, col=i)
        i += 1
        c += 1
        # fig = px.line(movingAvg_df, x=total_cases, y=new_cases, color="Country/Region",
        #        hover_name="Country/Region", log_x = True, log_y = True)
    # annotations = []
    #
    # for i in range(1,len(selected_countries[0:5])+1):
    #     if i ==1:
    #         annotations.append({'xref': 'x','x': 0.5,
    #         'text': selected_countries[i-1]})
    #     else:
    #         annotations.append({'xref': 'x'+str(i),'x': 0.5,
    #         'text': selected_countries[i-1]})
    # for i in range(6,len(selected_countries[5:])+1):
    #     annotations.append({'xref': 'x'+str(i),'x': -0.5,
    #     'text': selected_countries[i-1]})
    # fig.update_layout(annotations=annotations)
    xaxes = [0.02,0.22,0.45,0.66,0.89]
    yaxes = [0.98,0.38]
    # diff_df = diff_df.sort_values(y_axis,ascending = False)
    c = 0
    for i in range(len(xaxes)):
        fig.add_annotation( x=xaxes[i], y=yaxes[0], showarrow=False,
            text= selected_countries[c], xref="paper", yref="paper",
            font=dict(color=colors['graph_text'], size=18))
        c+=1
    # c = 5
    for i in range(len(xaxes)):
        fig.add_annotation( x=xaxes[i], y=yaxes[1], showarrow=False,
            text= selected_countries[c], xref="paper", yref="paper",
            font=dict(color=colors['graph_text'], size=18))
        c+=1
    fig.update_layout(
    title= "Top 10 Countries : "+new_cases+" Cases Vs "+total_cases,
    xaxis= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis2= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis3= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis4= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis5= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis6= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis7= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis8= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis9= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis10= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis2= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis3= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis4= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis5= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis6= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis7= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis8= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis9= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis10= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},

    # yaxis2=dict(
    #     title = new_cases,
    #     overlaying='y',
    #     side='right'
    # )
    # yaxis={'type': 'linear' if scale == 'Linear' else 'log',
    #     'autorange': True},
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],
    title_x= 0.5,
    # yaxis_type="log",
    titlefont= dict(
        color=colors['heading'],
        size=22
    ),
    # title_y = 0.05,
    margin=dict(l=60, r=20, t=80, b=20, autoexpand = True))
    # for country in ordered_countries:
    #     selector_df = movingAvg_df[movingAvg_df['Country/Region']==country]
    #     fig.add_trace()
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
