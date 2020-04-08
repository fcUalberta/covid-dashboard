# Importing libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime as dt
from datetime import date
import numpy as np
import datetime

# Importing dependencies
from data_ingest import data_ingest
from forecasting import forecast


df, latest_df,country_df,countryDays_df = data_ingest()

# df = pd.read_csv("covid.csv",sep='\t')


# Initializing Variables

target_options = [{'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Death', 'value': 'Death'},
                        {'label': 'Recovered', 'value': 'Recovered'}]

target_options1 = [{'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Death', 'value': 'Death'}]

top_options =  [{'label': 'Top 20', 'value': 'Top 20'},
                        {'label': 'Top 30', 'value': 'Top 30'},
                        {'label': 'Top 40', 'value': 'Top 40'}]

countries_options = [{'label': 'Top 10', 'value': 'Top 10'},
                        {'label': 'G7', 'value': 'G7'},
                        {'label': 'BRICS', 'value': 'BRICS'}]

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
    'heading':'#C01414'
    # 'analytics_tab_color':''
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

tab_selected_style = {
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

# Calling external stylesheet
# external_stylesheets=['https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-web-trader/assets/style.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Initializing Dash app
# app = dash.Dash(__name__)
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
            html.Div([
            html.Div(
            children=[

                # Div for DropDown to select option
                html.Div([
                        html.Div(style = {"padding":10}),# For vertical space
                        html.H6('Select from the drop down'
                        ,style={'text-align':'left','font-family':'sans-serif', 'color': colors['text']}),

                        html.Div([
                        dcc.Dropdown(id='option',
                            options=target_options,
                            value ='Confirmed',
                            style={'width':'40%', 'text-align':'left', 'color':colors["text1"]}),
                        html.Div([
                        html.Div(style = {"padding":10}),# For vertical space
                            dcc.Graph(
                                        id='chlorepath',
                                        style = {"height":"70vh"}),
                            ], style = graph_style,
                            className="seven columns"),
                            ])


                ],className="row"), # End of Div for second container



                ]),
            ], className = "page"),


            ]), # End of Tab 1

        # Tab 2
        dcc.Tab(label='Canada Trends',
        value='tab-2',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [

            html.Div([
             html.Div(style = {"padding":10}),# For vertical space
             dcc.Dropdown(
                    id='tab-2-Dropdown',
                    options=target_options,
                    value='Confirmed',
                    style={'width':'40%', 'text-align':'left', 'color':colors["text1"]}
                ),
                dcc.Graph(id='country_bar'),

            ],className="six columns")
        ]), # End of Tab 2

        # Tab 3
        dcc.Tab(label='Analytics',
        value='tab-3',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div([
                html.Div([
                    html.Div(style = {"padding":20}),# For vertical space
                    html.H2("Number of days since first case Vs current figures",
                    style={'text-align':'center', 'color':colors["heading"]},
                    className = "container"),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([
                    html.P("Select the data"),
                    dcc.Dropdown(
                           id='tab-3-Dropdown1',
                           options=target_options1,
                           value='Confirmed',
                           style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                       ),
                      html.P("Select the Option"),
                       dcc.Dropdown(
                              id='tab-3-Dropdown2',
                              options=top_options,
                              value="Top 20",
                              style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                          ),
                    ],className = "container"),

                    html.Div(style = {"padding":20}),# For vertical space
                    html.Div([
                       dcc.Graph(
                                   id='no-of-days',
                                   style = {"height":"100vh",'float':'center'}),
                    ],style=graph_style),

                ]), # End of Div for first graph
                html.Div([
                    html.Div(style = {"padding":20}),# For vertical space
                    html.H2("Number of days since first case Vs current figures",
                    style={'text-align':'center', 'color':colors["heading"]},
                    className = "container"),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([
                    html.P("Select the data"),
                    dcc.Dropdown(
                           id='tab-3-Dropdown3',
                           options=target_options1,
                           value='Confirmed',
                           style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                       ),
                      # html.P("Select the Option"),
                       # dcc.Dropdown(
                       #        id='tab-3-Dropdown2',
                       #        options=top_options,
                       #        value="Top 20",
                       #        style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                       #    ),
                    ],className = "container"),

                    html.Div(style = {"padding":20}),# For vertical space
                    html.Div([
                       dcc.Graph(
                                   id='sankey',
                                   style = {"height":"100vh",'float':'center'}),
                    ],style=graph_style),

                ]), # End of Div for first graph
            ])

            ]), # End of Tab 3
        # Tab 4
        dcc.Tab(label='Weekly Forecast',
        value='tab-4',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div([
                html.Div([
                    html.Div(style = {"padding":20}),# For vertical space
                    html.H2("Current Trend and Forecast for a Week",
                        style={'text-align':'center', 'color':colors["heading"]},
                        className = "container"),
                    html.Div(style = {"padding":10}),# For vertical space

                    html.Div([
                    html.P("Select the data"),
                    dcc.Dropdown(
                           id='tab-4-Dropdown1',
                           options=target_options1,
                           value='Confirmed',
                           style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                       ),
                      html.P("Select the Countries"),
                       dcc.Dropdown(
                              id='tab-4-Dropdown2',
                              options=countries_options,
                              value='Top 10',
                              style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                          ),
                    ],className = "container"),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([
                       dcc.Graph(
                                   id='forecast',
                                   style = {"height":"80vh"},
                                   className = "ten columns"),
                     # html.Div([
                     #                            html.Div([
                     #        html.H6("Budget",style=content),
                     #        html.Div(id='card11',style=it_content)
                     #    ], style= graph_style,className="four columns"),
                     #
                     # ])
                    ],style = graph_style,className="row"),

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


@app.callback(
    Output('chlorepath','figure'),
    [Input('option', 'value')])
def update_table(column):
        """
        Function to update the chlorepath map object based on dropdown
        Arguments:
            column: Column to select data from
        Returns:
            Updated chlorepath map object
        """

        colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
              "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
              "#08519c","#0b4083","#08306b"]
        fig = go.Figure(go.Choropleth(locationmode = 'country names', locations=country_df['Country/Region'], z=country_df[column],
                                            colorscale= "portland",
                                            zmin=country_df[column].min(), zmax=country_df[column].max(),
                                            marker_opacity=1, marker_line_width=0.5, geo = 'geo2'))
        fig["layout"].update(paper_bgcolor=colors["graph_bg_color"], plot_bgcolor=colors["graph_bg_color"])

        return fig


@app.callback(Output('country_bar','figure'),
        [Input('option', 'value')])
def update_figure(y_axis):
    fig = px.bar(country_df, x='Country/Region', y= y_axis,
                    hover_data=['Country/Region', 'Confirmed','Death','Recovered'], color=y_axis)
    fig.update_layout(title_text='Country-wise '+y_axis,paper_bgcolor = colors["graph_bg_color"], plot_bgcolor=colors["graph_bg_color"])

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
    # Copying the rows with rows ! = 0
    grouped_df = df.loc[df[y_axis] != 0].copy()
    grouped_df = grouped_df.sort_values(['Date'], ascending = True)
    # print(grouped_df)
    aggregations = {'Date':'first','Confirmed':'count','Death':'count','Recovered':'count'}
    count_df = grouped_df.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values
    count_df['NoOfDays'] = ((pd.to_datetime("now") - count_df['Date'])/np.timedelta64(1,'D')).astype(int)

    aggregations = {'Date':'first','Confirmed':'sum','Death':'sum','Recovered':'sum'}
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
                    shared_yaxes=False, vertical_spacing=0.001,
                    subplot_titles=('No. of days since first '+y_axis+' case','Total '+y_axis+' cases'))
    fig.append_trace(go.Bar(x=count_df['NoOfDays'].iloc[limit:],
                    y=count_df['Country/Region'].iloc[limit:],
                    marker=dict(
                        # color='rgba(50, 171, 96, 0.6)',
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
        # line_color='rgb(128, 0, 128)',
        name='Current '+y_axis+' Cases',
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
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)

    annotations = []
    # Adding labels
    for ydn, yd, xd in zip(current_df[y_axis].iloc[limit:], count_df['NoOfDays'].iloc[limit:], count_df['Country/Region'].iloc[limit:]):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2', y=xd, x=ydn+2*current_df[y_axis].mean(),
                                text='{:,}'.format(ydn) ,
                                font=dict(family='Arial', size=12, color=colors['graph_text']),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1', y=xd, x=yd+3,
                                text=str(yd) ,
                                font=dict(family='Arial', size=12, color=colors['graph_text']),
                                showarrow=False))


    fig.update_layout(annotations=annotations)


    return fig



@app.callback(Output('sankey','figure'),
        [Input('tab-3-Dropdown3','value')])
def update_figure(y_axis):
    selected_df = latest_df[['Province/State','Country/Region','Confirmed','Death','Recovered']]
    print("Selected",selected_df)
    fig = px.parallel_categories(df, color=y_axis, color_continuous_scale=px.colors.sequential.Inferno)
    return fig






@app.callback(Output('forecast','figure'),
        [Input('tab-4-Dropdown1','value'),Input('tab-4-Dropdown2','value')])
def update_figure(y_axis,countries):

    grouped_df = df.loc[df[y_axis] != 0].copy()
    # print(df.head())
    # aggregations = {'Confirmed':'sum','Death':'sum','Recovered':'sum'}
    # countryAllDays_df = grouped_df.groupby(["Country/Region","Date"],as_index=False).agg(aggregations)
    countryAllDays_df = countryDays_df.sort_values(y_axis,ascending=False)
    selector_df = countryAllDays_df.groupby(["Country/Region"],as_index=False).agg({"Date":"first",y_axis:"max"})
    selector_df = selector_df.sort_values(y_axis,ascending=False)

    if countries == "Top 10":
        limit = 10
        selected_countries = list(selector_df[:limit]['Country/Region'])
    elif countries == "G7":
        selected_countries = ['Canada','France','Germany','Italy','Japan','United Kingdom','US']
    elif countries == "BRICS":
        selected_countries = ['Brazil','Russia','India','China','South Africa']
    print(selected_countries)

    # countryAllDays_df.sort_index(inplace=True)
    # selector_df.sort_index(inplace=True)
    selected_df = countryAllDays_df[countryAllDays_df["Country/Region"].isin(selected_countries)]
    ordered_countries = list(selected_df['Country/Region'].unique())

    # print(selected_df)

    latest_date = df['Date'].max()
    next_week = []
    for x in range(1,8):
        next_day = latest_date+datetime.timedelta(days=x)
        next_week.append(next_day.date())
        # next_week.append(next_day.strftime("%x"))
    # print(next_week)

    fig = px.line(selected_df, x="Date", y=y_axis, color="Country/Region",
               hover_name="Country/Region")
    # fig.add_trace(go.Scatter(x=countryAllDays_df['Date'], y=countryAllDays_df[y_axis],
    selected_df = selected_df.sort_values(y_axis,ascending=True)
    estimator = pd.DataFrame(columns = ['Country/Region','Date','Estimated '+y_axis])
    # copy = estimator.copy()
    for country in ordered_countries:
        timeseries_df = selected_df[selected_df['Country/Region']==country]
        prediction = forecast(list(timeseries_df[y_axis]))
        row = []
        for i in range(len(next_week)):
            row.append([country + " Estimated",next_week[i],prediction[i]])
        copy =  pd.DataFrame(row,columns = ['Country/Region','Date','Estimated '+y_axis] )
        # print(copy)
        estimator = estimator.append(copy,ignore_index=True)
    print(estimator)

    row = []
    for country in ordered_countries:
        estimate = estimator[estimator['Country/Region']==country + " Estimated"]['Estimated '+y_axis].max()
        current = selected_df[selected_df['Country/Region']==country][y_axis].max()
        diff = estimate - current
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

    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)



    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
