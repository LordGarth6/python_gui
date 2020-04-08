import PySimpleGUI as sg
import os
import pandas as pd
import matplotlib.pyplot as plt
import io

selection_data = ['Oxygen', 'CO', 'Particulate', 'ID fan Speed', 'Bag differential','Comms fail','Reagent feed rate change',
'A cremator has started', 'Pre-warmed','Boiler water inlet','Boiler water outlet','Bag inlet','Stack temp','Cooler 1 water outlet',
'Cooler 2 water outlet','Cooler 3 water outlet','Pre-heated']
selected_data = []
datafile = "FGT_data.log"
paramfile = "FGT_Param_Record.log"
datafilepath = ""
paramfilepath = ""
barmax = 100
window = ""
def win():
	global selected_data
	global selection_data
	global datafile
	global paramfile
	global datafilepath
	global paramfilepath
	global window
	global barmax
	selection_data.sort()

	sg.theme('DarkBrown4')
	sg.SetOptions(element_padding=(0,0))
	
	colleft = [[sg.Listbox(values='',key='_OPTIONS_',size=(20,20))]]
	colcen = [[sg.Button('Add >>')],
		   [sg.Button('<< Remove')]]
	colright = [[sg.Listbox(values='',key='_CHOSEN_',size=(20,20))]]

	c2l= [[sg.Button('Data Log'),sg.Button('Parameter Log'), sg.Exit()]]
	c2r= [
		[sg.ProgressBar(barmax, orientation='h', size=(18, 4), key='_PROGRESSBAR_', pad=(0,3))],
		[sg.ProgressBar(barmax, orientation='h', size=(18, 4), key='_PROGRESSBAR2_', pad=(0,3))],
		[sg.ProgressBar(barmax, orientation='h', size=(18, 4), key='_PROGRESSBAR3_', pad=(0,3))]
	      ]

	layout =[
			[sg.Input('Folder',enable_events=True,key='_INPUT_PATH_'), sg.FolderBrowse()],
			[sg.Column(colleft),sg.Column(colcen),sg.Column(colright)],
			[sg.Text('-'*112)],
			[sg.Column(c2l),sg.VerticalSeparator(pad=(5,5)),sg.Column(c2r)],
			[sg.Text('-'*112)],
			[sg.Spin([i for i in range(1,100)], initial_value=1),sg.Radio('Year(s)', "RADIO1", default=True),sg.Radio('Month(s)', "RADIO1"),sg.Radio('Weeks(s)', "RADIO1"),sg.Radio('Days(s)', "RADIO1"),sg.Radio('Hour(s)', "RADIO1")],
			[]
		]      

	window = sg.Window('Simple data entry window',no_titlebar=False, grab_anywhere=False, keep_on_top=True).Layout(layout).Finalize()
	window.FindElement('_OPTIONS_').Update(values=selection_data)
	window.Refresh()
	button, values = window.Read()
	window['_PROGRESSBAR_'].UpdateBar(0)
	while True:
		event, values = window.Read()
		if event in (None,'Add >>'):
			try: 
				temp = values['_OPTIONS_'][0]
				if temp in selected_data:
					temp = None
				else:
					selected_data.append(temp)
					window['_CHOSEN_'](values=selected_data)
			except:
				None
			window.Refresh()
					     
		if event in (None,'<< Remove'):
			try:
				temp = values['_CHOSEN_'][0]
				if temp in selected_data:
					selected_data.remove(temp)
					window['_CHOSEN_'](values=selected_data)
				else:
					temp = None
			except:
				None 
			window.Refresh()
					     
		if event in (None,'Exit'):
			listprint(selected_data)
			window.Close()
			break
		if event in (None,'Data Log'):
			dtp_temp = values['_INPUT_PATH_']
			datafilepath =str('"'+dtp_temp + '/' + datafile+'"')
			datafilepath2 =str(dtp_temp + '/' + datafile)
			
			if dtp_temp == "Folder":
				sg.Print("ERROR, "+datafile+" NOT FOUND...\nPlease choose a folder.")
			else:
				try:
					if os.path.exists(datafilepath2):
						window['_PROGRESSBAR_'].UpdateBar((barmax/100)*10)
						cleandatafile(dtp_temp,"FGT_data")
						window['_PROGRESSBAR_'].UpdateBar((barmax/100)*100)
						temp_list = [x for x in selection_data if x not in selected_data]
						print("2")
						datalogcomb(temp_list,selected_data,datafilepath)
					else:
						sg.Print("ERROR, "+datafile+" NOT FOUND...\n",datafilepath2)
				except:
					print(datafilepath)
					sg.PopupScrolled("ERROR. DATA LOG OPEN ISSUE",keep_on_top=True,non_blocking=False)
			
			
		elif event in (None, 'Parameter Log'):
			dtp_temp = values['_INPUT_PATH_']
			paramfilepath = str('"'+dtp_temp + '/' + paramfile+'"')
			paramfilepath2 = str(dtp_temp + '/' + paramfile)
			if dtp_temp == "Folder":
				sg.Print("ERROR, "+datafile+" NOT FOUND...\nPlease choose a folder.")
			else:
				try: 
					if os.path.exists(paramfilepath2):
						cleandatafile(dtp_temp,"FGT_Param_Record")
					else:
						sg.Print("ERROR, FILE NOT FOUND...\n",paramfilepath2)
				except:
					sg.PopupScrolled("ERROR. PARAM LOG OPEN ISSUE",keep_on_top=True,non_blocking=False)
			

