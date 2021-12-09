from django.shortcuts import render, redirect
from .models import *
from .home_views import loged_decorator
from datetime import datetime
from plotly.offline import plot
import plotly.express as px
from pandas import DataFrame
from matplotlib import pyplot as plt
from .plots import *
#fc4f30
#statistics mean, median, multimode 
#mnozstvi objeveni polozek v jednotlivych nakupech budeme hledat pres import collections Counter
#plt.pie pro zobrazeni jakou cast nakupu tvori ktery klient, s tim ze bude scalable na mesic, den i all time

def month_now(month=datetime.now().month):
    #month_s = datetime.now().strftime("%B")
    if int(month) in [1,3,5,7,8,10,12]:
        return range(1,32)
    elif int(month) == 2 :
        return range(1,29)
    else:
        return range(1,31)

#@loged_decorator
def graphs(response):

	customer = Customer.objects.get(id=response.session["customer"])
	print(customer,"'s graphs accessed")
	curr_time=datetime.now()
#non_filtred_carts = Cart.objects.filter(customer=customer)
	#yearly_carts = [cart for cart in non_filtred_carts if int(cart.date.split(".")[2])==curr_time.year]
	#monthly_carts = [cart for cart in yearly_carts if int(cart.date.split(".")[1])==curr_time.month]
	#daily_carts = [cart for cart in monthly_carts if int(cart.date.split(".")[0])==curr_time.day]
	
	#dfm=DataFrame(sorted([it.json_serialize() for it in monthly_carts], key=lambda x: x["compare_date"]))
	#dfd=DataFrame(sorted([it.json_serialize() for it in daily_carts], key=lambda x: x["compare_date"]))
	#dfy=DataFrame(sorted([it.json_serialize() for it in yearly_carts], key=lambda x: x["compare_date"]))
	#dfa=DataFrame(sorted([it.json_serialize() for it in non_filtred_carts], key=lambda x: x["compare_date"]))
	

	df = DataFrame(list(Cart.objects.filter(customer=customer).values()))
	#print(df)
	fig = px.bar(df, x="date", y="prize", color="item_amount",
		hover_data=["prize","item_amount"],
		labels={"prize":"Prize of a bill","date":"Date","place":"Place","item_amount":"Amount of items","prize":"Prize"}, height=700, template="plotly_dark", width=1400,text="prize",hover_name="place")

	fig.update_traces(textposition='outside')

	fig.update_layout(title={
	        'text': "Plot Title",
	        'y':0.95,
	        'x':0.5,
	        'xanchor': 'center',
	        'yanchor': 'top',
	        'font':{"family":"Courier New, monospace","size":35, "color":"Lime"}})

#
#	fig.update_layout(updatemenus=[
#	        dict(
#	            buttons=list([
#	                dict(args=[{"colorscale":"Viridis","visible":[True,False,False,False]}],label="Viridis",method="update"),
#	                dict(args=[{"colorscale":"Cividis","visible":[False,True,False,False]}],label="Cividis",method="update"),
#	                dict(args=[{"colorscale":"Blues","visible":[False,False,True,False]}],label="Blues",method="update"),
#	                dict(args=[{"colorscale":"Greens","visible":[False,False,False,True]}],label="Greens",method="update")]),
#	            direction="down",
#	            pad={"r": 10, "t": 10},
#	            x=0.1,
#	            xanchor="left",
#	            y=1.08,
#	            yanchor="top"),
#
#	        dict(
#	            buttons=list([
#	            	dict(args=["reversescale", False],label="False",method="update"),
#	            	dict(args=["reversescale", True],label="True",method="update")]),
#	            direction="down",
#	            pad={"r": 10, "t": 10},
#	            x=0.37,
#	            xanchor="left",
#	            y=1.08,
#	            yanchor="top")])
#
#	        dict(
#	            buttons=list([
#	            	dict(args=[{"data":dfm}],label="Monthly",method="update"),
#	            	dict(args=[{"data": dfd}],label="Daily",method="update"),
#	                dict(args=[{"data": dfy}],label="Yearly",method="update"),
#	                dict(args=[{"data": dfa}],label="All Time",method="update")]),
#	            direction="down",
#	            pad={"r": 10, "t": 10},
#	            x=0.58,
#	            xanchor="left",
#	            y=1.08,
#	            yanchor="top"),])
#
#	fig.update_layout(
#	    annotations=[
#	        dict(text="Colorscale", x=0, xref="paper", y=1.06, yref="paper",
#	                             align="left", showarrow=False),
#	        dict(text="Reverse<br>Colorscale", x=0.25, xref="paper", y=1.07,
#	                             yref="paper", showarrow=False)#,
#	       # dict(text="Time Intervals", x=0.54, xref="paper", y=1.06, yref="paper",
#	        #                     showarrow=False)
#	    ])
#
#  layout = {
#     'title': 'Title of the figure',
#     'yaxis_title'#: 'Y',
#     'width': 560,
#
#	graphs=[fig]
	plot_div = plot(fig, output_type='div', include_plotlyjs=False)


	#colors = ['#333F44', '#37AA9C', '#94F3E4']






	
	
	context= {'plot1': plot_div}#, "plot2":graph}

