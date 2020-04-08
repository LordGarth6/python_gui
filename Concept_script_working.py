import os
import pandas as pd
import matplotlib.pyplot as plt

def main():

	print ("Cleaning file for proper use\n")
	import io
	with io.open('FGT_data.log', 'r') as f:
		text = f.read()
	with io.open('FGT_data.log', 'w', encoding='utf8') as f:
		f.write(text)
	os.system('echo F|xcopy /y /F %0\..\FGT_data.log %0\..\FGT_data.csv')
	os.system('echo Date,Event,Value, Unit,0,1,2,3,4 > data.csv')
	os.system('type FGT_data.csv >> data.csv')
	os.system('echo F|xcopy /y /F %0\..\data.csv %0\..\FGT_data.csv')
	
	datascrub = ['Oxygen ', 'CO ', 'Particulate', 'ID fan Speed', 'Bag differential','Comms fail',
			'Reagent feed rate change', 'A cremator has started', 'Pre-warmed']
	datakeep = ['Boiler water inlet ','Bag inlet ','Stack temp ','Cooler 1 water outlet ',
			'Cooler 2 water outlet ','Cooler 3 water outlet ']
	bwi = pd.DataFrame()
	bi = pd.DataFrame()
	st = pd.DataFrame()
	c1wo = pd.DataFrame()
	c2wo = pd.DataFrame()
	c3wo = pd.DataFrame()
	totaldata= pd.DataFrame()
	preheating = pd.DataFrame()
	preheated = pd.DataFrame()
	dataframed = [bwi,bi,st,c1wo,c2wo,c3wo]

	print ("importing FGT_data.csv\n")
	df = pd.read_csv(
		'FGT_data.csv',low_memory=False,
		header=0,index_col=False,
		)
	df.columns = ['Date','Event','Value', 'Unit','0','1','2','3','4']

	print ("cleaning up data\n")
	baddata=(df[df.Date.str.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"))==False])
	if (not baddata.empty):
		baddata.to_csv('baddata.csv', index=False)
	df=(df[df.Date.str.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"))==True])
	df['Date']= pd.to_datetime(df['Date'])
	df = df.drop(df.columns[[4,5,6,7,8]], axis=1)

	print ("Getting years worth of data\n")
	dates = df['Date'].iloc[-1]
	dates2 = dates - pd.DateOffset(years=1)
	mask = (df['Date'] > dates2) & (df['Date'] <= dates)
	df = df.loc[mask]	

	preheatmaskdf = df
	preheatmaskdf = preheatmaskdf.loc[preheatmaskdf['Event']=='Pre-heated']
	preheatmaskdf.reset_index(inplace = True)
	preheatmaskdf = preheatmaskdf.drop(preheatmaskdf.columns[[4]],axis=1)
	preheatmaskdf['Value'] = preheatmaskdf['Value'].astype(int)
	preheatmaskdf['NxV']=preheatmaskdf['Value'].shift(-1)
	preheatmaskdf['NxI']=preheatmaskdf['index'].shift(-1)
	preheatmaskdf['Heated']=preheatmaskdf['Value']-preheatmaskdf['NxV']
	preheatmaskdf = preheatmaskdf.loc[(preheatmaskdf['Heated']==1)]
	preheatmaskdf.reset_index(drop = True,inplace = True)
	preheatmaskdf = preheatmaskdf.drop(preheatmaskdf.columns[[1,2,3,4,6]], axis=1)
	
	num_coolers="0"
	
	tempc3_df=df[df['Event'].str.contains("Cooler 3 water outlet")]
	tempc3_df=tempc3_df[['Value']]
	tempc3_df=tempc3_df.apply(pd.to_numeric)
	test = (tempc3_df.Value.nunique() == 1)
	tempc3_df.drop(tempc3_df.loc[tempc3_df['Value']==0].index, inplace=True)
	if(tempc3_df.empty or test):
		tempc2_df=df[df['Event'].str.contains("Cooler 2 water outlet")]
		tempc2_df=tempc2_df[['Value']]
		tempc2_df=tempc2_df.apply(pd.to_numeric)
		test = (tempc2_df.Value.nunique() == 1)
		tempc2_df.drop(tempc2_df.loc[tempc2_df['Value']==0].index, inplace=True)
		if(tempc2_df.empty or test):
			tempc1_df=df[df['Event'].str.contains("Cooler 1 water outlet")]
			tempc1_df=tempc1_df[['Value']]
			tempc1_df=tempc1_df.apply(pd.to_numeric)
			test = (tempc1_df.Value.nunique() != 1)
			tempc1_df.drop(tempc1_df.loc[tempc1_df['Value']==0].index, inplace=True)
			if(not tempc1_df.empty or test):
				num_coolers="1"
		else:
			num_coolers= "2"
	else:
		num_coolers="3"

	print ("Removing unneeded data\n")
	for x in range(len(datascrub)):
		df = df[df.Event != datascrub[x]]

	if num_coolers == "2":
		df = df[df.Event != datakeep[5]]
	elif num_coolers == "3":
		df = df[df.Event != datakeep[4]]
		df = df[df.Event != datakeep[5]]
	elif num_coolers == "0":
		df = df[df.Event != datakeep[3]]
		df = df[df.Event != datakeep[4]]
		df = df[df.Event != datakeep[5]]
		
	if num_coolers == "1":
		y=4
	elif num_coolers == "2":
		y=5
	elif num_coolers == "3":
		y=6
	else:
		y=3

	print ("Scrubbing for preheated data\n")
	for x in range(len(preheatmaskdf)):
		preheatmask = ((df.index > preheatmaskdf.iloc[x,0]) & (df.index < preheatmaskdf.iloc[x,1]))
		phtemp=df.loc[preheatmask]
		preheating = preheating.append(phtemp,ignore_index=True)

	print ("Plotting preheated data\n")
	for x in range(y):
		dataframed[x] = preheating[preheating.Event == datakeep[x]]
		temp=dataframed[x]
		name = str(temp['Event'].iloc[0]) + ' ' + str(temp['Unit'].iloc[0])
		dataframed[x].columns = ['Date','Event',name, 'Unit']
		dataframed[x] = dataframed[x].drop(dataframed[x].columns[[1,3]], axis=1)
		temp2=dataframed[x].set_index('Date')
		temp2=temp2.apply(pd.to_numeric)
		temp2.plot(figsize=(32, 18),linestyle='-',marker='.', markersize=10,markerfacecolor='black', title=('Temperature '+ name + ' Preheat Data'))
		plt.ylabel(str(name))
		plt.savefig(name + '_preheated.png')
		temp=dataframed[x]
		if x == 0:
			preheated['Date'] = temp['Date']
		try:
			preheated[name] = temp[name].values
		except:
			try:
				preheated[name] = temp.loc[temp[name]]
			except:
				preheated[name] = "Error

	print ("Plotting total data\n")
	for x in range(y):
		dataframed[x] = df[df.Event == datakeep[x]]
		temp=dataframed[x]
		name = str(temp['Event'].iloc[0]) + ' ' + str(temp['Unit'].iloc[0])
		dataframed[x].columns = ['Date','Event',name, 'Unit']
		dataframed[x] = dataframed[x].drop(dataframed[x].columns[[1,3]], axis=1)
		temp2=dataframed[x].set_index('Date')
		temp2=temp2.apply(pd.to_numeric)
		temp2.plot(figsize=(32, 18),linestyle='-',marker='.', markersize=10,markerfacecolor='black', title=('Temperature '+ name + ' Total Data'))
		plt.ylabel(str(name))
		plt.savefig(name + '_total.png')
		temp=dataframed[x]
		if x == 0:
			totaldata['Date'] = temp['Date']
		try:
			totaldata[name] = temp[name].values
		except:
			try:
				totaldata[name] = temp.loc[temp[name]]
			except:
				totaldata[name] = "Error"
		
	totaldata = totaldata.set_index('Date')
	preheated = preheated.set_index('Date')
	totaldata.reset_index(inplace = True)
	preheated.reset_index(inplace = True)
	
	print ("Outputing data\n")
	preheated.to_csv('FGT_data_PH.csv', index=False)
	totaldata.to_csv('FGT_data_T.csv', index=False)	

	print ("DONE!\n")

if __name__ == '__main__':
	main()
