import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import get
import requests


website_keys = {}
with open('website_keys.txt') as f:
    for line in f:
        line=line.split(':')
        website_keys[line[0].strip()]=line[1].strip()

def get_soup(key):
    base_url = 'http://governmentresponse.globalslaveryindex.org/country.php'
    data = {'agree': 1}
    payload = {'country': key}
    s = requests.Session()
    s.post(base_url, params=payload, data=data)
    result = s.get(base_url, params=payload)
    soup = BeautifulSoup(result.content, 'html.parser')
    return soup

def make_df(df, soup):
    page_body = soup.find('body')
    table = page_body.findChildren('ul')
    for i in range(2, 33):
        first = table[1].findChildren('li')[i]
        indicator = first.findChildren('div')[0].text.strip().split()[0]
        rating = first.findChildren('div')[1].text.strip()
        df["m1_"+indicator]=rating
    second = table[1].findChildren('li')[33]
    for i in range(1, 33):
        row = second.findChildren('li')[i]
        indicator = row.findChildren('div')[0].text.strip().split()[0]
        rating = row.findChildren('div')[1].text.strip()
        df["m2_"+indicator]=rating
    for i in range(69, 79):
        third = table[1].findChildren('li')[i]
        indicator = third.findChildren('div')[0].text.strip().split()[0]
        rating = third.findChildren('div')[1].text.strip()
        df["m3_"+indicator]=rating
    for i in range(81, 100):
        third = table[1].findChildren('li')[i]
        indicator = third.findChildren('div')[0].text.strip().split()[0]
        rating = third.findChildren('div')[1].text.strip()
        df["m4_"+indicator]=rating
    for i in range(102, 108):
        third = table[1].findChildren('li')[i]
        indicator = third.findChildren('div')[0].text.strip().split()[0]
        rating = third.findChildren('div')[1].text.strip()
        df["m5_"+indicator]=rating
    return df

def full_df():
    list_df = []
    for country in website_keys.keys():
        df_country = pd.DataFrame()
        df_country['country']= pd.Series([country])
        soup = get_soup(website_keys[country])
        df_country = make_df(df_country, soup)
        list_df.append(df_country)
    return pd.concat(list_df)



if __name__ == '__main__':
    # table = []
    # for key in website_keys.keys():
    # key = website_keys["Uruguay"]
    # soup = get_soup(key)
    # df = pd.DataFrame()
    # df['country']= pd.Series(["Uruguay"])
    # df_full= make_df(df, soup)
    # list_df = []
    # for country in website_keys.keys():
    #     df_country = pd.DataFrame()
    #     df_country['country']= pd.Series([country])
    #     soup = get_soup(website_keys[country])
    #     df_country = make_df(df_country, soup)
    #     list_df.append(df_country)
    df = full_df()
    df.to_csv('data/gov.csv')
