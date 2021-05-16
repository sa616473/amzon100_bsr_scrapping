#!/usr/bin/env python
# coding: utf-8

# In[3]:


from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import time


# In[4]:


INITIAL_URL = "https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_boost_1"


# In[7]:


#initializing selium
driver = webdriver.Chrome()
driver.get(INITIAL_URL)
src=driver.page_source
soup=BeautifulSoup(src,'html.parser')


# In[11]:


list_of_departments = soup.findAll('ul',{'id':'zg_browseRoot'})


# In[54]:


links_to_bsr_dep = []
dep = []
for department in list_of_departments:
    a_tag = department.findAll('a')


# In[82]:


for tag in a_tag:
    dep.append(tag.text)
    print(tag['href'])
    links_to_bsr_dep.append(tag['href'])


# In[90]:


dep_dict = {'department': dep, 'URL': links_to_bsr_dep}


# In[ ]:





# In[91]:


temp = pd.DataFrame(dep_dict)
temp.to_csv("department.csv")


# In[ ]:





# In[ ]:





# In[ ]:




