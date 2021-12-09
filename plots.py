from matplotlib import pyplot as plt
from datetime import datetime
from io import StringIO

def month_now():
	month = datetime.now().month
	month_s = datetime.now().strftime("%B")
	if int(month) in [1,3,5,7,8,10,12]:
		return list(range(1,32))
	elif int(month) == 2 :
		return list(range(1,29))
	else:
		return list(range(1,31))



def cart_serializer(period):
	"""Pass query set of carts of some tiem period get the data"""
	result_list,result=[],{}
	for i in range(len(period)):	
		x=period[i].cart.replace("[{","").replace("}]","").replace("'","").replace(" ","").replace("\n","")	
		cart_items=x.split("\r")
		#print(i,"\n\nCart items are: \n",cart_items)
		for index,cart_item in enumerate(cart_items):
			atributes=cart_item.split(",")
			#print("\nAtribbutes\n",atributes)
			for pair in atributes:
				key_value=pair.split(":")
				result[key_value[0]] = key_value[1]
				#print(pair, key_value, result)
			return result

def m_spend_stack(ax, plot, avg, mainly, X):
	#print("\nDaily spends: ",mainly,"\n Average: ",avg)
	ax.set_facecolor((0.25,0.25,0.25))
	ax.set_alpha(0.7)

	if plot == "plot":
		ax.plot(X,mainly, label="Daily spends", color=["m"], alpha=1, zorder=2, lw=1)
		ax.stackplot(X,avg, labels="Average", colors="#fc4f30", alpha=0.7, zorder=1)
		ax.set_title("Average vs Monthly Balance (Stackplot)",pad=20,color="black",fontsize=20)

	elif plot == "bar":
		ax.bar(X,mainly, label="Daily spends",color="lime", alpha=1, zorder=1,width=0.7575, align="center", ec="black", linewidth=2)
		#ax.bar(X,avg, label="Average", color="white", alpha=0.8, zorder=2, width=0.5, align="center")
		ax.plot(X,avg, label="Average", color="white", alpha=1, zorder=2, lw=2)
		for i in X:
			if mainly[i-1]>0:
				ax.annotate('{val}'.format(val=mainly[i-1]),xy=(i,mainly[i-1]),ha="center", va="bottom")
	
	#elif plot == "hist":
	#	ax.hist(mainly,bins=X, label="Daily spends", color=["m"], alpha=0.7, zorder=1, density=True)
	#	ax.hist(avg,bins=X, label="Average", color="#fc4f30", alpha=0.7,zorder=2, density=True)
	#	ax.set_title("Average vs Monthly Balance (Histogram)",pad=20,color="black",fontsize=20)
	
	else:
		ax.stackplot(X,mainly, colors="#ff424a", alpha=0.6, zorder=1)
		ax.plot(X,avg, label="Average", color="white", alpha=1, zorder=2, lw=2)
		ax.set_title("Average vs Monthly Balance (Stackplot)",pad=20,color="black",fontsize=20)
		for i in X:
			if mainly[i-1]>0:
				#print(mainly[i],i)
				ax.annotate('{val}'.format(val=mainly[i-1]),xy=(i,mainly[i-1]),ha="center", va="bottom")

	ax.set_xticks(X)
	ax.set_yticks(list(range(0,1000,100)))
	ax.set_xlabel("Days of the {}".format(datetime.now().strftime("%B")), color="red",fontsize=16)
	ax.set_ylabel("Spent (CZK) ",color="red",fontsize=16)
	ax.grid(axis="y",color="black")
	ax.margins(0)
	ax.legend(loc="upper right") #or ax.set (xlabel =....,title=...)
	ax.tick_params(axis="y",color="yellow", labelcolor="red", grid_lw=1)
	ax.tick_params(axis="x",color="yellow", labelcolor="black", grid_lw=1)
	for key in ax.spines.keys():
		ax.spines[key].set_linewidth(1)
	return ax

def plot_end(fig):

	fig.patch.set_visible(False)
	imgdata=StringIO()
	fig.savefig(imgdata, format="svg", dpi=100)
	imgdata.seek(0)
	data = imgdata.getvalue()
	fig.savefig('main/static/main/myplot.png', dpi=100)


	#for i in range(len(X)):
	#		if mainly[i]>0:
	#			plt.text(i, mainly[i],str(mainly[i]), ha="center", va="bottom", zorder=3, color="white")


