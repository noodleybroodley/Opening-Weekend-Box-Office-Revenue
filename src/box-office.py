import pandas as pd
import matplotlib.pyplot as plt

#import data pulled from boxofficemojo.com on November 15th, 2021 using the create_csv script
df = pd.read_csv('../data/movies.csv')

#select only the 'Release', 'Opening', 'Date'
df = df[['Release','Opening','Date', 'Distributor']]

def cleaner(string):
    '''
    Parameter: String
    Return: Int

    Cleaner removes punctuation and special characters from a string and casts that string to an integer.
    '''
    string = "".join([l for l in string if l not in '$,' ])
    return int(string)

#converts the opening weekend revenue from a string to an integer
df['Opening'] = df['Opening'].apply(lambda x: cleaner(x))

#converts the date column to a datetime object
df['Date'] = pd.to_datetime(df['Date'])

#creates a Month column
df['Month'] = df['Date'].dt.month

#creates a Year column
df['Year'] = df['Date'].dt.year

#Replace the 3 null Distributors with 'The Weinstein Company'
df.loc[(df.Distributor == '-'),'Distributor']='The Weinstein Company'

month_list = ['January','February','March','April',
	              'May', 'June', 'July', 'August',
				  'September', 'October', 'November', 'December']

def create_studio_df_list(dataframe):
	'''
	parameter: DataFrame
	returns: List of DataFrame Objects

	Takes in a DataFrame object and returns a list of DataFrame objects containing only data for one studio.
	'''
	studio_list = ['Warner Bros.','Universal Pictures','Walt Disney Studios Motion Pictures','Twentieth Century Fox']
	df_list = []
	for studio in studio_list:
		df_list.append(dataframe[dataframe['Distributor']==studio])
	return df_list

def make_scatter(dataframe):
	'''
	parameter: DataFrame
	return: None (displays scatterplot)

	Takes in a DataFrame object and displays a scatterplot of the Opening Weekend Revenue vs Month of Release
	'''
	fig, ax = plt.subplots()
	ax.scatter(x=dataframe['Month'],y=dataframe['Opening'], alpha = 0.25)
	plt.xticks(list(range(1,13)), rotation=90)
	ax.set_xticklabels(month_list)
	
	fig.suptitle('Opening Weekend Revenue vs. Month of Release')
	
	plt.xlabel('Months')
	plt.ylabel('Opening Weekend Revenue ($100 Million)')
	ax.grid(axis="x", color="black", alpha=.5, linewidth=.5, linestyle=":")
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle=":")
	
	plt.show()

def median_bar_graph(dataframe):
	'''
	Parameter: dataframe - DataFrame Object
	Return: Bar Graph
	
	Create a bar graph of the median box office revenue for each month's releases.
	'''
	
	monthly_median_df = dataframe[['Month','Opening','Year']]
	monthly_median_df = monthly_median_df.groupby(by='Month', as_index=False).median().reset_index()
	
	x_values = monthly_median_df['Month']
	y_values = monthly_median_df['Opening']

	fig, ax = plt.subplots()
	ax.bar(x_values,height=y_values)

	plt.xticks(list(range(1,13)), rotation=90)
	ax.set_xticklabels(month_list)
	
	fig.suptitle('Median Opening Weekend Revenue')

	plt.xlabel('Months')
	plt.ylabel('Opening Weekend Revenue ($10 Million)')
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle=":")

	plt.tight_layout
	plt.show()

def make_hist(dataframe):
	'''
	Parameter: dataframe - DataFrame Object
	Return: Bar Graph
	
	Create a bar graph of the median box office revenue for each month's releases.
	'''
	
	fig, ax = plt.subplots()
	ax.hist(x=dataframe.Month,bins=12)

	plt.xticks(list(range(1,13)), rotation=90)
	ax.set_xticklabels(month_list)

	fig.suptitle('Distribution of Movie Releases over the Months')
	
	plt.xlabel('Months')
	plt.ylabel('Number of Releases')
	ax.grid(axis="x", color="black", alpha=.5, linewidth=.5, linestyle=":")
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle=":")
	
	plt.tight_layout()
	plt.show()

df['Month'].value_counts()

def create_year_bargraphs(dataframe):
	'''
	Parameter: dataframe - DataFrame Object
	Return: Bar Graph
	
	Creates bar graphs of the median box office revenue for each
	month's releases for the years 2010-2019.
	'''
	
	month_year_df = dataframe[['Month','Year','Opening']]
	year_list = [x for x in range(2010,2020)]

	fig, axes = plt.subplots(nrows=2, ncols=5, sharey=True,figsize=(30,10))
	i = 0
	for row in axes:
		for col in row:
			year_df = month_year_df.loc[(month_year_df.Year==year_list[i]),['Opening','Month']]
			plot_data = []
			for j in range(1,13):
				month_data = year_df.loc[(year_df.Month==j),'Opening']
				plot_data.append(month_data.median())
			col.bar(month_list,height=plot_data)
			col.title.set_text(f'{year_list[i]}')
			col.set_xticklabels(month_list,rotation=45)
			col.set_xlabel('Month')
			col.set_ylabel('Opening Weekend Revenue ($100 Million)')
			col.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle=":")
			i+=1
			
	fig.suptitle('Median Opening Weekend Revenue (2010-2019)')
	
	
	plt.xticks(rotation=45)
	plt.tight_layout()
	plt.show()

