class EvenStream(object):
    def __init__(self):
        self.current = 0

    def get_next(self):
        to_return = self.current
        self.current += 2
        return to_return

class OddStream(object):
    def __init__(self):
        self.current = 1

    def get_next(self):
        to_return = self.current
        self.current += 2
        return to_return

def print_from_stream(n, stream=EvenStream()):
    for i in range(n):
        print(stream.get_next(),file=open("vysledek.txt","a"), end="\n")

answers = [line.rsplit() for line in open("xxx.txt", "r")]
file =[line.rsplit() for line in open("xxx.txt", "r")]

for stream_name,n in file:
    print(stream_name,n)
    n = int(n)
    if stream_name == "even":
        print_from_stream(n)

    else:
        print_from_stream(n, OddStream())



    #dbc.Col(
    #    dcc.Dropdown(id="month",
    #                   options=[
    #                       {"label": "January", "value":1},
    #                       {"label": "February", "value":2},
    #                       {"label": "March", "value":3},
    #                       {"label": "April", "value":4},
    #                       {"label": "May", "value":5},
    #                       {"label": "June", "value":6},
    #                       {"label": "July", "value":7},
    #                       {"label": "August", "value":8},
    #                       {"label": "September", "value":9},
    #                       {"label": "October", "value":10},
    #                       {"label": "November", "value":11},
    #                       {"label": "December", "value":12}],
    #                   multi=True,
    #                   value=int(datetime.now().month),
    #                   placeholder="Select a month",
    #                ), width={'size':2, 'offset':1, 'order':2})




#,dbc.Row([
#       dbc.Col([
#            html.P("Select a Client: ",
#                   style={"textDecoration": "underline",
#                             "font-size":24 px}),
#            dcc.Checklist(id='my-checklist', value=['food', 'school','flat','others'],
#                          options=[
#                                   {'label':"Food", 'value':"food"}
#                                   {'label':"School", 'value':"school"}
#                                   {'label':"Home", 'value':"flat"}
#                                   {'label':"Others", 'value':"others"}
#                               ],
#                         labelClassName="mr-4"),
#           dcc.Graph(id='my-hist'),
#       ], width={'size':5, 'offset':1},
#          #xs=12, sm=12, md=12, lg=5, xl=5
#       ),
#   ], align="center")  # Vertical: start, center, end
#






def month_now(month=datetime.now().month):
    #month_s = datetime.now().strftime("%B")
    if int(month) in [1,3,5,7,8,10,12]:
        return range(1,32)
    elif int(month) == 2 :
        return range(1,29)
    else:
        return range(1,31)


 #   yearly_carts = [cart for cart in non_filtred_carts if cart.date.split(".")[2]==str(datetime.now().year)]
 #   monthly_carts = [cart for cart in yearly_carts if cart.date.split(".")[1]==str(datetime.now().month)]
 #   daily_carts = [cart for cart in monthly_carts if cart.date.split(".")[0]==str(datetime.now().day)]
 #   spent_daily,spent_avg,tmp=[],[],0
 #   for day in month_now():
 #       todays_carts = list(filter(lambda x: int(x.date.split(".")[0]) == day ,carts))
 #       todays_spend_temp = sum((cart.prize) for cart in todays_carts)
 #       spent_daily+=[todays_spend_temp]
 #       tmp+=todays_spend_temp
 #       spent_avg +=[tmp//(day+1)]
#
df = DataFrame(list(Cart.objects.all().values()))


#TOTO JE ZDROJAK Z GRAPHS2 BYVALEHO

appka.layout =  html.Div(
        className="row", children=[

            html.Div(className='six columns', children=[

                dcc.Dropdown(id="select_month", options=[
                    {"label": "January", "value":1},
                    {"label": "February", "value":2},
                    {"label": "March", "value":3},
                    {"label": "April", "value":4},
                    {"label": "May", "value":5},
                    {"label": "June", "value":6},
                    {"label": "July", "value":7},
                    {"label": "August", "value":8},
                    {"label": "September", "value":9},
                    {"label": "October", "value":10},
                    {"label": "November", "value":11},
                    {"label": "December", "value":12}],
                    multi=False,
                    value=str(datetime.now().month),
                    style={"width":"50%"},
                    placeholder="Select a month")]),

            html.Div(className='six columns', children=[

                dcc.Dropdown(id="select_year", 
                    options=[
                        {"label": "2020", "value":2020},
                        {"label": "2021", "value":2021},
                        {"label": "2022", "value":2022}],
                    multi=False,
                    value=str(datetime.now().year),
                    style={"width":"50%"},
                    placeholder="Select a year")]),

            html.Div(className="columns", children=[
                dcc.Slider(id='slider_days',
                            min=1,
                            value=30,
                            step=1,
                            updatemode='drag',
                            included=True)])], 

            style=dict(display='flex'))





@appka.callback([Output('month_spends', 'figure'),
    Output('slider_days','max'),
    Output('slider_days','marks')],
    Input('select_year', 'value'))

def display_value(year,*args,**kwargs):
    month = kwargs["django_plotly_dash"]["month"]
    days = kwargs["django_plotly_dash"]["days"]
    print("Tento mesic je ",month,year,days)
    user = kwargs["user"]
    first_day=int(f"{year}{month}00")
    last_day=int(f"{year}{month}{days}")
    person = Person.objects.get(user=user)

    df_filtered = (((df["compare_date"] > first_day) & (df["compare_date"] < last_day)) & (df["customer_id"] == person.id))

    
    print(df_filtered,first_day,last_day, len(df))
    fig = px.bar(df[df_filtered], x="date", y="prize", color="item_amount",hover_data=["prize","item_amount"],labels={"prize":"Prize of a bill","date":"Date","place":"Place","item_amount":"Amount of items","prize":"Prize"}, template="plotly_dark",text="prize",hover_name="place")
    #container = "Days of the {}".format(datetime.now().strftime("%B"))

    max_slide = max(month_now(month))
    max_mark = {i: '{}'.format(i) for i in range(1,max_slide)}

    return fig, max_slide, max_mark


@appka.callback([Output('month_spends', 'figure'),
    Output('slider_days','max'),
    Output('slider_days','marks')],[
    Input('select_month', 'value'),
    Input('select_year', 'value'),
    Input('slider_days', 'value')])
def display_value(month,year,days,*args,**kwargs):
    print("Tento mesic je ",month,year,days)
    first_day=int(f"{year}{month}00")
    last_day=int(f"{year}{month}{days}")
    user = kwargs["user"]
    person = Person.objects.get(user=user)
    df_filtered = (((df["compare_date"] > first_day) & (df["compare_date"] < last_day)) & (df["customer_id"] == person.id))

        
    print(df_filtered,first_day,last_day, len(df))
    fig = px.bar(df[df_filtered], x="date", y="prize", color="item_amount",hover_data=["prize","item_amount"],labels={"prize":"Prize of a bill","date":"Date","place":"Place","item_amount":"Amount of items","prize":"Prize"}, template="plotly_dark",text="prize",hover_name="place")
    #container = "Days of the {}".format(datetime.now().strftime("%B"))

    max_slide = max(month_now(month))
    max_mark = {i: '{}'.format(i) for i in range(1,max_slide)}
    

    return fig, max_slide, max_mark