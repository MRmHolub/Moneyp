import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
from django_plotly_dash import DjangoDash
from datetime import datetime
from main.models import *
import plotly.express as px
from pandas import DataFrame
import dash
import dash_bootstrap_components as dbc

mesice =[{1:'January'},{2:'February'},{3:'March'},{4:'April'},{5:'May'},{6:'June'},{7:'July'},{8:'August'},{9:'September'},{10:'October'},{11:'November'},{12:'December'}]

df = DataFrame(list(Cart.objects.all().values()))
print(df)

app = DjangoDash('graphs2', external_stylesheets=[dbc.themes.SLATE],
    #meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}], #FOR MOBILE COMPATIBILITY
    suppress_callback_exceptions=True)


app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("Monthly Activity",
                        className='text-center bg-dark text-danger mb-4'),
                width=12)
    ),

    dbc.Row(
        dbc.Col([
            dcc.Dropdown(id='year',
                         multi=False,
                         value=2021,
                         options=[
                            {"label": "2020", "value":2020},
                            {"label": "2021", "value":2021},
                            {"label": "2022", "value":2022}],
                        ),
                ], width={'size':2, 'offset':1, 'order':1},style={"color":"red","margin":"1%","margin-left":"10%"})

        #here used to be another dropdown
        ,
        no_gutters=True, justify='start'),

    dbc.Row(    
        dbc.Col(           
            dcc.Graph(id='main-fig'),style={'display': 'block'}, width={'size':11, 'offset':1})),

    dbc.Row(
        dbc.Col(
            dcc.Slider(id="main-slider",
                        min=1,
                        max=12,
                        step=1,
                        value=12,
                        marks=[dict(i=i) for i in range(1,13)])
                        #included=True,
                        #disabled=True,
                        #tooltip={"placement": "bottom", "always_visible": True})

            ,width={'size':11, 'offset':1},style={"color":"red","margin":"1%","margin-left":"9%"})),

    dbc.Row(
        dbc.Col([
            html.P("Select a Client: ",
                   style={"textDecoration": "underline",
                             "font-size":24}),
            dcc.Checklist(id='my-checklist', value=['food', 'school','flat','others'],
                          options=[
                                   {'label':"Food", 'value':"food"},
                                   {'label':"School", 'value':"school"},
                                   {'label':"Home", 'value':"flat"},
                                   {'label':"Others", 'value':"others"}
                               ],
                         labelClassName="mr-4"),
           dcc.Graph(id='my-hist')], width={'size':5, 'offset':1}))],

    fluid=True, style={'background-color':'transparent'})




@app.callback(Output('main-fig', 'figure'),
              [Input('year', 'value'),
              Input('main-slider','value')])
def display_value(year,month,*args,**kwargs):

    #print("Tento mesic je ",month,year,days)
    user = kwargs["user"]
    person = Person.objects.get(user=user)

    first_day=(f"{year}{month}00")
    last_day=(f"{year}{month}99")


    df_filtered = (((df["compare_date"] > first_day) & (df["compare_date"] < last_day)) & (df["customer_id"] == person.id))

    title = "Money spend in: "+mesice[month-1][month]
    fig = px.bar(df[df_filtered], x="date", y="prize", color="item_amount",title=title,
                                  hover_data=["prize","item_amount"],
                                  labels={"prize":"Prize of a bill","date":"Date","place":"Place","item_amount":"Amount of items","prize":"Prize"},
                                  template="plotly_dark",text="prize",hover_name="place")

    
    fig.update_traces(textposition='outside')

    fig.update_layout(title={
            'text': "Money spend in: "+mesice[month-1][month],
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font':{"family":"Courier New, monospace","size":26, "color":"Lime"}})
    return fig