def create_year_hist(dataframe):
	'''
	Parameter: dataframe - DataFrame Object
	Return: Bar Graph
	
	Creates bar graphs of the median box office revenue for each
	month's releases for the years 2010-2019.
	'''
	month_list = ['January','February','March','April',
	              'May', 'June', 'July', 'August',
				  'September', 'October', 'November', 'December']
	
	month_year_df = dataframe[['Month','Year','Opening']]
	year_list = [x for x in range(2010,2020)]

	fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(30,10), sharey=True)
	i = 0
	for row in axes:
		for col in row:
			month_series= month_year_df.loc[(month_year_df.Year==year_list[i]),['Month']]
			col.hist(x=month_series, bins=12)
			col.title.set_text(f'{year_list[i]}')
			col.set_xlabel('Month')
			col.set_ylabel('Number of Releases')
			col.grid(axis="x", color="black", alpha=.5, linewidth=.5, linestyle=":")
			col.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle=":")
			col.set_xticklabels(month_list,rotation=45)
			i+=1
			
	#plt.setp(axes, xticks=list(range(0,12)),xticklabels=month_list)
	fig.suptitle('Distribution of Movie Releases over the Months (2010-2019)')
	plt.setp(axes, xticks=list(range(1,13)))
	plt.tight_layout()
	plt.show()

def create_studio_df_list(dataframe):
	'''
	parameter: DataFrame
	returns: List of DataFrame Objects

	Takes in a DataFrame object and returns a list of DataFrame objects containing only data for one studio.
	'''
	studio_list = ['Warner Bros.','Universal Pictures','Walt Disney Studios Motion Pictures','Twentieth Century Fox']
	df_list = []
	for studio in studio_list:
		df_list.append(dataframe[dataframe['Distributor']==studio])
	return df_list

def create_studio_bargraphs(dataframe):
	'''
	parameter: DataFrame
	returns: None

	Takes in a DataFrame object and returns a scatterplot showing the
	Opening Weekend Revenue for each film for the past 10 years.
	'''
	studio_list = ['Warner Bros.','Universal Pictures','Walt Disney Studios Motion Pictures','Twentieth Century Fox']
	month_list = ['January','February','March','April',
	              'May', 'June', 'July', 'August',
				  'September', 'October', 'November', 'December']
	df_list = create_studio_df_list(dataframe)

	fig, axes = plt.subplots(nrows=2, ncols=2, figsize = (10,10), sharey=True)
	
	i = 0
	for row in axes:
		for col in row:
			plot_data = []
			for month in range(1,13):
				month_data = df_list[i].loc[(df_list[i].Month==month),'Opening']
				plot_data.append(month_data.median())
			col.bar(month_list,height=plot_data)
			col.set_title(studio_list[i], fontsize = 20)
			col.set_xlabel('Month')
			col.set_ylabel('Opening Weekend Revenue ($100 Million)')
			col.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle=":")
			col.set_xticklabels(month_list,rotation=45)
			i+=1
		
	fig.suptitle('Median Opening Weekend Revenue (Top Four Studios)')
	plt.tight_layout()
	plt.show()

def create_studio_hist(dataframe):
	'''
	parameter: DataFrame
	returns: None

	Takes in a DataFrame object and returns a scatterplot showing the
	Opening Weekend Revenue for each film for the past 10 years.
	'''
	studio_list = ['Warner Bros.','Universal Pictures','Walt Disney Studios Motion Pictures','Twentieth Century Fox']
	month_list = ['January','February','March','April',
	              'May', 'June', 'July', 'August',
				  'September', 'October', 'November', 'December']
	df_list = create_studio_df_list(dataframe)

	fig, axes = plt.subplots(nrows=2, ncols=2, figsize = (10,10), sharey=True)
	
	i = 0
	for row in axes:
		for col in row:
			month_series = df_list[i].Month
			col.hist(x=month_series, bins=12)
			col.set_title(studio_list[i], fontsize = 20)
			col.set_xlabel('Month')
			col.set_ylabel('Number of Releases')
			col.grid(axis="x", color="black", alpha=.5, linewidth=.5, linestyle=":")
			col.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle=":")
			col.set_xticklabels(month_list,rotation=45)
			i+=1
		
	fig.suptitle('Distribution of Movie Releases over the Months (Top Four Studios)')
	plt.setp(axes, xticks=list(range(1,13)))
	plt.tight_layout()
	plt.show()

if __name__== "__main__":
	create_studio_df_list(df)
	
	make_scatter(df)

	median_bar_graph(df)

	make_hist(df)

	create_year_bargraphs(df)

	create_year_hist(df)

	create_studio_bargraphs(df)

	create_studio_hist(df)