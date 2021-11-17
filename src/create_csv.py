import pandas as pd
import ssl

#The below handles a certificate error when scraping the database from the website
ssl._create_default_https_context = ssl._create_unverified_context

#Set the URLs that you want to pull tables from
urls = ['https://www.boxofficemojo.com/chart/top_opening_weekend/','https://www.boxofficemojo.com/chart/top_opening_weekend/?offset=200',
'https://www.boxofficemojo.com/chart/top_opening_weekend/?offset=400',
'https://www.boxofficemojo.com/chart/top_opening_weekend/?offset=600',
'https://www.boxofficemojo.com/chart/top_opening_weekend/?offset=800']

#Reads in the first url from the list of urls, creates a list of dataframe objects from the table on that page,
#assigns 'df' as the first dataframe object in that list
df = pd.read_html(urls[0])[0]

#Iterates through the rest of the list of urls, creates new dataframes, concatenates the first dataframe with these new ones
for i in range(1, len(urls)):
	url = urls[i]
	new_df = pd.read_html(url)[0]
	df = pd.concat([df,new_df])

#Write final dataframe to csv file
df.to_csv('movies.csv')