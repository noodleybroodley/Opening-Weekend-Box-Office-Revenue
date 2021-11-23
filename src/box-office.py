import pandas as pd
import matplotlib.pyplot as plt

#import data pulled from boxofficemojo.com on November 15th, 2021
df = pd.read_csv('../data/movies.csv')

#select only the 'Release', 'Opening', 'Date'
df = df[['Release','Opening','Date', 'Distributor']]

def cleaner(string):
    '''
    Parameter: String
    Return: String

    Cleaner takes in a string and returns a string with all punctuation and special characters removed.
    '''
    string = "".join([l for l in string if l not in '!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{}~ ' ])
    return string

#converts the opening weekend revenue from a string to an integer
df['Opening'] = df['Opening'].apply(lambda x: int(cleaner(x)))

df['Date'] = pd.to_datetime(df['Date'])

df['Month'] = df['Date'].dt.month

df['Year'] = df['Date'].dt.year

#Replace the 3 null Distributors with 'The Weinstein Company'
df.loc[(df.Distributor == '-'),'Distributor']='The Weinstein Company'