#	
#	dfc = {'year':df_y, 'month':df_m}
#
#	# set index
#	for df in dfc.keys():
#	    dfc[df].set_index('x', inplace=True)
#
#
#	# plotly start 
#	figr = go.Figure()
#
#	buttons=[]
#
#	# one trace for each column per dataframe: AI and RANDOM
#	for df in dfc.keys():
#	    figr.add_trace(go.Scatter(x=dfc[df].index,
#	                             y=dfc[df]['y'],
#	                             visible=True,
#	                             marker=dict(size=12, line=dict(width=2)),
#	                             marker_symbol = 'diamond',
#	                             name=df
#	                  )
#	             )
#
#
#	# some line settings for fun
#	lines = [dict(color='royalblue', width=2, dash='dot'), dict(color='firebrick', width=1, dash='dash')]
#	markers = [dict(size=12, line=dict(width=2)), dict(size=12, line=dict(width=2))]
#
#	# create traces for each color: 
#	# build argVals for buttons and create buttons
#	for i, df in enumerate(dfc.keys()):
#	    args_y = []
#	    args_x = []
#	    for col in dfc[df]:
#	        args_y.append(dfc[df][col].values)
#	        args_x.append(dfc[df].index)
#	    argVals = [ {'y':args_y, 'x':args_x,
#	                 'marker':markers[i], 'line': lines[i]}]
#
#	    buttons.append(dict(method='update',
#	                        label=df,
#	                        visible=True,
#	                        args=argVals))
#
#	updatemenu=[]
#	updatemenu.append({})
#	updatemenu[0]['buttons']=buttons
#	updatemenu[0]['direction']='down'
#	updatemenu[0]['showactive']=True
#
#
#	figr.update_layout(showlegend=False, updatemenus=updatemenu)
#	figr.show()
	return render(response, 'main/graphs.html', context)


@loged_decorator
def wallet(response):
	customer = Customer.objects.get(id=response.session["customer"])
	print(customer,"'s wallet accessed")
	if response.method == "POST":
		form = customer.set_addmoney.create(sponsor=response.POST.get("sponsor"), amount=response.POST.get("amount"))
		finish_form(response, form)
	curr_time= datetime.now()
	non_filtred_carts = Cart.objects.filter(customer=customer)
	yearly_carts = [cart for cart in non_filtred_carts if int(cart.date.split(".")[2])==int(curr_time.year)]
	monthly_carts = [cart for cart in yearly_carts if int(cart.date.split(".")[1])==int(curr_time.month)]
	daily_carts = [cart for cart in monthly_carts if int(cart.date.split(".")[0])==int(curr_time.day)]
	print(yearly_carts)
	d_bill=customer.spend(carts=daily_carts)
	m_bill=customer.spend(carts=monthly_carts)
	#y_bill=customer.spend(carts=yearly_carts)
	alltime_bill=customer.money_spend
	

	graph=make_plot(carts=monthly_carts)
	state=sum([obj.amount for obj in AddMoney.objects.filter(customer=customer)]) - int(customer.money_spend)
	
	context={"state":state, "graph":graph, "m_bill":m_bill, "d_bill":d_bill, "alltime_bill":alltime_bill}
	return render(response, "main/wallet.html", context)
#response.person



def make_plot(carts):
	plt.style.use("dark_background")
	fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1, tight_layout=True)
	fig.set_size_inches(12,7, forward=True)
	#automatically adjusts subplot params so that the subplot(s) fits in to the figure area. It only checks the extents of ticklabels, axis labels, and titles. An alternative to tight_layout is constrained_layout.
	X = month_now()
	spent_daily,spent_avg,tmp=[],[],0
	for day in X:
		todays_carts = list(filter(lambda x: int(x.date.split(".")[0]) == day ,carts))
		todays_spend_temp = sum((cart.prize) for cart in todays_carts)
		spent_daily+=[todays_spend_temp]
		tmp+=todays_spend_temp
		spent_avg +=[tmp//(day+1)]
		#if day==int(datetime.now().day):
		#	todays_spend = todays_spend_temp




	ax1 = m_spend_stack(ax=ax1, plot="stack", avg=spent_avg, mainly=spent_daily, X=X)
	ax2 = m_spend_stack(ax=ax2, plot="bar", avg=spent_avg, mainly=spent_daily, X=X) 

	data = plot_end(fig=fig)
	
	return data
	
@loged_decorator
def dash_plot(response):
	response.session["django_plotly_dash"]="Nič"
	return render(response,"main/dash.html",{})