def listprint(testingl):
	if not testingl:
		return
	print(testingl[0])

def cleandatafile(fp,file):
	global window
	global barmax
	
	window['_PROGRESSBAR_'].UpdateBar((barmax/100)*0)
	with io.open(fp+ '/' + file + '.log', 'r') as f:
		text = f.read()
		window['_PROGRESSBAR_'].UpdateBar((barmax/100)*20)
	with io.open(fp+ '/' + file+'.log', 'w', encoding='utf8') as f:
		f.write(text)
		window['_PROGRESSBAR_'].UpdateBar((barmax/100)*40)
	paramstr = "DATE & TIME,R3801,R3802,R3803,R3804,R3805,R3806,R3807,R3808,R3809,R3810,R3811 Boiler High Temp,R3812 Attemperation Damper High Temp/Shunt Temp,R3813,R3814,R3815,R3816,R3817,R3818,R3819 Bag Filter Low Temp,R3820 Bag Filter Preheat Temp,R3821 Bag Filter High Temp,R3822,R3823,R3824,R3825,R3826,R3827,R3828,R3829,R3830,R3831,R3832,R3833,R3834,R3835,R3836,R3837,R3838,R3839,R3840,R3841 ABC High temp,R3842,R3843,R3844,R3845,R3846,R3847,R3848,R3849 Vent on FGT On ACD,R3850,R3851,R3852,R3853,R3854,R3855,R3856,R3857,R3858,R3859,R3860,R3861,R3862,R3863,R3864,R3865,R3866,R3867,R3868,R3869 ABC Min Speed,R3870,R3871,R3872,R3873,R3874,R3875,R3876,R3877,R3878,R3879,R3880,R3881,R3882,R3883,R3884,R3885,R3886,R3887,R3888,R3889,R3890,R3891,R3892,R3893,R3894,R3895,Name,Reason,R3869 ABC Min Speed"
	datastr = "Date,Event,Value, Unit,0,1,2,3,4"
	if(file == "FGT_data"):
		headerstr=datastr
	if(file == "FGT_Param_Record"):
		headerstr=paramstr
	cmd = str('echo F|xcopy /y /F "' + fp +'\\'+ file + '.log" "' + fp +'\\'+ file + '.csv"')
	os.system(cmd)
	window['_PROGRESSBAR_'].UpdateBar((barmax/100)*50)
	cmd = str('echo ' + headerstr + ' > "' + fp + '\datatemp.csv"')
	print(cmd)
	os.system(cmd)
	window['_PROGRESSBAR_'].UpdateBar((barmax/100)*70)
	cmd = str('type "' + fp +'\\'+ file + '.csv" >> "' +fp+'\datatemp.csv"')
	os.system(cmd)
	window['_PROGRESSBAR_'].UpdateBar((barmax/100)*90)
	cmd = str('echo F|xcopy /y /F "' +fp+'\datatemp.csv "'  + fp +'\\'+ file + '.csv"')
	os.system(cmd)
	
	
def datalogcomb():#datascrub,datakeep,datafilep
	
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
	
	#datafilep=datafilep.replace('.log','.csv')
	datafilep='B:/Desktop/WORK/python_gui/Rouen/Data/FGT_data.csv'#datafilep.replace('"','')
	print(datafilep)
##	df = pd.read_csv(
##		'C:/Users/agarth/Desktop/python_gui/Rouen/Data/FGT_data.csv',low_memory=False,
##		header=0,index_col=False,
##		)
	df = pd.read_csv(
		'B:/Desktop/WORK/python_gui/Rouen/Data/FGT_data.csv'
		)
	print("3")
	df.columns = ['Date','Event','Value', 'Unit','0','1','2','3','4']

	print ("cleaning up data\n")
	baddata=(df[df.Date.str.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"))==False])
	if (not baddata.empty):
		baddata.to_csv(datafilep+'/baddata.csv', index=False)
	df=(df[df.Date.str.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"))==True])
	df['Date']= pd.to_datetime(df['Date'])
	df = df.drop(df.columns[[4,5,6,7,8]], axis=1)
	
	df=df.str.strip()
	datascrub=datascrub.str.strip()
	datakeep=datakeep.str.strip()
	df=df.str.upper()
	datascrub=datascrub.str.upper()
	datakeep=datakeep.str.upper()

	print ("Getting years worth of data\n")
	dates = df['Date'].iloc[-1]
	if offsetspan == 1: dates2 = dates - pd.DateOffset(years=offsetspan_amount)
	elif offsetspan == 2: dates2 = dates - pd.DateOffset(months=offsetspan_amount)
	elif offsetspan == 3: dates2 = dates - pd.DateOffset(weeks=offsetspan_amount)
	elif offsetspan == 4: dates2 = dates - pd.DateOffset(days=offsetspan_amount)
	elif offsetspan == 5: dates2 = dates - pd.DateOffset(hours=offsetspan_amount)
	else: dates2 = dates - pd.DateOffset(year)
	
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
	
	print ("Removing unneeded data\n")
	for x in range(len(datascrub)):
		df = df[df.Event != datascrub[x]]

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
				preheated[name] = "Error"

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
	datalogcomb()
