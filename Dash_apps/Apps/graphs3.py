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

app = DjangoDash('graphs2', external_stylesheets=[dbc.themes.DARKLY],
	meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}], #FOR MOBILE COMPATIBILITY
	suppress_callback_exceptions=True)


app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("Monthly Activity",
                        className='text-center text-dark mb-4'),
                width=12)
    ),

    dbc.Row(
        dbc.Col([
            dcc.Dropdown(id='year',
            			 multi=True,
            			 value=2021,
                         options=[
                         	{"label": "2020", "value":2020},
	                        {"label": "2021", "value":2021},
	                        {"label": "2022", "value":2022}],
	                    ),
            	], width={'size':2, 'offset':1, 'order':1},)

        #here used to be another dropdown
        ,
		no_gutters=True, justify='start'),

	dbc.Row(	
		dbc.Col(	       
            dcc.Graph(id='main-fig'), width={'size':11, 'offset':1})),

	dbc.Row(
		dbc.Col(
			dcc.Slider(id="main-slider",
				 		min=1,
        				max=12,
        				step=1,
        				value=12,
        				marks=[dict(i,i) for i in range(1,13)])
        				#included=True,
        				#disabled=True,
        				#tooltip={"placement": "bottom", "always_visible": True})

			,width={'size':11, 'offset':1}))
# here used to be a checklist
], fluid=True)




@app.callback(Output('main-fig', 'figure'),
              [Input('year', 'value'),
              Input('main-slider','value')])
def display_value(year,month,*args,**kwargs):

    #print("Tento mesic je ",month,year,days)
    user = kwargs["user"]
    person = Person.objects.get(user=user)
    
    if month>=10:
    	first_day=int(f"{year}{month}00")
    	last_day=int(f"{year}{month}99")
    else:
    	first_day=int(f"{year}0{month}00")
    	last_day=int(f"{year}0{month}99")

    df_filtered = (((df["compare_date"] > first_day) & (df["compare_date"] < last_day)) & (df["customer_id"] == person.id))

    title = "Money spend in: "+mesice[month]
    fig = px.bar(df[df_filtered], x="date", y="prize", color="item_amount",title=title,
    							  hover_data=["prize","item_amount"],
    							  labels={"prize":"Prize of a bill","date":"Date","place":"Place","item_amount":"Amount of items","prize":"Prize"},
    							  template="plotly_dark",text="prize",hover_name="place")

    return fig


#@app.callback(Output('main-fig', 'figure'),
#              [Input('year', 'value'),
#              Input('month','value')])
#def display_value(year,*args,**kwargs):
#
#    #print("Tento mesic je ",month,year,days)
#    user = kwargs["user"]
#    if month>=10:
#    	first_day=int(f"{year}{month}00")
#    	last_day=int(f"{year}{month}99")
#    else:
#    	first_day=int(f"{year}0{month}00")
#    	last_day=int(f"{year}0{month}99")
#
#    person = Person.objects.get(user=user)
#    
#    df_filtered = (((df["compare_date"] > first_day) & (df["compare_date"] < last_day)) & (df["customer_id"] == person.id))
#
#    print(df_filtered,first_day,last_day, len(df))
#    fig = px.bar(df[df_filtered], x="date", y="prize", color="item_amount",hover_data=["prize","item_amount"],labels={"prize":"Prize of a bill","date":"Date","place":"Place","item_amount":"Amount of items","prize":"Prize"}, template="plotly_dark",text="prize",hover_name="place")
#    #container = "Days of the {}".format(datetime.now().strftime("%B"))
#
#    max_slide = max(month_now(month))
#    max_mark = {i: '{}'.format(i) for i in range(1,max_slide)}
#
#    return fig, max_slide, max_mark

