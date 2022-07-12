#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Scrape the following into CSV files. Each one is broken up into multiple tiers – the more you scrape the tougher it is!
# Scrape https://www.congress.gov/members (Links to an external site.)
# Tier 1: Scrape their name and full profile URL, and additional
# Tier 2: Separate their state/party/etc into separate columns
# Advanced: Scrape each person's actual data from their personal project

import pandas as pd
from bs4 import BeautifulSoup
import requests


# In[2]:


response = requests.get("https://www.congress.gov/members")
doc = BeautifulSoup(response.text)
doc


# In[3]:


import re

members = doc.find_all("li", class_="expanded")
base_url = "https://www.congress.gov/"

for member in members:

    name = member.find("a").text
    
    rm_representative = re.sub('Representative', '', name)
    rm_senator = re.sub('Senator', '', rm_representative)
    rm_commissioner = re.sub('Resident Commissioner', '', rm_senator)
    
    name = rm_commissioner
    
    url = base_url + member.find("a").get("href")
    state = member.find_all("span", class_="result-item")[0].select("span")[0].text
    party = member.find_all("span", class_="result-item")[1].select("span", class_="result-item")[0].text
    
    if party.isnumeric() == False:
        party

# main=main        
# class=search-column-main basic-search-results nav-on


# In[15]:


# Scrape https://www.marylandpublicschools.org/stateboard/Pages/Meetings-2018.aspx (Links to an external site.)
# Tier 1: Scrape the date, URL to agenda, URL to board minutes
# Tier 2: Download agenda items to an "agendas" folder and board minutes to a "minutes" folder

response = requests.get("https://www.marylandpublicschools.org/stateboard/Pages/Meetings-2018.aspx")
doc = BeautifulSoup(response.text)
# doc


# In[30]:


import os

table = doc.find("table")
base_url = "https://www.marylandpublicschools.org"

count = 2
length = len(doc.find("table").select("tr"))

agendas = []
minutes = []

for row in table:
    
    while count < length:
        url_agenda = base_url + row.select("tr")[count].find_all("a")[0].get("href")
        url_minutes = base_url + row.select("tr")[count].find_all("a")[1].get("href")
        url_dates = row.select("tr")[count].strong.text
        
        count = count + 1
        
        agendas.append(url_agenda)
        minutes.append(url_minutes)
    
current_dir = os.getcwd()
agendas_dir = os.path.join(current_dir, r'agendas')
minutes_dir = os.path.join(current_dir, r'minutes')

if not os.path.exists(agendas_dir):
   os.makedirs(agendas_dir)

if not os.path.exists(minutes_dir):
   os.makedirs(minutes_dir)


# In[6]:


# agendas_content = "\n".join(agendas)
# minutes_content = "\n".join(minutes)

# with open("agendas.txt", "w") as f:
#     f.write(agendas_content)

# with open("minutes.txt", "w") as f:
#     f.write(minutes_content)


# In[7]:


# !wget -i agendas.txt
# !wget -i minutes.txt


# In[33]:


# Scrape http://www.nvmcsd.org/our-school-board/meetings/agendas (Links to an external site.)
# Tier 1: Scrape the name of the link and the URL
# Tier 2: Add a column for the date (you'll need to manually edit some, probably [but using pandas!])
# Tier 3: Download the PDFs but name them after the date

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

response = requests.get("http://www.nvmcsd.org/our-school-board/meetings/agendas", headers=headers)
doc = BeautifulSoup(response.text)
# doc


# In[35]:


import re
import glob

links = doc.find("div", class_="kt-accordion-panel-inner").find_all("p")
dates = []

for link in links:
    link_name = link.text
    link_url = link.find("a").get("href")
    
    dates.append(link_url)
    
    # July 12, 2022 School Board Meeting
    # \w.\d+.,\d+
#     print(link_name)
            
    link_date = link_name \
        .replace("School Board Meeting", "") \
        .replace("Budget Committee Meeting", "") \
        .replace("MCSD Safety Committee Meeting", "") \
        .replace("February 4, Special Board Meeting", "February-4-2002-Special") \
        .replace("Policy Meeting", "") \
        .replace("Special Board Meeting", "") \
        .replace("MCSD Safety Committee Meeting", "") \
        .replace("Budget Committee Meeting", "") \
        .replace("Policy Committee ", "") \
        .replace("Budget Committee Meeting", "") \
        .replace("Board Meeting", "") \
        .replace(",", "") \
        .replace(" ", "-") \
        .replace("--", "-") \
        .replace("2022-", "2022") \
        .replace(";", "\n") \
        .replace("-Item-#3-Attachment", "April-19-2022-Item-3") \
        .replace("-Item-#2", "May-31-2022-Item-2") \
        .replace("-Item-#3", "May-31-2022-Item-3") \
        .replace("-January", "January") \
        .replace("Special-", "") \
        .replace("Safety-Committee-", "-Safety") \
      
#     print(link_name, link_url, (link_date).lower())


# In[36]:


file_content = "\n".join(dates)

with open("dates.txt", "w") as f:
    f.write(file_content)


# In[37]:


get_ipython().system('wget -i dates.txt')


# In[12]:


# Scrape https://rocktumbler.com/blog/rock-and-mineral-clubs/ (Links to an external site.)
# Tier 1: Scrape all of the name and city
# Tier 2: Scrape the name, city, and URL
# Tier 3: Scrape the name, city, URL, and state name (you'll probably need to learn about "parent" nodes)

response = requests.get("https://rocktumbler.com/blog/rock-and-mineral-clubs/")
doc = BeautifulSoup(response.text)
# doc


# In[13]:


tables = doc.find("article").select("table")

for table in tables:
    col_name = table.find("td", attrs={"width": "60%"})
    col_city = table.find("td", attrs={"width": "40%"})
    
    name_city = table.tr.text
    state = ((table.parent.parent.find("map").area.get("href")).replace("#", "")).upper()
    
    if col_name != None:
        name = col_name.a.text
        url = col_name.a.get("href")
    
    if col_city:
        city = col_city.text

