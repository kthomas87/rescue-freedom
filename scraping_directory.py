import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import get
import requests
from selenium import webdriver
from time import sleep



def get_soup():
    url = 'http://globalmodernslavery.org/'
    d = webdriver.Chrome()
    d.get(url)
    sleep(20)
    soup = BeautifulSoup(d.page_source, 'html.parser')
    return soup

def make_df(soup):
        orgs = soup.select('div.org-row.row.row-eq-height')
        org_name = []
        org_info = []
        t_types = []
        for row in range(0, 2157):
            org_name.append(orgs[row].findChildren('h2')[0].text.strip())
            org_info.append(orgs[row].find('div' , {'class' : 'organizations col-xs-12 col-sm-4'}).text.strip())
            ttypes = orgs[row].findChildren('div')[1].findChildren('p')
            if len(ttypes)!=0:
                ttypes=ttypes[0].text.strip().split(':')[1].split(',')
            else:
                ttypes= None
            t_types.append(ttypes)
        df = pd.DataFrame()
        df['org_name']=org_name
        df['org_info']=org_info
        df['trafficking_types']=t_types
        return df

def extract_country(df):
    location = []
    for item in org_info:
        location.append(item.split(':')[-1])
    df['location']=location
    country = []
    for item in location:
        first = item.strip().split(',')[-1]
        if "United States" in first:
            country.append('United States')
        elif 'Uganda' in first:
            country.append('Uganda')
        elif 'Democratic Republic of Congo' in first:
            country.append('Democratic Republic of Congo')
        elif "South Korea" in first:
            country.append('South Korea')
        elif 'Singapore' in first:
            country.append('Singapore')
        elif 'United Kingdom' in first:
            country.append('United Kingdom')
        elif 'Bolivia' in first:
            country.append('Bolivia')
        elif 'India' in first:
            country.append('India')
        elif 'Nigeria' in first:
            country.append('Nigeria')
        elif 'Mexico' in first:
            country.append('Mexico')
        elif 'Argentina' in first:
            country.append('Argentina')
        elif 'Paraguay' in first:
            country.append('Paraguay')
        elif 'Somalia' in first:
            country.append('Somolia')
        elif 'The Netherlands' in first:
            country.append('Netherlands')
        elif 'Philippines' in first:
            country.append('Philippines')
        elif 'Switzerland' in first:
            country.append('Switzerland')
        elif 'Liberia' in first:
            country.append('Liberia')
        elif 'Hong Kong' in first:
            country.append("Hong Kong, SAR China")
        elif 'Malaysia' in first:
            country.append('Malaysia')
        elif 'Brazil' in first:
            country.append('Brazil')
        elif 'Chile' in first:
            country.append('Chile')
        elif 'Thailand' in first:
            country.append('Thailand')
        elif 'Sengal' in first:
            country.append('Sengal')
        elif 'Czech Republic' in first:
            country.append('Czech Republic')
        elif 'Belgium' in first:
            country.append('Belgium')
        elif 'Guinea' in first:
            country.append('Guinea')
        elif 'Malta' in first:
            country.append('Malta')
        elif "Cote d'Ivoire" in first:
            country.append("Cote d'Ivoire")
        else:
            country.append(first)
    return country

def extract_sex_trafficking(df):
    sex_trafficking = []
    for row in df['trafficking_types']:
        if row != None:
            row= set(row)
            if " Sex Trafficking" in row:
                sex_trafficking.append(1)

            else:
                sex_trafficking.append(0)
        else:
            sex_trafficking.append(0)
    return sex_trafficking

if __name__ == '__main__':
    soup = get_soup()
    df = make_df(soup)
    country = extract_country(df)
    df['country']=country
    sex_trafficking = extract_sex_trafficking(df)
    df['sex_trafficking']=sex_trafficking
    df_sex_trafficking = df[df['sex_trafficking']==1]
    df_sex_trafficking.to_csv('data/directory.csv')
    count = df_sex_trafficking['country'].str.strip().value_counts()
    count.to_csv('data/num_ngos.csv')
